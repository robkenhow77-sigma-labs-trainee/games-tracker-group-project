"""A script to run the entire steam pipeline"""

# Native imports
from os import environ as ENV

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
from extract_steam import scrape_newest, parse_args
from transform import clean_data
from load import load_data


def lambda_handler(event=None, context=None):
    """Function to run entire Steam ETL pipeline"""
    # Initialise
    args = parse_args()
    target_date = args.scroll_to_date
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

    # Load
    load_data(cleaned_data, db_connection)



if __name__ == "__main__":
    lambda_handler()
    