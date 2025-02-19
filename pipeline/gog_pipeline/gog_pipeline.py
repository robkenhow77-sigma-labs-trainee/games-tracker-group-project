"""A script to run the entire gog pipeline"""

# Native imports
from os import environ as ENV
import logging
from argparse import ArgumentParser
from datetime import datetime, timedelta

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
from gog_extract import scrape_newest
from gog_transform import clean_data
from gog_load import load_data


def init_args() -> bool:
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
        "is_nsfw": game["NSFW"],
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
    # Initialise logging
    log_format = "{asctime} - {levelname} - {message}"
    log_datefmt = "%Y-%m-%d %H:%M"
    logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            style="{",
            datefmt=log_datefmt
        )
    # CLI arguments
    local, targeted_date = init_args()

    if not targeted_date:
        targeted_date = datetime.now() - timedelta(days=2)
        targeted_date = targeted_date.strftime('%d %b, %Y')

    # ENV variables
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    CONN_STRING = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    db_connection = psycopg.connect(CONN_STRING, row_factory=dict_row)

    

    # Extract
    url = 'https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2025,2025'
    scraped_data = scrape_newest(url, local, db_connection)

    # Transform
    cleaned_data = clean_data(scraped_data, targeted_date)
    cleaned_data = change_keys(cleaned_data)
    

    # Load
    load_data(cleaned_data, db_connection)
    return


if __name__ == "__main__":
    # Initialise logging
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
