"""A script to run the entire steam pipeline"""

# Native imports
from os import environ as ENV

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
from lambda_extract_steam import scrape_newest, parse_args
from transform import clean_data
from load import load_data


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


def lambda_handler(event=None, context=None):
    """Function to run entire Steam ETL pipeline"""
    # Initialise
    args = parse_args()
    target_date = args.scroll_to_date
    if target_date is None:
        target_date = "11 Feb, 2025"
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    CONN_STRING = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    db_connection = psycopg.connect(CONN_STRING, row_factory=dict_row)

    # Extract
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&supportedlang=english&ndl=1"
    scraped_data = scrape_newest(url, target_date)

    # Transform
    cleaned_data = clean_data(scraped_data)
    cleaned_data = change_keys(cleaned_data)

    # Load
    load_data(cleaned_data, db_connection)
    return


if __name__ == "__main__":
    lambda_handler()
