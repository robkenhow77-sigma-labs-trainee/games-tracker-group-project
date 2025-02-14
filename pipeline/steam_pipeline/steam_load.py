"""A python script to load game data to the database"""

# Native imports
from os import environ as ENV
from datetime import datetime

# Third-party imports
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Local imports
import steam_pipeline.steam_load_functions as lf


def load_data(new_games_transformed: list[dict], connection: psycopg.Connection):
# LOAD STEP 1: Update the game, tag, developer, publisher and genre tables
    # Get the current tables and make a mapping of {name: id}
    game_titles_and_ids = lf.make_id_mapping(lf.get_game_ids(connection), 'game')
    tags_and_ids = lf.make_id_mapping(lf.get_tag_ids(connection), 'tag')
    devs_and_ids = lf.make_id_mapping(lf.get_developer_ids(connection), 'developer')
    pubs_and_ids = lf.make_id_mapping(lf.get_publisher_ids(connection), 'publisher')
    genres_and_ids = lf.make_id_mapping(lf.get_genre_ids(connection), 'genre')


    # Gets a list of games, tags, developers, publishers and genres
    # that are not in the database, and need to be uploaded
    new_games = lf.get_games_for_upload(new_games_transformed, game_titles_and_ids)
    new_tags = lf.get_items_for_upload('tag', new_games_transformed, tags_and_ids)
    new_devs = lf.get_items_for_upload('developer', new_games_transformed, devs_and_ids)
    new_pubs = lf.get_items_for_upload('publisher', new_games_transformed, pubs_and_ids)
    new_genres = lf.get_items_for_upload('genre', new_games_transformed, genres_and_ids)

    # Game table must be formatted differently as it has more than just name and id
    age_rating_map = lf.make_id_mapping(lf.get_age_rating_mapping(connection), "age_rating")
    new_games = lf.format_games_for_upload(new_games, age_rating_map)

    # Upload games, tags, developers, publishers and genres and return their new ids
    new_game_titles_and_ids = lf.make_id_mapping(
        lf.upload_and_return_games(new_games, connection), 'game')
    new_tags_and_ids = lf.make_id_mapping(
        lf.upload_and_return_tags(new_tags, connection), 'tag')
    new_devs_and_ids = lf.make_id_mapping(
        lf.upload_and_return_devs(new_devs, connection), 'developer')
    new_pubs_and_ids = lf.make_id_mapping(
        lf.upload_and_return_pubs(new_pubs, connection), 'publisher')
    new_genres_and_ids = lf.make_id_mapping(
        lf.upload_and_return_genres(new_genres, connection), 'genre')

    # Update names and ids with the new ones
    game_titles_and_ids.update(new_game_titles_and_ids)
    tags_and_ids.update(new_tags_and_ids)
    devs_and_ids.update(new_devs_and_ids)
    pubs_and_ids.update(new_pubs_and_ids)
    genres_and_ids.update(new_genres_and_ids)


    # LOAD STEP 2: Update the game_publisher_assignment,
    # game_developer_assignment and game_platform assignment
    # Get the current tables and makes them into tuples of
    # (game_id, pub/dev id) to check for duplicates
    current_game_developer_assignments = lf.get_developer_game_assignments(connection)
    current_game_publisher_assignments = lf.get_publisher_game_assignments(connection)
    current_game_dev_tuples = lf.make_current_dev_or_pub_game_assignment_tuples(
        current_game_developer_assignments, 'developer_id')
    current_game_pub_tuples = lf.make_current_dev_or_pub_game_assignment_tuples(
        current_game_publisher_assignments, 'publisher_id')

    # Formats the game_publisher_assignments and game_developer_assignments for upload
    game_dev_assignments = lf.assign_developers(
        new_games_transformed, game_titles_and_ids, devs_and_ids, current_game_dev_tuples)
    game_pub_assignments = lf.assign_publishers(
        new_games_transformed, game_titles_and_ids, pubs_and_ids, current_game_pub_tuples)

    # Uploads the game_publisher_assignments and game_developer_assignments
    lf.upload_developer_game_assignment(game_dev_assignments, connection)
    lf.upload_publisher_game_assignment(game_pub_assignments, connection)

    # Get the current game_platform_assignments
    current_game_platform_assignments = lf.get_game_platform_assignments(connection)

    # Get the platform names and ids
    platform_mapping = lf.make_id_mapping(lf.get_platform_ids(connection), 'platform')

    # Get the current game_platform tuples
    current_game_platform_tuples = lf.make_current_game_platform_assignment_tuples(
        current_game_platform_assignments, 'platform_id')

    # Gets the new game_platform assignments that aren't in the database, to be uploaded
    game_platform_tuples = lf.assign_game_platform(new_games_transformed,
        game_titles_and_ids, platform_mapping, current_game_platform_tuples)
    # Upload the game_platform_assignments and return the new ids
    new_game_platform_assignments = lf.upload_and_return_game_platform_assignment(
        game_platform_tuples, connection)

    # Creates a mapping in the form {(game_id, platform_id): game_assignment_id}
    # This is because in order to update the genre/tag_game_platform_assignments you
    # need to be able to go from the raw game name and platform name
    # to the game_platform_assignment and them match with the genre/tag
    current_game_platform_assignments =  {
        str((row['game_id'], row["platform_id"])): row['platform_assignment_id']
        for row in current_game_platform_assignments}
    new_game_platform_assignments =  {
        str((row['game_id'], row["platform_id"])): row['platform_assignment_id']
        for row in new_game_platform_assignments}
    current_game_platform_assignments.update(new_game_platform_assignments)


    # LOAD STEP 3: Update the genre_game_platform_assignment and tag_game_platform_assignment
    genre_game_platform_assignment = lf.get_genre_game_platform_assignment(connection)
    tag_game_platform_assignment = lf.get_tag_game_platform_assignment(connection)

    # Get mapping for genre_name: genre_id and tag_name: tag_id
    genre_game_platform_mapping = {
        row['platform_assignment_id']: row['genre_id'] for row in genre_game_platform_assignment}
    tag_game_platform_mapping = {
        row['platform_assignment_id']: row['tag_id'] for row in tag_game_platform_assignment}

    # Make tuples of the existing genre/tag_ids and platform_assignment_ids
    current_genre_game_platform_tuples = [(game["genre_id"],
        game['platform_assignment_id']) for game in genre_game_platform_assignment]
    current_tag_game_platform_tuples = [(game["tag_id"],
        game['platform_assignment_id']) for game in tag_game_platform_assignment]

    # Get the new tuples of (genre/tag, game_platform_assignment_id) be uploaded to the database
    new_genre_game_platform_tuples = lf.assign_genre_game_platform(new_games_transformed,
            game_titles_and_ids, platform_mapping, genres_and_ids,
            current_game_platform_assignments, current_genre_game_platform_tuples)
    new_tag_game_platform_tuples = lf.assign_tag_game_platform(new_games_transformed,
            game_titles_and_ids, platform_mapping, tags_and_ids,
            current_game_platform_assignments, current_tag_game_platform_tuples)

    # Upload the tag/genre_game_platform_assignments
    lf.upload_genre_game_platform_assignment(new_genre_game_platform_tuples, connection)
    lf.upload_tag_game_platform_assignment(new_tag_game_platform_tuples, connection)

    # Close the connection to the database
    connection.close()  # pylint: disable=no-member


if __name__ == "__main__":
    # initialise
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    CONN_STRING = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    db_connection = psycopg.connect(CONN_STRING, row_factory=dict_row)

    NEW_GAMES_EXAMPLE = [{
        "game_name": "BO3",
        "developer": ["treyarch", 'epic', 'some other dev', "someone"],
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


    load_data(NEW_GAMES_EXAMPLE, db_connection)
