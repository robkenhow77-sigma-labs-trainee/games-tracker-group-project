"""Useful functions for load """
import psycopg

def get_game_ids(conn: psycopg.Connection):
    """Simple query function"""
    query = f"""
        SELECT * FROM game;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_publisher_ids(conn: psycopg.Connection):
    """Simple query function"""
    query = f"""
        SELECT * FROM publisher;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    

def get_developer_ids(conn: psycopg.Connection):
    """Simple query function"""
    query = f"""
        SELECT * FROM developer;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_tag_ids(conn: psycopg.Connection):
    """Simple query function"""
    query = f"""
        SELECT * FROM tag;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_genre_ids(conn: psycopg.Connection):
    """Simple query function"""
    query = f"""
        SELECT * FROM genre;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def upload_and_return_devs(devs: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
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
    """Loads values and returns"""
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
    """Loads values and returns"""
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
    """Loads values and returns"""
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
    """Loads values and returns"""
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
    sql = """
    SELECT platform_assignment_id, game_id, platform_id
    FROM game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_publishers(new_games_list: list[dict], game_id_mapping: dict, publisher_mapping, current: list[tuple]):
    """Maps the names to the ids and the pubs to ids, for the assignment table"""
    values = []
    for game in new_games_list:
        if isinstance(game["publisher"], list):
            publishers = game["publisher"]
            for publisher in publishers:
                values.append((
                    game_id_mapping[game["game_name"]],
                    publisher_mapping[publisher]
                ))
        else:
            values.append((
                game_id_mapping[game["game_name"]],
                publisher_mapping[game["publisher"]]
            ))
    return [value for value in values if value not in current]


def assign_developers(new_games_list: list[dict], game_id_mapping: dict, developer_mapping, current: list[tuple]):
    """Maps the names to the ids and the pubs to ids, for the assignment table"""
    values = []
    for game in new_games_list:
        if isinstance(game["developer"], list):
            developers = game["developer"]
            for developer in developers:
                values.append((
                    game_id_mapping[game["game_name"]],
                    developer_mapping[developer]
                ))
        else:
            values.append((
                game_id_mapping[game["game_name"]],
                developer_mapping[game["developer"]]
            ))
    return [value for value in values if value not in current]


def upload_developer_assignment(data: list[tuple], conn: psycopg.Connection):
     with conn.cursor() as cur:
        cur.executemany("""INSERT INTO developer_game_assignment (game_id, developer_id) 
            VALUES (%s, %s)""", data)
        conn.commit()


def upload_publisher_assignment(data: list[tuple], conn: psycopg.Connection):
     with conn.cursor() as cur:
        cur.executemany("""INSERT INTO publisher_game_assignment (game_id, publisher_id) 
            VALUES (%s, %s)""", data)
        conn.commit()


def get_publisher_game_assignments(conn: psycopg.Connection):
    sql = """
    SELECT *
    FROM publisher_game_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
    

def get_developer_game_assignments(conn: psycopg.Connection):
    sql = """
    SELECT *
    FROM developer_game_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_platform_mapping(conn: psycopg.Connection):
    sql = """
    SELECT *
    FROM platform
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def assign_game_platform(new_games_list: list[dict], game_id_mapping: dict, platform_mapping: dict, current: list[tuple]):
    """Maps the names to the ids and the pubs to ids, for the assignment table"""
    values = []
    for game in new_games_list:
        new_assignment_tuple = (
            game_id_mapping[game["game_name"]], platform_mapping[game["platform"]]
        )
        if new_assignment_tuple not in current:
            values.append((
                game_id_mapping[game["game_name"]], # game_id
                platform_mapping[game["platform"]], # platform_id
                game["score"], # platform_score
                game["price"], # platform_price
                game["discount"] # platform_discount
            ))
    return values


def upload_and_return_game_platform_assignment(data: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
    try:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO game_platform_assignment (game_id, platform_id, platform_score, platform_price, platform_discount) 
            VALUES (%s, %s, %s, %s, %s) RETURNING platform_assignment_id, game_id""", data, returning=True)
            ids = []
            while True:
                ids.append(cur.fetchone())
                if not cur.nextset():
                    break
            conn.commit()
            return ids
    except :
        return {}
