"""A script to run the entire gog pipeline"""

# Native imports
from os import environ as ENV
from datetime import datetime, timedelta
from argparse import ArgumentParser

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

    args = parser.parse_args()
    return args.local


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
    # CLI arguments
    local = init_args()

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
    scraped_data = scrape_newest(url, local)

    # Transform
    cleaned_data = clean_data(scraped_data)
    cleaned_data = change_keys(cleaned_data)

    # Load
    load_data(cleaned_data, db_connection)
    print(cleaned_data, "data loaded")
    return


if __name__ == "__main__":
    lambda_handler()
