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


def make_id_mapping(ids_and_items: list[dict], item: str):
    """Creates a dictionary in the form item: id"""
    return {id_and_item[f'{item}_name']: id_and_item[f'{item}_id'] for id_and_item in ids_and_items}


def get_items_not_in_current(new: list[str], current: list[str]):
    """Checks the new list to find any strings not in the current list. 
    Eg. new tags that aren't already in the database"""
    return [word for word in new if word not in current]


def get_new_items_list(item: str, games_list_dict: list[dict]) -> list[str]:
    """Gets the specified item from each dictionary
    Eg. get all the game titles
    """
    items = []
    for game in games_list_dict:
        value = game[item]
        if isinstance(value, str):
            items.append(value)
        else:
            for val in value:
                items.append(val)
    return items


# Get devs, pubs, tags, genres and games for upload
def get_items_for_upload(table: str, new_games: list[dict], conn: psycopg.Connection):
    """Gets all the new genres for uploading to the database"""
    ids = get_ids(table, conn)
    current = make_id_mapping(ids, table)
    new = get_new_items_list(table, new_games)
    return  get_items_not_in_current(new, current.keys())


# Dev_assignment, pub_assignment
# Need game id and corresponding pub/dev ids
def get_new_game_ids(table: str, new_games: list[dict], conn: psycopg.Connection):
    items_for_upload = get_items_for_upload(table, new_games, conn)
    ids = get_ids(table, conn)
    max_id = max([game[f"{table}_id"] for game in ids])
    return assign_new_ids(items_for_upload, max_id)


def assign_new_ids(new_games: list[str], max_game_id: int) -> dict:
    """assigns an id based on the current db max_id"""
    return {game: max_game_id + i for i, game in enumerate(new_games, 1)}


def pub_or_dev_game_assignment(game_ids: dict, pub_or_dev_ids: dict) -> list[tuple]:
    """Returns a list of tuples for uploading to the database"""
    assignments = []
    for game_id in game_ids.values():
        for pub_dev_id in pub_or_dev_ids.values():
            assignments.append((game_id, pub_dev_id))
    return assignments



if __name__ == "__main__":
    load_dotenv()
    conn_string = f"postgresql://{ENV['DB_USERNAME']}:{ENV["DB_PASSWORD"]}@{ENV["DB_HOST"]}:{ENV["DB_PORT"]}/{ENV["DB_NAME"]}"
    connection = psycopg.connect(conn_string)
    
    new_games_example = [{
        "game": "fortnite",
        "developer": ["treyarch", 'epic', 'goat'],
        "tag": ["action"],
        "genre": "mystic",
        "publisher": "sigma"
        }]

    get_new_game_ids()


    new_game_ids = get_new_game_ids('game', new_games_example, connection)
    print(new_game_ids)

    # print(pub_or_dev_game_assignment(new_game_ids, new_developer_ids))


    connection.close()