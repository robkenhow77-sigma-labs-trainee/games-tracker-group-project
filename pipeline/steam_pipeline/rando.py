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
conn = psycopg.connect(conn_string, row_factory=dict_row)

with conn.cursor() as cur:
    sql = """
    SELECT *
    FROM developer_game_assignment
    WHERE game_id = 1000000;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        print(cur.fetchall())