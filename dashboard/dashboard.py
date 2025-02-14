"""Code for designing the dashboard."""

import logging
from os import environ as ENV
from datetime import datetime

import pandas as pd
from psycopg2 import connect
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st
from requests import get

def get_connection() -> object:
    """Returns a connection to the database."""

    logging.info("Getting connection to database...")

    dbname = ENV['DB_NAME']
    user = ENV['DB_USERNAME']
    host = ENV['DB_HOST']
    port = ENV['DB_PORT']
    password = ENV['DB_PASSWORD']

    connection = connect(dbname=dbname, user=user, password=password, host=host, port=port)

    logging.info('Connected.')

    return connection


def get_data(conn: connection) -> pd.DataFrame:
    """Gets the data from the database"""

    with conn.cursor() as cur:
        cur.execute("""
        SELECT g.game_id, g.game_name, gpa.platform_score, gpa.platform_release_date, g.game_image, gpa.platform_price
        FROM game g
        JOIN game_platform_assignment gpa
        ON g.game_id = gpa.game_id;
        """)
        data = cur.fetchall()

    columns = ['ID', 'Title', 'Score', 'Release Date', 'Image', 'Price']

    return pd.DataFrame(data, columns=columns)


def format_price(price: int) -> str:
    """Returns the price in £ format."""

    if price > 0:
        return f"£{int(price) / 100:.2f}"

    return "Free to play"


def format_score(score: int) -> str:
    """Returns the score out of 100."""

    if score != -1:
        return str(score) + "/100"

    return "No ratings on release."


def format_date(date: datetime) -> str:
    """Returns the date formatted as DD/MM/YYYY"""
    return datetime.strftime(date, "%d/%m/%Y")


if __name__ == "__main__":

    load_dotenv()

    connection_to_db = get_connection()

    value_data = get_data(connection_to_db)

    connection_to_db.close()

    print(value_data)

    st.write("Game Data Table:")

    cols = st.columns(5)
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
    st.markdown("---")

    for idx, row in value_data.iterrows():
        cols = st.columns(5)
        with cols[0]:
            st.write(f"{row["Title"]}")
        with cols[1]:
            try: 
                get(row['Image'])
                if get(row['Image']).status_code == 200:
                    st.image(row["Image"], caption=row["Title"])
                else:
                    st.write("NO VALID IMAGE")
            except:
                st.write("NO VALID IMAGE")
        with cols[2]:
            st.write(f"{format_date(row['Release Date'])}")
        with cols[3]:
            st.write(f"{format_score(row['Score'])}")
        with cols[4]:
            st.write(f"{format_price(row['Price'])}")
        st.markdown("---")
