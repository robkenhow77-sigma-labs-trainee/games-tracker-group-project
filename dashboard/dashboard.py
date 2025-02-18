"""
This module connects to a PostgreSQL database to fetch and display game data. 
It allows users to filter games by genre, tag, price, and platform, 
and displays information such as title, image, release date, score, price, and platform.
"""
import logging
from os import environ as ENV
from datetime import datetime
import pandas as pd
from psycopg2 import connect
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st
from requests import get


@st.cache_resource
def get_connection() -> object:
    """Returns a new connection to the database."""
    logging.info("Getting connection to database...")

    dbname = ENV['DB_NAME']
    user = ENV['DB_USERNAME']
    host = ENV['DB_HOST']
    port = ENV['DB_PORT']
    password = ENV['DB_PASSWORD']

    return connect(dbname=dbname, user=user, password=password, host=host, port=port)


def get_genre_tag_platform_options(conn: connection) -> tuple[list[str], list[str], list[str]]:
    """Fetches all available genres, tags, and platforms for filtering."""
    genre_query = "SELECT genre_name FROM genre"
    tag_query = "SELECT tag_name FROM tag"
    platform_query = "SELECT platform_name FROM platform"

    with conn.cursor() as cursor:
        cursor.execute(genre_query)
        available_genres = [row[0] for row in cursor.fetchall()]

        cursor.execute(tag_query)
        available_tags = [row[0] for row in cursor.fetchall()]

        cursor.execute(platform_query)
        available_platforms = [row[0] for row in cursor.fetchall()]

    return available_genres, available_tags, available_platforms


def get_filtered_games(conn: connection, genre: str = None, tag: str = None, price: float = None,
    platform: str = None, limit: int = 25, offset: int = 0) -> pd.DataFrame:
    """
    Fetches games from the database based on the provided filters (genre, tag, price, platform).

    Returns:
        A Pandas DataFrame containing filtered game data.
    """
    query = """
    SELECT DISTINCT g.game_name, g.game_image, gp.platform_score, gp.platform_price, 
                    gp.platform_release_date, p.platform_name
    FROM game g
    JOIN game_platform_assignment gp ON g.game_id = gp.game_id
    JOIN platform p ON gp.platform_id = p.platform_id
    LEFT JOIN genre_game_platform_assignment gpa ON gp.platform_assignment_id = gpa.platform_assignment_id
    LEFT JOIN genre ge ON gpa.genre_id = ge.genre_id
    LEFT JOIN tag_game_platform_assignment tgpa ON gp.platform_assignment_id = tgpa.platform_assignment_id
    LEFT JOIN tag t ON tgpa.tag_id = t.tag_id
    """
    filters = []

    if genre and genre != "All":
        filters.append("ge.genre_name = %s")
    if tag and tag != "All":
        filters.append("t.tag_name = %s")
    if price:
        filters.append("gp.platform_price <= %s")
    if platform and platform != "All":
        filters.append("p.platform_name = %s")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY g.game_name LIMIT %s OFFSET %s"

    params = []
    if genre and genre != "All":
        params.append(genre)
    if tag and tag != "All":
        params.append(tag)
    if price:
        params.append(price * 100)
    if platform and platform != "All":
        params.append(platform)
    params.append(limit)
    params.append(offset)

    with conn.cursor() as cursor:
        cursor.execute(query, tuple(params))
        result = cursor.fetchall()

    df = pd.DataFrame(result, columns=["game_name", "game_image", "platform_score",
                "platform_price", "platform_release_date", "platform_name"])

    df['platform_price'] = df['platform_price']
    df['platform_score'] = df['platform_score'].apply(
        lambda x: "No rating at release"
        if x == -1 else f"{x}%"
        if x != "No rating at release" else x)
    return df


def format_price(price: int) -> str:
    """Returns the price in £ format."""
    return f"£{price / 100:.2f}" if price > 0 else "Free to play"

def format_score(score: str) -> str:
    """Returns the score formatted as 'No rating at release' or a percentage."""
    return score if score == "No rating at release" else score

def format_date(date: datetime) -> str:
    """Returns the date formatted as DD/MM/YYYY."""
    return datetime.strftime(date, "%d/%m/%Y")

def main():
    """Main function to execute the Streamlit app."""
    load_dotenv()


    if 'offset' not in st.session_state:
        st.session_state.offset = 0
        st.session_state.limit = 25

    offset = st.session_state.offset
    limit = st.session_state.limit

    connection_to_db = get_connection()
    genres, tags, platforms = get_genre_tag_platform_options(connection_to_db)

    genre_filter = st.sidebar.selectbox("Select Genre", ["All"] + genres)
    tag_filter = st.sidebar.selectbox("Select Tag", ["All"] + tags)
    platform_filter = st.sidebar.selectbox("Select Platform", ["All"] + platforms)
    price_range = st.sidebar.selectbox("Price Range", ["Any",
                                                       "Free",
                                                       "Under £10",
                                                       "£10 - £50",
                                                       "£50 - £100",
                                                       "Above £100"])

    price_mapping = {
        "Free": 0,
        "Under £10": 10,
        "£10 - £50": 50,
        "£50 - £100": 100,
        "Above £100": 300
    }

    selected_price = price_mapping.get(price_range, None)
    value_data = get_filtered_games(connection_to_db,
                                    genre_filter,
                                    tag_filter,
                                    selected_price,
                                    platform_filter,
                                    limit,
                                    offset)

    st.write("Game Data Table:")

    cols = st.columns(6)
    with cols[0]:
        st.write("Title")
    with cols[1]:
        st.write("Image")
    with cols[2]:
        st.write("Release Date")
    with cols[3]:
        st.write("Score")
    with cols[4]:
        st.write("Price")
    with cols[5]:
        st.write("Platform")
    st.markdown("---")

    for idx, row in value_data.iterrows():
        cols = st.columns(6)
        with cols[0]:
            st.write(f"{row['game_name']}")
        with cols[1]:
            try:
                response = get(row['game_image'], timeout=5)
                if response.status_code == 200:
                    st.image(row["game_image"], caption=row["game_name"])
                else:
                    st.write("No valid image")
            except Exception:
                st.write("No valid image")
        with cols[2]:
            st.write(f"{format_date(row['platform_release_date'])}")
        with cols[3]:
            st.write(format_score(row['platform_score']))
        with cols[4]:
            st.write(format_price(row['platform_price']))
        with cols[5]:
            st.write(row['platform_name'])
        st.markdown("---")


    if st.button("Load More"):
        st.session_state.offset += limit
        value_data = get_filtered_games(connection_to_db,
                                    genre_filter,
                                    tag_filter,
                                    selected_price,
                                    platform_filter,
                                    limit,
                                    offset)

        for idx, row in value_data.iterrows():
            cols = st.columns(6)
            with cols[0]:
                st.write(f"{row['game_name']}")
            with cols[1]:
                try:
                    response = get(row['game_image'], timeout=5)
                    if response.status_code == 200:
                        st.image(row["game_image"], caption=row["game_name"])
                    else:
                        st.write("No valid image")
                except Exception:
                    st.write("No valid image")
            with cols[2]:
                st.write(f"{format_date(row['platform_release_date'])}")
            with cols[3]:
                st.write(format_score(row['platform_score']))
            with cols[4]:
                st.write(format_price(row['platform_price']))
            with cols[5]:
                st.write(row['platform_name'])
            st.markdown("---")


if __name__ == "__main__":
    main()
