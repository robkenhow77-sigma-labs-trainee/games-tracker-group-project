"""A script to run the entire steam pipeline"""

# Native imports
from os import environ as ENV
from datetime import datetime, timedelta
from argparse import ArgumentParser
import logging

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
from steam_extract import scrape_newest
from steam_transform import clean_data
from steam_load import load_data


def init_args() -> tuple:
    """Gets the command line arguments for target date or running local vs cloud."""
    parser = ArgumentParser()

    parser.add_argument(
            "-l", "--local",
            action="store_true",
            required=False,
            help="Call argument to run local.")

    parser.add_argument(
            "-t", "--target_date",
            type=str,
            required=False,
            help="Set a target date, in the form' 11 Feb, 2025'. Defaults to yesterday.")

    args = parser.parse_args()
    return (args.local, args.target_date)


def change_keys(data: list[dict]):
    """Converts the key names from the transform script to match the load script"""
    updated_keys = []
    for game in data:
        updated_keys.append({
        "game_name": game['title'],
        "developer":  game['developer'],
        "tag":  game['tag'],
        "genre": game['genres'],
        "publisher":  game['publisher'],
        "release_date": game['release_date'],
        "game_image": game['game_image'],
        "is_nsfw": False, # NEED TO CHANGE!!
        "age_rating": game['age_rating'],
        "platform": game['platform'],
        "score": game['platform_score'],
        "price": game['platform_price'],
        "discount": game['platform_discount']
        })
    return updated_keys


def lambda_handler(event=None, context=None) -> None:
    """Function to run entire Steam ETL pipeline"""
    # Initialise
    # Logging
    log_format = "{asctime} - {levelname} - {message}"
    log_datefmt = "%Y-%m-%d %H:%M"
    logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            style="{",
            datefmt=log_datefmt
        )

    # CLI arguments
    local, target_date = init_args()

    if not target_date:
        target_date = datetime.now() - timedelta(days=2)
        target_date = target_date.strftime('%d %b, %Y')

    # ENV variables
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    conn_string = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    db_connection = psycopg.connect(conn_string, row_factory=dict_row)

    # Extract
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&supportedlang=english&ndl=1"
    scraped_data = scrape_newest(url, target_date, local, db_connection)

    # Transform
    cleaned_data = clean_data(scraped_data)
    cleaned_data = change_keys(cleaned_data)

    # Load
    load_data(cleaned_data, db_connection)
    db_connection.close()
    return


if __name__ == "__main__":
    log_format = "{asctime} - {levelname} - {message}"
    log_datefmt = "%Y-%m-%d %H:%M"
    logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            style="{",
            datefmt=log_datefmt
        )
    
    load_dotenv()

    lambda_handler()
