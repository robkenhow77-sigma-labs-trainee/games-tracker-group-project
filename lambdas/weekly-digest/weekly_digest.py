"""Creates an email giving weekly digestible information on new game platform trends"""

from psycopg2.extensions import connection
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import boto3
from os import environ as ENV
from dotenv import load_dotenv
from datetime import datetime


def get_sns_connection() -> boto3.client:
    """Get SNS client connection"""
    print("Connecting to SNS...")
    client = boto3.client(
        'sns',
        aws_access_key_id=ENV['AWS_ACCESS_KEY'],
        aws_secret_access_key=ENV['AWS_SECRET_ACCESS_KEY'],
        region_name=ENV['AWS_REGION']
    )
    print("Connected to SNS.")
    return client


def get_ses_connection() -> boto3.client:
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


def get_database_connection() -> connection:
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


def get_weekly_top_games(conn: connection) -> pd.DataFrame:
    """Returns a Dataframe of the top games of the week per week"""
    query = """SELECT
    g.game_id AS id,
    g.game_name AS title,
    gpa.platform_release_date AS release_date,
    g.game_image AS cover_image_url,
    p.platform_name,
    gpa.platform_score
    FROM game AS g
    JOIN game_platform_assignment AS gpa ON g.game_id = gpa.game_id
    JOIN platform AS p ON gpa.platform_id = p.platform_id
    WHERE gpa.platform_release_date >= CURRENT_DATE - INTERVAL '7 days'
    ORDER BY gpa.platform_score DESC
    LIMIT 10;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=['id', 'title', 'release_date', 'cover_image_url', 'platform_name', 'platform_score'])


def sum_of_games_released_per_platform(conn: connection) -> pd.DataFrame:
    """Returns the number of games released this week per platform"""
    query = """SELECT
    p.platform_name,
    COUNT(g.game_id) AS game_count
    FROM game AS g
    JOIN game_platform_assignment AS gpa ON g.game_id = gpa.game_id
    JOIN platform AS p ON gpa.platform_id = p.platform_id
    WHERE gpa.platform_release_date >= CURRENT_DATE - INTERVAL '7 days'  -- Games released this week
    GROUP BY p.platform_name
    ORDER BY game_count DESC;"""

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=['platform_name', 'game_count'])


def generate_email_content(top_games: pd.DataFrame, sum_of_games: pd.DataFrame) -> str:
    """Generates an HTML email with the platform game count table at the top and the top games table below"""
    dark_cyan = "#006F6A"
    blue = "#003F87"

    html = f"""<html><body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: {blue};">Weekly Game Platform Trends</h2>
    <p>Here are the number of games released per platform this week:</p>
    
    <table border='1' cellpadding='5' cellspacing='0' style="border-collapse: collapse; width: 100%; background-color: #f9f9f9;">
    <tr style="background-color: {dark_cyan}; color: white;">
        <th>Platform</th><th>Games Released</th>
    </tr>"""

    for i, (_, row) in enumerate(sum_of_games.iterrows()):
        row_style = f"background-color: {dark_cyan}; color: white;" if i % 2 == 0 else "background-color: #ffffff; color: #333;"
        html += f"<tr style='{row_style}'><td>{row['platform_name']}</td><td>{row['game_count']}</td></tr>"

    html += "</table>"

    html += "<p>Here are the top games released this week:</p>"
    html += """<table border='1' cellpadding='5' cellspacing='0' style="border-collapse: collapse; width: 100%; background-color: #f9f9f9;">
    <tr style="background-color: {dark_cyan}; color: white;">
        <th>Title</th><th>Platform</th><th>Release Date</th><th>Score</th><th>Cover</th>
    </tr>"""

    for i, (_, row) in enumerate(top_games.iterrows()):
        release_date_str = row['release_date'].strftime('%Y-%m-%d')

        row_style = f"background-color: {dark_cyan}; color: white;" if i % 2 == 0 else "background-color: #ffffff; color: #333;"

        html += f"""
        <tr style="{row_style}">
            <td>{row['title']}</td>
            <td>{row['platform_name']}</td>
            <td>{release_date_str}</td>
            <td>{row['platform_score']}</td>
            <td><img src='{row['cover_image_url']}' width='100'/></td>
        </tr>"""

    html += "</table></body></html>"
    return html


def write_html_to_file(html_body: str):
    """Writes the HTML to a file for testing purposes"""
    with open("weekly_digest.html", "w", encoding="utf-8") as file:
        file.write(html_body)


def get_subscribers(sns_conn: boto3.client) -> list[str]:
    """Gets a list of subscribers for the 'play_stream_weekly_digest' topic"""
    response = sns_conn.list_subscriptions_by_topic(
        TopicArn=ENV['SNS_TOPIC_ARN'])
    subscribers = [sub['Endpoint'] for sub in response.get('Subscriptions', []) if sub['Protocol'] == 'email']
    return subscribers


def send_email(ses_client: boto3.client, subscribers: list, html_body: str):
    """Sends an email with the HTML content to subscribers"""
    for subscriber in subscribers:
        ses_client.send_email(
            Source="trainee.jamie.groom@sigmalabs.co.uk",
            Destination={'ToAddresses': [subscriber]},
            Message={
                'Subject': {'Data': "Weekly Game Platform Trends"},
                'Body': {'Html': {'Data': html_body}}
            }
        )


def lambda_handler():
    """Main function"""
    load_dotenv()
    conn = get_database_connection()

    top_games = get_weekly_top_games(conn)
    sum_of_games = sum_of_games_released_per_platform(conn)
    html_body = generate_email_content(top_games, sum_of_games)
    write_html_to_file(html_body)

    sns_client = get_sns_connection()
    subscribers = get_subscribers(sns_client)
    ses_client = get_ses_connection()
    send_email(ses_client, subscribers, html_body)


if __name__ == "__main__":
    lambda_handler()
