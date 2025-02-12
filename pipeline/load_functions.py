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


def execute_and_return_devs(devs: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
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


def execute_and_return_games(games: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO game (game_name, release_date, game_image, age_rating_id, is_nsfw) 
                        VALUES (%s, %s, %s, %s, %s) RETURNING *""", games, returning=True)
        ids = []
        while True:
            ids.append(cur.fetchone())
            if not cur.nextset():
                break
        conn.commit()
        return ids


def execute_and_return_pubs(pubs: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
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


def execute_and_return_genres(genre: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
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


def execute_and_return_tags(tags: list[tuple], conn: psycopg.Connection):
    """Loads values and returns"""
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


def get_game_platform_assignments(conn: psycopg.Connection):
    sql = """
    SELECT game_id, platform_id
    FROM game_platform_assignment
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


# Dev_assignment, pub_assignment
# def get_new_item_ids(table: str, new_games: list[dict], conn: psycopg.Connection, get_ids):
#     """Gets the ids that the items will have when they get uploaded to the database"""
#     items_for_upload = get_items_for_upload(table, new_games, conn)
#     ids = get_ids(table, conn)
#     max_id = max([game[f"{table}_id"] for game in ids])
#     return assign_new_ids(items_for_upload, max_id)