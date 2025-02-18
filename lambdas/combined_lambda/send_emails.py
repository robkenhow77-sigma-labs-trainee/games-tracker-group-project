import boto3
import json
from os import environ as ENV
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict
import psycopg2
import logging
from psycopg2.extras import RealDictCursor

# Load environment variables from .env file
load_dotenv()


def sns_connect():
    """Connect to sns client"""
    print("Connecting to SNS...")
    client = boto3.client(
        'sns',
        aws_access_key_id=ENV['AWS_ACCESS_KEY'],
        aws_secret_access_key=ENV['AWS_SECRET_ACCESS_KEY'],
        region_name=ENV['AWS_REGION']
    )
    print("Connected to SNS.")
    return client


def get_connection():
    """Connects to the games database"""
    print("Connecting to database...")
    connection = psycopg2.connect(
        dbname=ENV['DB_NAME'],
        user=ENV['DB_USERNAME'],
        password=ENV['DB_PASSWORD'],
        host=ENV['DB_HOST'],
        port=ENV['DB_PORT'],
        cursor_factory=RealDictCursor)
    print("Connected to database.")
    return connection


def get_new_games(conn):
    """Queries database for games released in past 24h"""
    previous_day = (datetime.now() - timedelta(days=1)).date()
    print(f"Fetching games released since {previous_day}...")

    query = """SELECT 
    g.game_id, 
    g.game_name, 
    g.game_image, 
    STRING_AGG(ge.genre_name, ', ') AS genre_names,  -- ✅ Collects all genres
    p.platform_release_date, 
    pl.platform_name,
    -- calc discount
    CASE 
        WHEN p.platform_discount > 0 
        THEN CONCAT('£', ROUND((p.platform_price * (1 - p.platform_discount / 100.0)) / 100.0, 2)) 
        WHEN p.platform_price = 0 
        THEN 'Free'
        ELSE CONCAT('£', ROUND(p.platform_price / 100.0, 2))
    END AS final_price,
    CASE 
        WHEN p.platform_discount > 0 THEN CONCAT(p.platform_discount, '%% off')
        ELSE 'No discount'
    END AS discount_info
FROM game AS g
JOIN game_platform_assignment AS p USING (game_id)
JOIN genre_game_platform_assignment AS gp USING (platform_assignment_id)
JOIN genre AS ge USING (genre_id)
JOIN platform AS pl USING (platform_id)
WHERE p.platform_release_date >= %s
GROUP BY g.game_id, g.game_name, g.game_image, p.platform_release_date, pl.platform_name, p.platform_price, p.platform_discount;
"""

    with conn.cursor() as cur:
        cur.execute(query, (previous_day,))
        res = cur.fetchall()

    print(f"Found {len(res)} new games.")
    return res


def get_subscribers_for_genres(client):
    """Retrieve all subscribers for each genre (SNS topic) in one call per genre."""
    print("Fetching subscribers for each genre...")
    subscribers_by_genre = defaultdict(set)

    next_token = None
    topics = []
    while True:
        if next_token:
            response = client.list_topics(NextToken=next_token)
        else:
            response = client.list_topics()

        topics.extend(response["Topics"])

        next_token = response.get("NextToken")
        if not next_token:
            break

    print(f"Found {len(topics)} topics.")

    for topic in topics:
        topic_arn = topic["TopicArn"]
        genre = topic_arn.split(":")[-1]

        formatted_genre = genre.replace('play_stream_', '')
        formatted_genre = formatted_genre.replace('_', ' ').title()

        if genre.startswith('play_stream'):
            print(f"Checking topic: {topic_arn} ({formatted_genre})")

            next_token = None
            while True:
                params = {"TopicArn": topic_arn}
                if next_token:
                    params["NextToken"] = next_token

                response = client.list_subscriptions_by_topic(**params)

                for sub in response["Subscriptions"]:
                    if sub["Protocol"] == "email" and sub["SubscriptionArn"] != "PendingConfirmation":
                        subscribers_by_genre[formatted_genre].add(
                            sub["Endpoint"])

                next_token = response.get("NextToken")
                if not next_token:
                    break

    print(f"Found subscribers for {len(subscribers_by_genre)} genres.")
    for genre, subscribers in subscribers_by_genre.items():
        print(f"Subscribers for {genre}: {list(subscribers)}")
    return subscribers_by_genre


def generate_html(genre_name, game_data, subscribers):
    """Generates HTML email body with all games for the genre (with images)"""
    print(
        f"Generating HTML for {genre_name} genre with {len(game_data)} games and {len(subscribers)} subscribers...")

    body_html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #f0f0f0;
                        padding: 20px;
                        margin: 0;
                        width: 100%;
                        text-align: center;
                        background-color: #152736;
                    }}
                    .email-container {{
                        width: 90%;
                        max-width: 600px;  
                        margin: 40px auto;
                        padding: 20px;
                        background-color: #1b3a4b;
                        border-radius: 10px;
                        text-align: center;
                    }}
                    h1, h2, p {{
                        color: #f0f0f0;
                        text-align: center;
                    }}
                    .game-table {{
                        width: 100%;
                        border-spacing: 0;
                    }}
                    .game {{
                        width: 100%;
                        background-color: #204050;
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 15px;
                        text-align: center;
                    }}
                    .game img {{
                        max-width: 100%;
                        height: auto;
                        display: block;
                        margin: 0 auto;
                        border-radius: 5px;
                    }}
                    .game-title {{
                        font-size: 20px;
                        font-weight: bold;
                        color: #f0f0f0;
                        margin-top: 10px;
                    }}
                    .game-info {{
                        font-size: 16px;
                        color: #f0f0f0;
                        margin-top: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <h1>New Game Releases in {genre_name}</h1>
                    <table class="game-table">
    """

    # List games one by one using table rows
    print('GAME DATA ', game_data)
    for game in game_data:
        game_name = game["game_name"]
        game_image = game["game_image"]
        release_date = game["release_date"]
        price = game["final_price"]
        platform = game["platform"]

        body_html += f"""
            <tr>
                <td class="game">
                    <img src="{game_image}" alt="{game_name}">
                    <div class="game-title">{game_name} - {price}</div>
                    <div class="game-info">Release Date: {release_date}</div>
                    <div class="game-info">Available for the best price on <b>{platform}</b></div>
                </td>
            </tr>
        """

    body_html += f"""
                    </table>
                    <p>Check out these new games now! Available on Steam, GoG, and Epic.</p>
                </div>
            </body>
        </html>
    """

    print(f"HTML generated for {genre_name} genre:\n{body_html[:500]}...")
    return body_html


def get_ses_connection():
    """Get SES client connection"""
    print("Connecting to SES...")
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=ENV['AWS_ACCESS_KEY'],
        aws_secret_access_key=ENV['AWS_SECRET_ACCESS_KEY'],
        region_name=ENV['AWS_REGION']
    )
    print("Connected to SES.")
    return ses_client


def send_email(ses_client, email_data):
    """Send emails for each genre to subscribers using SES"""
    print("Sending emails...")
    for genre, details in email_data.items():
        subscribers = details['subscribers']
        html_body = details['html_body']

        # iterate each subscriber of the genre
        for subscriber in subscribers:
            email_params = {
                'Destination': {
                    'ToAddresses': [subscriber]
                },
                'Message': {
                    'Body': {
                        'Html': {
                            'Data': html_body
                        }
                    },
                    'Subject': {
                        'Data': f'🎮 New Game Releases in {genre}'
                    }
                },
                'Source': 'trainee.jamie.groom@sigmalabs.co.uk',
            }

            try:
                response = ses_client.send_email(**email_params)
                print(
                    f"Email sent to {subscriber} with response: {response['ResponseMetadata']}")
            except Exception as e:
                print(f"Error sending email to {subscriber}: {e}")

    print("Emails sent.")
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Emails sent successfully.'})
    }


def lambda_handler(event, context):

    log_format = "{asctime} - {levelname} - {message}"
    log_datefmt = "%Y-%m-%d %H:%M"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        style="{",
        datefmt=log_datefmt
    )
    logging.info("Lambda function started")

    sns_client = sns_connect()
    db_conn = get_connection()

    new_games = get_new_games(db_conn)

    # get subscribers grouped by genre
    subscribers_by_genre = get_subscribers_for_genres(sns_client)
    print(f"Found {len(subscribers_by_genre)} genres with subscribers.")
    logging.info(f"Found {len(subscribers_by_genre)} genres with subscribers.")

    # organise games by game_name and associated genres
    games_dict = defaultdict(
        lambda: {"genres": set(), "release_date": None, "game_image": None, "final_price": None, "platform": None})

    # get data from query and store in dict for each game
    for row in new_games:
        game_name = row["game_name"]
        genres = row["genre_names"].split(", ")
        release_date = row["platform_release_date"]
        game_image = row["game_image"]
        final_price = row['final_price']
        platform = row['platform_name']

        games_dict[game_name]["genres"].update(genres)
        games_dict[game_name]["release_date"] = release_date
        games_dict[game_name]["game_image"] = game_image
        games_dict[game_name]["final_price"] = final_price
        games_dict[game_name]["platform"] = platform

    logging.info(f"Games dict populated with {len(games_dict)} games.")

    logging.info("Games dict: ", games_dict)

    email_data = defaultdict(lambda: {"games": [], "subscribers": []})

    # populate email_data with games and their subscribers by genre
    for game_name, details in games_dict.items():
        game_genres = sorted(details["genres"])
        release_date = details["release_date"]
        game_image = details["game_image"]
        final_price = details["final_price"]
        platform = details["platform"]

        for genre in game_genres:
            formatted_genre = genre.replace('play_stream_', '')
            formatted_genre = formatted_genre.replace('_', ' ').title()

            if formatted_genre in subscribers_by_genre:
                email_data[formatted_genre]["games"].append({
                    "game_name": game_name,
                    "game_image": game_image,
                    "release_date": release_date,
                    "final_price": final_price,
                    "platform": platform
                })
                email_data[formatted_genre]["subscribers"] = list(
                    subscribers_by_genre[formatted_genre])

    # Generate html for each genre
    final_email_data = {}

    logging.info('Email Data', email_data)

    for genre, data in email_data.items():
        if data["subscribers"]:  # only send emails if there are subscribers
            email_body = generate_html(
                genre,
                data["games"],
                data["subscribers"]
            )
            final_email_data[genre] = {
                "subscribers": data["subscribers"],
                "html_body": email_body
            }

    logging.info(
        f"Final email data prepared for {len(final_email_data)} genres.")

    # Send emails through SES
    ses_client = get_ses_connection()
    return send_email(ses_client, final_email_data)
