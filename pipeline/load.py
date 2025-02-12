"""A python script to load game data to the database"""

# Native imports
from os import environ as ENV

# Third-party imports 
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
import load_functions as lf


def make_id_mapping(ids_and_items: list[dict], item: str):
    """Creates a dictionary in the form item: id"""
    return {id_and_item[f'{item}_name']: id_and_item[f'{item}_id'] for id_and_item in ids_and_items}


def get_new_items_set(item: str, games_list_dict: list[dict]) -> list[str]:
    """Gets the specified item from each dictionary
    Eg. get all the game titles
    """
    items = set()
    for game in games_list_dict:
        value = game[item]
        if isinstance(value, str):
            items.add(value)
        else:
            for val in value:
                items.add(val)
    return items


def get_items_not_in_current(new: list[str], current: list[str]):
    """Checks the new list to find any strings not in the current list. 
    Eg. new tags that aren't already in the database"""
    return [word for word in new if word not in current]


def get_games_if_on_all_platforms(game_platform_assignments: list[dict]):
    """Checks to see if the game exists on all platforms"""
    game_ids = [str(game["game_id"]) for game in game_platform_assignments]
    game_ids_on_all = []
    for id in game_ids:
        if game_ids.count(id) == 3:
            game_ids_on_all.append(id)
    return game_ids_on_all


# Get devs, pubs, tags, genres and games for upload
def get_items_for_upload(table: str, new_games: list[dict], current_items: dict):
    """Gets all the new genres for uploading to the database"""
    new = get_new_items_set(table, new_games)
    items_for_upload = get_items_not_in_current(new, current_items.keys())
    return [(item,) for item in items_for_upload]





# Dev_assignment, pub_assignment
def get_new_item_ids(table: str, new_games: list[dict], conn: psycopg.Connection):
    """Gets the ids that the items will have when they get uploaded to the database"""
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


# Game_platform_assignment
# Check if the game exists on all 3 platforms
def get_game_assignments(conn: psycopg.Connection):
    """Gets the game assignment table"""
    query = """
        SELECT game_id, COUNT(platform_id) 
        FROM game_platform_assignment
        GROUP BY game_id;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def make_game_platform_assignment_data(new_games: list[dict], conn: psycopg.Connection):
    new_game_ids = get_new_item_ids('game', new_games, conn)
    current_game_ids = make_id_mapping(get_ids('game', conn), 'game')
    current_game_ids.update(new_game_ids)
    latest_game_ids = current_game_ids
    latest_game_ids


if __name__ == "__main__":
    # initialise
    load_dotenv()
    conn_string = f"postgresql://{ENV['DB_USERNAME']}:{ENV["DB_PASSWORD"]}@{ENV["DB_HOST"]}:{ENV["DB_PORT"]}/{ENV["DB_NAME"]}"
    connection = psycopg.connect(conn_string, row_factory=dict_row)

    new_games_example = [{
        "game": "fortnite",
        "developer": ["treyarch", 'epic', 'some other dev'],
        "tag": ["action"],
        "genre": "mystic",
        "publisher": "sigma"
        },{
        "game": "rocket league",
        "developer": "EA",
        "tag": ["action", "racing"],
        "genre": ["mystic", "horror"],
        "publisher": "sigma"
        }]

    # Data to be loaded from db
    # game titles and ids, tag and id, dev and id, pub and id and genre and id
    game_titles_and_ids = make_id_mapping(get_ids('game', connection), 'game')
    tags_and_ids = make_id_mapping(get_ids('tag', connection), 'tag')
    devs_and_ids = make_id_mapping(get_ids('developer', connection), 'developer')
    pubs_and_ids = make_id_mapping(get_ids('publisher', connection), 'publisher')
    genres_and_ids = make_id_mapping(get_ids('genre', connection), 'genre')
    # return example: {'treyarch': 1}

    # Get the game platform assignments
    sql = """
    SELECT game_id, platform_id
    FROM game_platform_assignment
    """
    with connection.cursor() as cur:
        cur.execute(sql)
        game_and_platform_ids = cur.fetchall()
    
    # Get any games on all platforms
    game_ids_on_all_platforms = get_games_if_on_all_platforms(game_and_platform_ids)

    # Get new tags, games, publishers, developers and genres
    devs = get_items_for_upload('developer', new_games_example, devs_and_ids)
    print(devs)
    
    


    connection.close()
