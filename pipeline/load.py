"""A python script to load game data to the database"""

# Native imports
from os import environ as ENV

# Third-party imports 
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports

def get_ids(table_name: str, conn: psycopg.Connection):
    if table_name not in ["tag", "genre", "developer", "publisher", "game"]:
        raise ValueError("Invalid table")
    """Simple query function"""
    query = f"""
        SELECT * FROM {table_name};
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query)
        return cur.fetchall()


def check_existing(new: list[str], current: list[str]):
    """Checks the new list to find any strings not in the current list. 
    Eg. new tags that aren't already in the database"""
    return [word for word in new if word not in current]


def upload_values(conn: psycopg.Connection, values: list[tuple], table_name: str) -> None:
    sql = f"""
    INSERT INTO {table_name}
    VALUES (%)
    """
    with conn.cursor() as cur:
        cur.executemany(sql, values)
        conn.commit()


def get_new_items(item: str, games: list[dict]) -> list[str]:
    """Gets the specified item from each dictionary
    Eg. get all the game titles
    """
    items = []
    for game in games:
        value = game[item]
        if isinstance(value, str):
            items.append(value)
        else:
            for item in value:
                items.append(value)
    return items



if __name__ == "__main__":
    load_dotenv()
    conn_string = f"postgresql://{ENV['DB_USERNAME']}:{ENV["DB_PASSWORD"]}@{ENV["DB_HOST"]}:{ENV["DB_PORT"]}/{ENV["DB_NAME"]}"
    connection = psycopg.connect(conn_string)
    
    new_games_example = {}

    tag_ids = get_ids("tag", connection)
    genre_ids = get_ids("genre", connection)
    developer_ids = get_ids("developer", connection)
    publisher_ids = get_ids("publisher", connection)
    game_ids = get_ids("game", connection)

    new_tags = get_new_items(tag_ids.keys(), new_games_example)

    
