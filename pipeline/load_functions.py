"""Useful functions for load"""
import psycopg


def get_game_ids(conn: psycopg.Connection):
    """Gets the game name and ids"""
    query = f"""
        SELECT * FROM game;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_publisher_ids(conn: psycopg.Connection):
    """Gets the publisher names and ids"""
    query = f"""
        SELECT * FROM publisher;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    

def get_developer_ids(conn: psycopg.Connection):
    """Gets the developer names and ids"""
    query = f"""
        SELECT * FROM developer;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_tag_ids(conn: psycopg.Connection):
    """Gets the tag names and ids"""
    query = f"""
        SELECT * FROM tag;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_genre_ids(conn: psycopg.Connection):
    """Gets the genre names and ids"""
    query = f"""
        SELECT * FROM genre;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_age_rating_mapping(conn: psycopg.Connection):
    """Gets the age_ratings and ids"""
    query = f"""
        SELECT * FROM age_rating;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def upload_and_return_devs(devs: list[tuple], conn: psycopg.Connection):
    """Uploads the new developers and returns their names and ids"""
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
            return ids
    except:
        return {}


def upload_and_return_games(games: list[tuple], conn: psycopg.Connection):
    """Uploads the new games and returns their names and ids"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO game (game_name, release_date, game_image, age_rating_id, is_nsfw) 
                            VALUES (%s, %s, %s, %s, %s) RETURNING game_id, game_name""", games, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            return ids
    except :
        return {}


def upload_and_return_pubs(pubs: list[tuple], conn: psycopg.Connection):
    """Uploads the new publishers and returns their names and ids"""
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
            return ids
    except :
        return {}


def upload_and_return_genres(genre: list[tuple], conn: psycopg.Connection):
    """Uploads the new genres and returns their names and ids"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO genre (genre_name) 
                            VALUES (%s) RETURNING *""", genre, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            return ids
    except :
        return {}


def upload_and_return_tags(tags: list[tuple], conn: psycopg.Connection):
    """Uploads the new tags and returns their names and ids"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO tag (tag_name) 
                            VALUES (%s) RETURNING *""", tags, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            return ids
    except :
        return {}


def get_game_platform_assignments(conn: psycopg.Connection):
    """Gets the game_platform_assignment_ids, game_id and platform_id"""
    sql = """
    SELECT platform_assignment_id, game_id, platform_id
    FROM game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_publishers(new_games_list: list[dict], game_id_mapping: dict, publisher_mapping, current: list[tuple]):
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


def assign_developers(new_games_list: list[dict], game_id_mapping: dict, developer_mapping, current: list[tuple]):
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


def upload_developer_game_assignment(data: list[tuple], conn: psycopg.Connection):
    """Uploads the new developer_game_assignments"""
    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO developer_game_assignment (game_id, developer_id) 
            VALUES (%s, %s)""", data)
    conn.commit()


def upload_publisher_game_assignment(data: list[tuple], conn: psycopg.Connection):
    """Uploads the new publisher_game_assignments"""
    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO publisher_game_assignment (game_id, publisher_id) 
            VALUES (%s, %s)""", data)
        conn.commit()


def get_publisher_game_assignments(conn: psycopg.Connection):
    """Gets the publisher_game_assignments"""
    sql = """
    SELECT *
    FROM publisher_game_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
    

def get_developer_game_assignments(conn: psycopg.Connection):
    """Gets the developer_game_assignments"""
    sql = """
    SELECT *
    FROM developer_game_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_platform_ids(conn: psycopg.Connection):
    """Gets the platform names and ids"""
    sql = """
    SELECT *
    FROM platform
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_game_platform(new_games_list: list[dict], game_id_mapping: dict, platform_mapping: dict, current: list[tuple]):
    """Maps the game names to the ids and the publisher names to ids, for the game_platform_assignment table.
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
                game["discount"]
            ))
    return values


def upload_and_return_game_platform_assignment(data: list[tuple], conn: psycopg.Connection):
    """Uploads the game_platform_assignments and returns platform_assignment_id, game_id, platform_id"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO game_platform_assignment (game_id, platform_id, platform_score, platform_price, platform_discount) 
            VALUES (%s, %s, %s, %s, %s) RETURNING platform_assignment_id, game_id, platform_id""", data, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            return ids
    except :
        return {}


def get_genre_game_platform_assignment(conn: psycopg.Connection):
    """Gets the genre_game_platform_assignments"""
    sql = """
    SELECT *
    FROM genre_game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_tag_game_platform_assignment(conn: psycopg.Connection):
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
        game_platform_assignment_mapping: dict, current: list[tuple]):
    """Maps the genre names to the ids and the game names and platform names to the game_platform_assignment_id, for the genre_game_platform_assignment table.
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
        game_platform_assignment_mapping: dict, current: list[tuple]):
    """Maps the tag names to the ids and the game names and platform names to the game_platform_assignment_id, for the tag_game_platform_assignment table.
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


def upload_genre_game_platform_assignment(data: list[tuple], conn: psycopg.Connection):
    """Uploads the genre_game_platform_assignments"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO genre_game_platform_assignment (genre_id, platform_assignment_id) 
            VALUES (%s, %s)""", data)
            conn.commit()
    except:
        return None


def upload_tag_game_platform_assignment(data: list[tuple], conn: psycopg.Connection):
    """Uploads the tag_game_platform_assignments"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO tag_game_platform_assignment (tag_id, platform_assignment_id) 
            VALUES (%s, %s)""", data)
            conn.commit()
    except:
        return None


def make_id_mapping(ids_and_items: list[dict], item: str):
    """Creates a dictionary in the form {item_name: id}"""
    return {id_and_item[f'{item}_name']: id_and_item[f'{item}_id'] for id_and_item in ids_and_items}


def get_new_items_set(item: str, games_list_dict: list[dict]) -> list[str]:
    """Gets the specified item from each dictionary
    Eg. get all the game titles. Uses a set to make sure their are no duplicates
    """
    items = set()
    for game in games_list_dict:
        value = game[item]
        for val in value:
            items.add(val)
    return items


def get_items_not_in_current(new: list[str], current: list[str]):
    """Checks the new list to find any strings not in the current list. 
    Eg. new tags that aren't already in the database"""
    return [word for word in new if word not in current]


def get_items_for_upload(table: str, new_games: list[dict], current_items: dict):
    """Gets all the new items for uploading, that aren't already in the database"""
    new = get_new_items_set(table, new_games)
    items_for_upload = get_items_not_in_current(new, current_items.keys())
    return [(item,) for item in items_for_upload]


def get_games_for_upload(new_games: list[dict], current_games: dict):
    """Gets a set of current games, 
    then gets a set of games that have been scraped and cleaned, 
    then gets any game names that are in the scraped games and not in the database,
    then adds the dictionaries of games not in the databases."""
    current_games = set(current_games.keys())
    new_game_names = set(game["game_name"] for game in new_games)
    games_to_upload = [game for game in new_game_names if game not in current_games]
    return [game for game in new_games if game["game_name"] in games_to_upload]
    

def format_games_for_upload(games: list[dict], age_rating_mapping: dict):
    """Returns a list of tuples to upload to the game table.
    Maps the age_rating to age_rating_id"""
    games_for_upload = []
    for game in games:
        games_for_upload.append((
            game["game_name"],
            game["release_date"],
            game["game_image"],
            age_rating_mapping[game["age_rating"]], # NEED TO MAP
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


def make_current_dev_or_pub_game_assignment_tuples(current_assignments: list[dict], dev_or_pub_or_platform: str):
    """takes the current publisher or developer game assignments
    and makes tuples in the form (game_id, pub/dev_id).
    This allows the new tuples to be checked against the existing."""
    return [(game["game_id"], game[dev_or_pub_or_platform]) for game in current_assignments]


def make_current_game_platform_assignment_tuples(current_assignments: list[dict], dev_or_pub_or_platform: str):
    return [(game["game_id"], game[dev_or_pub_or_platform]) for game in current_assignments]
