"""Useful functions for load"""
# Native imports
import logging

# Third-party imports
import psycopg


def get_game_ids(conn: psycopg.Connection) -> list[dict]:
    """Gets the game name and ids"""
    query = "SELECT * FROM game;"
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_publisher_ids(conn: psycopg.Connection) -> list[dict]:
    """Gets the publisher names and ids"""
    query = "SELECT * FROM publisher;"
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_developer_ids(conn: psycopg.Connection) -> list[dict]:
    """Gets the developer names and ids"""
    query = "SELECT * FROM developer;"
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_tag_ids(conn: psycopg.Connection) -> list[dict]:
    """Gets the tag names and ids"""
    query = "SELECT * FROM tag;"
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_genre_ids(conn: psycopg.Connection) -> list[dict]:
    """Gets the genre names and ids"""
    query = "SELECT * FROM genre;"
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_age_rating_mapping(conn: psycopg.Connection) -> list[dict]:
    """Gets the age_ratings and ids"""
    query = " SELECT * FROM age_rating;"
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def upload_and_return_devs(devs: list[tuple], conn: psycopg.Connection) -> dict:
    """Uploads the new developers and returns their names and ids"""
    if len(devs) == 0:
        logging.info("No new developers to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO developer (developer_name)
                            VALUES (%s) RETURNING *""", devs, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            logging.info("Successfully loaded developers")
            return ids

    except psycopg.Error as e:
        logging.error(f"Uploading developers failed: {e}. Data to be uploaded: {devs}")
        return {}


def upload_and_return_games(games: list[tuple], conn: psycopg.Connection) -> dict:
    """Uploads the new games and returns their names and ids"""
    if len(games) == 0:
        logging.info("No new games to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO game (game_name, game_image, age_rating_id, is_nsfw)
                VALUES (%s, %s, %s, %s) RETURNING game_id, game_name""", games, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            logging.info("Successfully loaded games")
            return ids

    except psycopg.Error as e:
        logging.error(f"Uploading games failed: {e}. Data to be uploaded: {games}")
        return {}


def upload_and_return_pubs(pubs: list[tuple], conn: psycopg.Connection) -> dict:
    """Uploads the new publishers and returns their names and ids"""
    if len(pubs) == 0:
        logging.info("No new publishers to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO publisher (publisher_name)
                            VALUES (%s) RETURNING *""", pubs, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            logging.info("Successfully loaded publishers")
            return ids

    except psycopg.Error as e:
        logging.error(f"Uploading publishers failed: {e}. Data to be uploaded: {pubs}")
        return {}


def upload_and_return_genres(genres: list[tuple], conn: psycopg.Connection) -> dict:
    """Uploads the new genres and returns their names and ids"""
    if len(genres) == 0:
        logging.info("No new genres to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO genre (genre_name)
                            VALUES (%s) RETURNING *""", genres, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            logging.info("Successfully loaded genres")
            return ids

    except psycopg.Error as e:
        logging.error(f"Uploading genres failed: {e}. Data to be uploaded: {genres}")
        return {}


def upload_and_return_tags(tags: list[tuple], conn: psycopg.Connection) -> dict:
    """Uploads the new tags and returns their names and ids"""
    if len(tags) == 0:
        logging.info("No new tags to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO tag (tag_name)
                VALUES (%s) RETURNING *""", tags, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            logging.info("Successfully loaded tags")
            return ids

    except psycopg.Error as e:
        logging.error(f"Uploading tags failed: {e}. Data to be uploaded: {tags}")
        return {}


def get_game_platform_assignments(conn: psycopg.Connection) -> list[dict]:
    """Gets the game_platform_assignment_ids, game_id and platform_id"""
    sql = """
    SELECT platform_assignment_id, game_id, platform_id
    FROM game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_publishers(new_games_list: list[dict],
    game_id_mapping: dict, publisher_mapping, current: list[tuple]) -> list[str]:
    """Maps the publisher names to their ids, maps the game names to their ids.
    Returns a list of tuples in the form (game_id, publisher_id).
    Only the tuples not in the current publisher assignment table are returned."""
    values = []
    for game in new_games_list:
        publishers = game["publisher"]
        for publisher in publishers:
            values.append((
                game_id_mapping[game["game_name"]],
                publisher_mapping[publisher]
            ))

    return [value for value in values if value not in current]


def assign_developers(new_games_list: list[dict],
    game_id_mapping: dict, developer_mapping: dict, current: list[tuple]) -> list[str]:
    """Maps the developer names to their ids, maps the game names to their ids.
    Returns a list of tuples in the form (game_id, developer_id).
    Only the tuples not in the current developer assignment table are returned."""
    values = []
    for game in new_games_list:
        developers = game["developer"]
        for developer in developers:
            values.append((
                game_id_mapping[game["game_name"]],
                developer_mapping[developer]
            ))

    return [value for value in values if value not in current]


def upload_developer_game_assignment(data: list[tuple], conn: psycopg.Connection) -> None:
    """Uploads the new developer_game_assignments"""
    if len(data) == 0:
        logging.info("No new developer_game_assignments to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO developer_game_assignment (game_id, developer_id)
                VALUES (%s, %s)""", data)
        conn.commit()
        logging.info("Successfully loaded developer_game_assignments")

    except psycopg.Error as e:
        logging.error(f"Uploading developer_game_assignments failed: {e}. Data to be uploaded: {data}")
        return {}


def upload_publisher_game_assignment(data: list[tuple], conn: psycopg.Connection) -> None:
    """Uploads the new publisher_game_assignments"""
    if len(data) == 0:
        logging.info("No new publisher_game_assignments to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO publisher_game_assignment (game_id, publisher_id)
                VALUES (%s, %s)""", data)
            conn.commit()
            logging.info("Successfully loaded publisher_game_assignments")

    except psycopg.Error as e:
        logging.error(f"Uploading publisher_game_assignments failed: {e}. Data to be uploaded: {data}")
        return {}


def get_publisher_game_assignments(conn: psycopg.Connection) -> list[dict]:
    """Gets the publisher_game_assignments"""
    sql = """
    SELECT *
    FROM publisher_game_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_developer_game_assignments(conn: psycopg.Connection) -> list[dict]:
    """Gets the developer_game_assignments"""
    sql = """
    SELECT *
    FROM developer_game_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_platform_ids(conn: psycopg.Connection) -> list[dict]:
    """Gets the platform names and ids"""
    sql = """
    SELECT *
    FROM platform
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_game_platform(new_games_list: list[dict],
    game_id_mapping: dict, platform_mapping: dict, current: list[tuple]) -> list[tuple]:
    """Maps the game names to the ids and
    the publisher names to ids, for the game_platform_assignment table.
    Returns a list of tuples. Only the assignments that exist in the database"""
    values = []
    for game in new_games_list:
        new_assignment_tuple = (
            game_id_mapping[game["game_name"]], platform_mapping[game["platform"]]
        )
        if new_assignment_tuple not in current:
            values.append((
                game_id_mapping[game["game_name"]],
                platform_mapping[game["platform"]],
                game["score"],
                game["price"],
                game["discount"],
                game["release_date"],
                game["platform_url"]
            ))
    return values


def upload_and_return_game_platform_assignment(data: list[tuple],
    conn: psycopg.Connection) -> dict:
    """Uploads the game_platform_assignments
    and returns platform_assignment_id, game_id, platform_id"""
    if len(data) == 0:
        logging.info("No new game_platform_assignments to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""
            INSERT INTO game_platform_assignment 
                (game_id, platform_id, platform_score,
                platform_price, platform_discount, platform_release_date, 
                platform_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING platform_assignment_id, game_id, platform_id""",
            data, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            logging.info("Successfully loaded game_platform_assignments")
            return ids

    except psycopg.Error as e:
        logging.error(f"Uploading game_platform_assignments failed: {e}. Data to be uploaded: {data}")
        return {}


def get_genre_game_platform_assignment(conn: psycopg.Connection) -> list[dict]:
    """Gets the genre_game_platform_assignments"""
    sql = """
    SELECT *
    FROM genre_game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_tag_game_platform_assignment(conn: psycopg.Connection) -> list[dict]:
    """Gets the tag_game_platform_assignments"""
    sql = """
    SELECT *
    FROM tag_game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_genre_game_platform(new_games_list: list[dict], game_id_mapping: dict,
        platform_mapping: dict, genre_mapping: dict,
        game_platform_assignment_mapping: dict, current: list[tuple]) -> list[tuple]:
    """Maps the genre names to the ids and the game names and platform names
     to the game_platform_assignment_id,
    for the genre_game_platform_assignment table.
    Returns a list of tuples. Only the assignments that exist in the database"""
    values = []
    for game in new_games_list:
        game_id = game_id_mapping[game["game_name"]]
        platform_id = platform_mapping[game["platform"]]
        assignment_id = game_platform_assignment_mapping[str((game_id, platform_id))]
        # MULTIPLE GENRES
        for genre in game["genre"]:
            new_assignment_tuple = (
                genre_mapping[genre], assignment_id
            )
            if new_assignment_tuple not in current:
                values.append((
                new_assignment_tuple
                ))
    return values


def assign_tag_game_platform(new_games_list: list[dict], game_id_mapping: dict,
        platform_mapping: dict, tag_mapping: dict,
        game_platform_assignment_mapping: dict, current: list[tuple]) -> list[tuple]:
    """Maps the tag names to the ids and the game names and
    platform names to the game_platform_assignment_id,
    for the tag_game_platform_assignment table.
    Returns a list of tuples. Only the assignments that exist in the database"""
    values = []
    for game in new_games_list:
        game_id = game_id_mapping[game["game_name"]]
        platform_id = platform_mapping[game["platform"]]
        assignment_id = game_platform_assignment_mapping[str((game_id, platform_id))]

        for tag in game["tag"]:
            new_assignment_tuple = (
                tag_mapping[tag], assignment_id
            )
            if new_assignment_tuple not in current:
                values.append((
                new_assignment_tuple
                ))
    return values


def upload_genre_game_platform_assignment(data: list[tuple], conn: psycopg.Connection) -> None:
    """Uploads the genre_game_platform_assignments"""
    if len(data) == 0:
        logging.info("No new genre_game_platform_assignments to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""
            INSERT INTO genre_game_platform_assignment (genre_id, platform_assignment_id)
            VALUES (%s, %s)""", data)
            conn.commit()
            logging.info("Successfully loaded genre_game_platform_assignments")
            return None

    except psycopg.Error as e:
        logging.error(f"Uploading genre_game_platform_assignments failed: {e}. Data to be uploaded: {data}")
        return None


def upload_tag_game_platform_assignment(data: list[tuple], conn: psycopg.Connection) -> None:
    """Uploads the tag_game_platform_assignments"""
    if len(data) == 0:
        logging.info("No new tag_game_platform_assignments to upload")
        return {}

    try:
        with conn.cursor() as cur:
            cur.executemany("""
            INSERT INTO tag_game_platform_assignment (tag_id, platform_assignment_id)
            VALUES (%s, %s)""", data)
            conn.commit()
            logging.info("Successfully loaded tag_game_platform_assignments")
            return None

    except psycopg.Error as e:
        logging.error(f"Uploading tag_game_platform_assignments failed: {e}. Data to be uploaded: {data}")
        return None


def make_id_mapping(ids_and_items: list[dict], item: str) -> dict:
    """Creates a dictionary in the form {item_name: id}"""
    return {id_and_item[f'{item}_name']: id_and_item[f'{item}_id'] for id_and_item in ids_and_items}


def get_new_items_set(item: str, games_list_dict: list[dict]) -> set[str]:
    """Gets the specified item from each dictionary
    Eg. get all the game titles. Uses a set to make sure their are no duplicates
    """
    items = set()
    for game in games_list_dict:
        value = game[item]
        for val in value:
            items.add(val)
    return items


def get_items_not_in_current(new: list[str], current: list[str]) -> list[str]:
    """Checks the new list to find any strings not in the current list. 
    Eg. new tags that aren't already in the database"""
    return [word for word in new if word not in current]


def get_items_for_upload(table: str, new_games: list[dict], current_items: dict) -> list[tuple]:
    """Gets all the new items for uploading, that aren't already in the database"""
    new = get_new_items_set(table, new_games)
    items_for_upload = get_items_not_in_current(new, current_items.keys())
    return [(item,) for item in items_for_upload]


def get_games_for_upload(new_games: list[dict], current_games: dict) -> list[dict]:
    """Gets a set of current games, 
    then gets a set of games that have been scraped and cleaned, 
    then gets any game names that are in the scraped games and not in the database,
    then adds the dictionaries of games not in the databases."""
    current_games = set(current_games.keys())
    new_game_names = set(game["game_name"] for game in new_games)
    games_to_upload = [game for game in new_game_names if game not in current_games]
    return [game for game in new_games if game["game_name"] in games_to_upload]


def format_games_for_upload(games: list[dict], age_rating_mapping: dict) -> list[tuple]:
    """Returns a list of tuples to upload to the game table.
    Maps the age_rating to age_rating_id"""
    games_for_upload = []
    for game in games:
        games_for_upload.append((
            game["game_name"],
            game["game_image"],
            age_rating_mapping[game["age_rating"]],
            game["is_nsfw"]
        ))

    return games_for_upload


def pub_or_dev_game_assignment(game_ids: dict, pub_or_dev_ids: dict) -> list[tuple]:
    """Returns a list of tuples for uploading to
    the publisher_game_assignment or developer_game_assignment tables"""
    assignments = []
    for game_id in game_ids.values():
        for pub_dev_id in pub_or_dev_ids.values():
            assignments.append((game_id, pub_dev_id))
    return assignments


def make_current_dev_or_pub_game_assignment_tuples(
    current_assignments: list[dict], dev_or_pub_or_platform: str) -> list[tuple]:
    """takes the current publisher or developer game assignments
    and makes tuples in the form (game_id, pub/dev_id).
    This allows the new tuples to be checked against the existing."""
    return [(game["game_id"], game[dev_or_pub_or_platform]) for game in current_assignments]


def make_current_game_platform_assignment_tuples(
    current_assignments: list[dict]) -> list[tuple]:
    """Makes the current game_platform_assignment tuples"""
    return [(game["game_id"], game["platform_id"]) for game in current_assignments]
