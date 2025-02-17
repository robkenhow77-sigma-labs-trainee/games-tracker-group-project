from os import environ as ENV
import boto3
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict
import psycopg2
from psycopg2.extras import RealDictCursor
import json


def sns_connect():
    """Connect to sns client"""
    client = boto3.client(
        'sns',
        aws_access_key_id=ENV['AWS_ACCESS_KEY'],
        aws_secret_access_key=ENV['AWS_SECRET_ACCESS_KEY'],
        region_name=ENV['AWS_REGION']
    )
    return client


def get_connection():
    """Connects to the games database"""
    connection = psycopg2.connect(
        dbname=ENV['DB_NAME'],
        user=ENV['DB_USERNAME'],
        password=ENV['DB_PASSWORD'],
        host=ENV['DB_HOST'],
        port=ENV['DB_PORT'],
        cursor_factory=RealDictCursor)

    return connection


def get_new_games(conn):
    """Queries database for games released in past 24h"""
    previous_day = (datetime.now() - timedelta(days=2)).date()
    print('PREVIOUS DAY', previous_day)
    query = """select g.game_name, ge.genre_name, p.platform_release_date
    from game as g
    join game_platform_assignment as p using (game_id)
    join genre_game_platform_assignment as gp using (platform_assignment_id)
    join genre as ge using (genre_id)
    where platform_release_date >= %s"""

    with conn.cursor() as cur:
        cur.execute(query, (previous_day,))
        res = cur.fetchall()

    print(f"Found {len(res)} new games.")
    return res


def get_subscribers_for_genres(client):
    """Retrieve all subscribers for each genre (SNS topic) in one call per genre."""
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
            print(f"Checking topic: {topic_arn}")

            next_token = None
            while True:
                params = {"TopicArn": topic_arn}
                if next_token:
                    params["NextToken"] = next_token

                response = client.list_subscriptions_by_topic(**params)

                for sub in response["Subscriptions"]:
                    if sub["Protocol"] == "email" and sub["SubscriptionArn"] != "PendingConfirmation":
                        subscribers_by_genre[formatted_genre].add(
                            sub["Endpoint"])  # Add email address

                # check for additional pages of subscribers
                next_token = response.get("NextToken")
                if not next_token:
                    break

    print('Subscribers: ', subscribers_by_genre.values())
    print(
        f"Found {sum(len(subs) for subs in subscribers_by_genre.values())} subscribers.")
    return subscribers_by_genre


def generate_html(game_name, genre, game_genres, release_date, subscribers):
    """Generates HTML email body with all games for the genre"""
    print('GENERATE HTML')

    body_html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #333333;
                        background-color: #f9f9f9;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #4CAF50;
                    }}
                    .button {{
                        color: white;
                        background-color: #4CAF50;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <h1>🎮 New Game Releases in {genre}</h1>
                <h2>Games:</h2>
                <ul>
    """

    for game in game_genres:
        body_html += f"<li>{game}</li>"

    body_html += f"""
                </ul>
                <p>Check out the games now and enjoy the new experience!</p>
                <a href="https://your-game-link.com" class="button">Play Now</a>
                <h2>Subscribers for {genre} Genre:</h2>
                <ul>
    """

    for subscriber in subscribers:
        body_html += f"<li>{subscriber}</li>"

    body_html += "</ul></body></html>"

    return body_html


def lambda_handler(event, context):
    sns_client = sns_connect()
    db_conn = get_connection()
    new_games = get_new_games(db_conn)

    # get subscribers grouped by genre
    subscribers_by_genre = get_subscribers_for_genres(sns_client)
    print(f"Found {len(subscribers_by_genre)} genres with subscribers.")
    print("Subscribers by Genre:", subscribers_by_genre)

    # organize games by game_name and associated genres
    games_dict = defaultdict(lambda: {"genres": set(), "release_date": None})

    for row in new_games:
        game_name = row["game_name"]
        genre = row["genre_name"]
        release_date = row["platform_release_date"]

        games_dict[game_name]["genres"].add(genre)
        games_dict[game_name]["release_date"] = release_date

    print(f"Games dict populated: {games_dict}")

    email_data = defaultdict(lambda: {"games": [], "subscribers": []})

    # populate email_data with games and their subscribers by genre
    for game_name, details in games_dict.items():
        game_genres = sorted(details["genres"])
        release_date = details["release_date"]

        for genre in game_genres:
            formatted_genre = genre.replace('play_stream_', '')
            formatted_genre = formatted_genre.replace('_', ' ').title()

            if formatted_genre in subscribers_by_genre:
                email_data[formatted_genre]["games"].append(game_name)
                email_data[formatted_genre]["subscribers"] = list(
                    subscribers_by_genre[formatted_genre])

    # Generate html for each genre
    final_email_data = {}

    for genre, data in email_data.items():
        if data["subscribers"]:  # only send emails if there are subscribers
            email_body = generate_html(
                ", ".join(data["games"]),
                genre,
                data["games"],
                release_date,
                data["subscribers"]
            )
            final_email_data[genre] = {
                "subscribers": data["subscribers"],
                "html_body": email_body
            }

    print(f"Final email_data: {final_email_data}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Emails generated for new games.", "email_data": final_email_data})
    }
