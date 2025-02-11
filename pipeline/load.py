"""A python script to load game data to the database"""

# Native imports
from os import environ as ENV

# Third-party imports 
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports

def query_sql(sql: str, conn: psycopg.Connection):
    """Simple query function"""
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql)
        return cur.fetchall()


def upload_many(sql: str, values: list[tuple], conn: psycopg.Connection) -> None:
    """Simple upload function for uploading many values"""
    with conn.cursor() as cur:
        cur.executemany(sql, values)
        conn.commit()


def get_tag_ids(conn: psycopg.Connection) -> dict:
    """Gets the tag ids and tag names"""
    query = """
        SELECT * FROM tag;
    """
    return query_sql(query, conn)


def get_genre_ids(conn: psycopg.Connection) -> dict:
    """Gets the genre ids and genre names"""
    query = """
        SELECT * FROM tag;
    """
    return query_sql(query, conn)


def get_developer_ids(conn: psycopg.Connection) -> dict:
    """Gets the developer ids and developer names"""
    query = """
        SELECT * FROM tag;
    """
    return query_sql(query, conn)


def get_publisher_ids(conn: psycopg.Connection) -> dict:
    """Gets the publisher ids and publisher names"""
    query = """
        SELECT * FROM tag;
    """
    return query_sql(query, conn)


def get_game_ids(conn: psycopg.Connection) -> dict:
    """Gets the game ids and game names"""
    query = """
        SELECT * FROM tag;
    """
    return query_sql(query, conn)


def check_existing(new: list[str], current: list[str]):
    """Checks the new list to find any strings not in the current list. 
    Eg. new tags that aren't already in the database"""
    return [word for word in new if word not in current]


def upload_tags(conn: psycopg.Connection, tags: list[tuple]) -> None:
    sql = """
    INSERT INTO tag
    VALUES (%)
    """
    upload_many(sql, tags, conn)


def upload_genres(conn: psycopg.Connection, genres: list[tuple]) -> None:
    sql = """
    INSERT INTO genre
    VALUES (%)
    """
    upload_many(sql, genres, conn)


def upload_developers(conn: psycopg.Connection, developers: list[tuple]) -> None:
    sql = """
    INSERT INTO developer
    VALUES (%)
    """
    upload_many(sql, developers, conn)


def upload_publishers(conn: psycopg.Connection, publishers: list[tuple]) -> None:
    sql = """
    INSERT INTO publisher
    VALUES (%)
    """
    upload_many(sql, publishers, conn)


def upload_games(conn: psycopg.Connection, games: list[tuple]) -> None:
    sql = """
    INSERT INTO game
    VALUES (%)
    """
    upload_many(sql, games, conn)


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
    
    tag_ids = get_tag_ids(connection)
    genre_ids = get_genre_ids(connection)
    developer_ids = get_developer_ids(connection)
    publisher_ids = get_publisher_ids(connection)
    game_ids = get_game_ids(connection)

    new_tags = 
    
