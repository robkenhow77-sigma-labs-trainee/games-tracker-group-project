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
        "age_rating": "PEGI 16",
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
        "publisher": ["sigma"],
        "release_date": datetime.now(),
        "game_image": "random",
        "is_nsfw": True,
        "age_rating": "PEGI 18",
        "platform": "GOG",
        "score": 10,
        "price": 20,
        "discount": 0
        }]
    
    #     {title: x,
    # genres: [x, y, z],
    # publisher: [x, y, z],
    # developer: [x, y, z],
    # tag: [x, y, z],
    # platform_score: x,
    # platform_price: x,
    # platform_discount: x,
    # release_date: x,
    # game_image: x,
    # age_rating: x
    # }

    # Data to be loaded from db
    # game titles and ids, tag and id, dev and id, pub and id and genre and id
    game_titles_and_ids = lf.make_id_mapping(lf.get_game_ids(connection), 'game')
    tags_and_ids = lf.make_id_mapping(lf.get_tag_ids(connection), 'tag')
    devs_and_ids = lf.make_id_mapping(lf.get_developer_ids(connection), 'developer')
    pubs_and_ids = lf.make_id_mapping(lf.get_publisher_ids(connection), 'publisher')
    genres_and_ids = lf.make_id_mapping(lf.get_genre_ids(connection), 'genre')
    # return example: {'treyarch': 1}

    # Load known values: game titles and ids, tag and id, dev and id, pub and id and genre and id
    # New values that don't exist in the DB
    new_games = lf.get_games_for_upload(new_games_example, game_titles_and_ids)
    new_tags = lf.get_items_for_upload('tag', new_games_example, tags_and_ids)
    new_devs = lf.get_items_for_upload('developer', new_games_example, devs_and_ids)
    new_pubs = lf.get_items_for_upload('publisher', new_games_example, pubs_and_ids)
    new_genres = lf.get_items_for_upload('genre', new_games_example, genres_and_ids)

    # Game table must be formatted differently
    age_rating_map = lf.make_id_mapping(lf.get_age_rating_mapping(connection), "age_rating")
    new_games = lf.format_games_for_upload(new_games, age_rating_map)

    # Upload tables and return values
    new_game_titles_and_ids = lf.make_id_mapping(lf.upload_and_return_games(new_games, connection), 'game')
    new_tags_and_ids = lf.make_id_mapping(lf.upload_and_return_tags(new_tags, connection), 'tag')
    new_devs_and_ids = lf.make_id_mapping(lf.upload_and_return_devs(new_devs, connection), 'developer')
    new_pubs_and_ids = lf.make_id_mapping(lf.upload_and_return_pubs(new_pubs, connection), 'publisher')
    new_genres_and_ids = lf.make_id_mapping(lf.upload_and_return_genres(new_genres, connection), 'genre')


    # Update names and ids with the new ones
    game_titles_and_ids.update(new_game_titles_and_ids)
    tags_and_ids.update(new_tags_and_ids)
    devs_and_ids.update(new_devs_and_ids)
    pubs_and_ids.update(new_pubs_and_ids)
    genres_and_ids.update(new_genres_and_ids)


    # Update game_publisher_assignment, game_developer_assignment
    current_game_developer_assignments = lf.get_developer_game_assignments(connection)
    current_game_publisher_assignments = lf.get_publisher_game_assignments(connection)
    current_game_dev_tuples = lf.make_current_assignment_tuples(current_game_developer_assignments, 'developer_id')
    current_game_pub_tuples = lf.make_current_assignment_tuples(current_game_publisher_assignments, 'publisher_id')

    game_dev_assignments = lf.assign_developers(new_games_example, game_titles_and_ids, devs_and_ids, current_game_dev_tuples)
    game_pub_assignments = lf.assign_publishers(new_games_example, game_titles_and_ids, pubs_and_ids, current_game_pub_tuples)

    lf.upload_developer_assignment(game_dev_assignments, connection)
    lf.upload_publisher_assignment(game_pub_assignments, connection)

    # Game_platform assignment
    current_game_platform_assignments = lf.get_game_platform_assignments(connection)
    platform_mapping = lf.make_id_mapping(lf.get_platform_mapping(connection), 'platform')
    current_game_platform_tuples = lf.make_current_assignment_tuples(current_game_platform_assignments, 'platform_id')
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
    current_genre_game_platform_tuples = [(game["genre_id"], game['platform_assignment_id']) for game in genre_game_platform_assignment]
    current_tag_game_platform_tuples = [(game["tag_id"], game['platform_assignment_id']) for game in tag_game_platform_assignment]

    # make proposed tuples
    new_genre_game_platform_tuples = lf.assign_genre_game_platform(new_games_example, game_titles_and_ids, platform_mapping, genres_and_ids, current_game_platform_assignments, current_genre_game_platform_tuples)
    new_tag_game_platform_tuples = lf.assign_tag_game_platform(new_games_example, game_titles_and_ids, platform_mapping, tags_and_ids, current_game_platform_assignments, current_tag_game_platform_tuples)

    # upload if not in proposed
    lf.upload_genre_game_platform_assignment(new_genre_game_platform_tuples, connection)
    lf.upload_tag_game_platform_assignment(new_tag_game_platform_tuples, connection)

    # NEED TO MAP AGE!!!
    # ANYTHING THAT COULD BE A LIST SHOULD BE EVEN IF ONLY ONE ENTRY, THEN REMOVE ANY ISISNTANCE LIST ...
    # CHECK EVERYTHING WORKS


    connection.close()
