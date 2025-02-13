"""A script to run the entire steam pipeline"""

# Native imports
from os import environ as ENV

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
from extract_steam import scrape_newest
from transform import clean_data


def lambda_handler(event=None, context=None):
    # Initialise
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    CONN_STRING = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    connection = psycopg.connect(CONN_STRING, row_factory=dict_row)

    # Extract
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&supportedlang=english&ndl=1"
    target_date = ""
    scraped_data = scrape_newest(url, )









if __name__ == "__main__":
    lambda_handler
    