"""A script to run the entire GOG pipeline"""

# Native imports
from os import environ as ENV

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
from gog_lambda_extract import scrape_newest, lambda_driver, local_driver 
from gog_transform import clean_data
from gog_load import load_data


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
    target_date = "11 Feb, 2025"
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    CONN_STRING = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    db_connection = psycopg.connect(CONN_STRING, row_factory=dict_row)
    
    driver = local_driver()
    # driver = lambda_driver()

    # Extract
    url = "https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2025,2025"
    scraped_data = scrape_newest(url, driver)

    # Transform
    cleaned_data = clean_data(scraped_data)
    cleaned_data = change_keys(cleaned_data)

    # Load
    load_data(cleaned_data, db_connection)
    return


if __name__ == "__main__":
    lambda_handler()
