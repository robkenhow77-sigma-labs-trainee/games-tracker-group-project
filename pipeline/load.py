"""A python script to load game data to the database"""

# Native imports
from os import environ as ENV
from datetime import datetime

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


def get_games_for_upload(new_games: list[dict], current_games: dict):
    """Gets a set of current games, 
    then gets a set of games that have been scraped and cleaned, 
    then gets any game names that are in the scraped games and not in the database,
    then adds the dictionaries of ga,es not in the databases."""
    current_games = set(current_games.keys())
    new_game_names = set(game["game_name"] for game in new_games)
    games_to_upload = [game for game in new_game_names if game not in current_games]
    return [game for game in new_games if game["game_name"] in games_to_upload]
    

def format_games_for_upload(games: list[dict]):
    """Returns the tuples to be uploaded"""
    age_map = {
        "":""
    }
    games_for_upload = []
    for game in games:
        games_for_upload.append((
            game["game_name"],
            game["release_date"],
            game["game_image"],
            game["age_rating_id"], # NEED TO MAP
            game["is_nsfw"]
        ))

    return games_for_upload


def pub_or_dev_game_assignment(game_ids: dict, pub_or_dev_ids: dict) -> list[tuple]:
    """Returns a list of tuples for uploading to the database"""
    assignments = []
    for game_id in game_ids.values():
        for pub_dev_id in pub_or_dev_ids.values():
            assignments.append((game_id, pub_dev_id))
    return assignments


# Game_platform_assignment
# Check if the game exists on all 3 platforms
def make_current_assignment_tuples(current_assignments: list[dict], dev_or_pub_or_platform: str):
    return [(game["game_id"], game[dev_or_pub_or_platform]) for game in current_assignments]


def get_game_platform_assignment_counts(conn: psycopg.Connection):
    """Gets the game assignment table"""
    query = """
        SELECT game_id, COUNT(platform_id) 
        FROM game_platform_assignment
        GROUP BY game_id;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


if __name__ == "__main__":
    # initialise
    load_dotenv()
    conn_string = f"postgresql://{ENV['DB_USERNAME']}:{ENV["DB_PASSWORD"]}@{ENV["DB_HOST"]}:{ENV["DB_PORT"]}/{ENV["DB_NAME"]}"
    connection = psycopg.connect(conn_string, row_factory=dict_row)

    new_games_example = [{
        "game_name": "fortnite",
        "developer": ["treyarch", 'epic', 'some other dev'],
        "tag": ["action"],
        "genre": ["mystic"],
        "publisher": ["sigma", "activision"],
        "release_date": datetime.now(),
        "game_image": "random",
        "is_nsfw": True,
        "age_rating_id": 18,
        "platform": "Steam",
        "score": 90,
        "price": 20000,
        "discount": 99
        },
        {
        "game_name": "rocket league",
        "developer": "EA",
        "tag": ["action", "racing"],
        "genre": ["mystic", "horror"],
        "publisher": "sigma",
        "release_date": datetime.now(),
        "game_image": "random",
        "is_nsfw": True,
        "age_rating_id": 18,
        "platform": "GOG",
        "score": 10,
        "price": 20,
        "discount": 0
        }]

    # Data to be loaded from db
    # game titles and ids, tag and id, dev and id, pub and id and genre and id
    game_titles_and_ids = make_id_mapping(lf.get_game_ids(connection), 'game')
    tags_and_ids = make_id_mapping(lf.get_tag_ids(connection), 'tag')
    devs_and_ids = make_id_mapping(lf.get_developer_ids(connection), 'developer')
    pubs_and_ids = make_id_mapping(lf.get_publisher_ids(connection), 'publisher')
    genres_and_ids = make_id_mapping(lf.get_genre_ids(connection), 'genre')
    # return example: {'treyarch': 1}

    # Load known values: game titles and ids, tag and id, dev and id, pub and id and genre and id
    # New values that don't exist in the DB
    new_games = get_games_for_upload(new_games_example, game_titles_and_ids)
    new_tags = get_items_for_upload('tag', new_games_example, tags_and_ids)
    new_devs = get_items_for_upload('developer', new_games_example, devs_and_ids)
    new_pubs = get_items_for_upload('publisher', new_games_example, pubs_and_ids)
    new_genres = get_items_for_upload('genre', new_games_example, genres_and_ids)

    # Game table must be formatted differently
    new_games = format_games_for_upload(new_games)

    # Upload tables and return values
    new_game_titles_and_ids = make_id_mapping(lf.upload_and_return_games(new_games, connection), 'game')
    new_tags_and_ids = make_id_mapping(lf.upload_and_return_tags(new_tags, connection), 'tag')
    new_devs_and_ids = make_id_mapping(lf.upload_and_return_devs(new_devs, connection), 'developer')
    new_pubs_and_ids = make_id_mapping(lf.upload_and_return_pubs(new_pubs, connection), 'publisher')
    new_genres_and_ids = make_id_mapping(lf.upload_and_return_genres(new_genres, connection), 'genre')


    # Update names and ids with the new ones
    game_titles_and_ids.update(new_game_titles_and_ids)
    tags_and_ids.update(new_tags_and_ids)
    devs_and_ids.update(new_devs_and_ids)
    pubs_and_ids.update(new_pubs_and_ids)
    genres_and_ids.update(new_genres_and_ids)


    # Update game_publisher_assignment, game_developer_assignment
    current_game_developer_assignments = lf.get_developer_game_assignments(connection)
    current_game_publisher_assignments = lf.get_publisher_game_assignments(connection)
    current_game_dev_tuples = make_current_assignment_tuples(current_game_developer_assignments, 'developer_id')
    current_game_pub_tuples = make_current_assignment_tuples(current_game_publisher_assignments, 'publisher_id')

    game_dev_assignments = lf.assign_developers(new_games_example, game_titles_and_ids, devs_and_ids, current_game_dev_tuples)
    game_pub_assignments = lf.assign_publishers(new_games_example, game_titles_and_ids, pubs_and_ids, current_game_pub_tuples)

    lf.upload_developer_assignment(game_dev_assignments, connection)
    lf.upload_publisher_assignment(game_pub_assignments, connection)

    # Game_platform assignment
    current_game_platform_assignments = lf.get_game_platform_assignments(connection)
    platform_mapping = make_id_mapping(lf.get_platform_mapping(connection), 'platform')
    current_game_platform_tuples = make_current_assignment_tuples(current_game_platform_assignments, 'platform_id')
    game_platform_tuples = lf.assign_game_platform(new_games_example, game_titles_and_ids, platform_mapping, current_game_platform_tuples)    
    new_game_platform_assignments = lf.upload_and_return_game_platform_assignment(game_platform_tuples, connection)
    
    current_game_platform_assignments =  {str((row['game_id'], row["platform_id"])): row['platform_assignment_id'] for row in current_game_platform_assignments}
    new_game_platform_assignments =  {str((row['game_id'], row["platform_id"])): row['platform_assignment_id'] for row in new_game_platform_assignments}
    current_game_platform_assignments.update(new_game_platform_assignments)

    # Game_genre_platform_assignment & tag_game_platform_assignment
    # Get current tables
    genre_game_platform_assignment = lf.get_genre_game_platform_assignment(connection)
    tag_game_platform_assignment = lf.get_tag_game_platform_assignment(connection)

    # get mapping for genre_name: genre_id anf tag_name: tag_id
    genre_game_platform_mapping = {row['platform_assignment_id']: row['genre_id'] for row in genre_game_platform_assignment}
    tag_game_platform_mapping = {row['platform_assignment_id']: row['tag_id'] for row in tag_game_platform_assignment}

    # make current tuples
    current_genre_game_platform_tuples = [(game["genre_id"], game['platform_assignment_id']) for game in genre_game_platform_mapping]
    current_tag_game_platform_tuples = [(game["tag_id"], game['platform_assignment_id']) for game in tag_game_platform_mapping]

    # make proposed tuples
    new_genre_game_platform_tuples = lf.assign_genre_game_platform(new_games_example, game_titles_and_ids, platform_mapping, genres_and_ids, current_game_platform_assignments, current_genre_game_platform_tuples)
    new_tag_game_platform_tuples = lf.assign_tag_game_platform(new_games_example, game_titles_and_ids, platform_mapping, tags_and_ids, current_game_platform_assignments, current_tag_game_platform_tuples)
    print(new_genre_game_platform_tuples)
    print(new_tag_game_platform_tuples)

    # upload if not in proposed
    lf.upload_genre_game_platform_assignment(new_genre_game_platform_tuples, connection)
    lf.upload_tag_game_platform_assignment(new_tag_game_platform_tuples, connection)

    # NEED TO MAP AGE!!!
    # ANYTHING THAT COULD BE A LIST SHOULD BE EVEN IF ONLY ONE ENTRY, THEN REMOVE ANY ISISNTANCE LIST ...
    # CHECK EVERYTHING WORKS


    connection.close()
