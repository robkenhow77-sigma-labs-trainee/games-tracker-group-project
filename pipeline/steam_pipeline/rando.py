from os import environ as ENV
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import steam_load_functions as lf

load_dotenv()
user = ENV['DB_USERNAME']
password = ENV["DB_PASSWORD"]
host = ENV["DB_HOST"]
port = ENV["DB_PORT"]
name = ENV["DB_NAME"]
conn_string = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
db_connection = psycopg.connect(conn_string, row_factory=dict_row)

lf.upload_and_return_devs([("x", "y")], db_connection)