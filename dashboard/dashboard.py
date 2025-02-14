"""Code for designing the dashboard."""

import logging
from os import environ as ENV
from datetime import datetime

import pandas as pd
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv
import streamlit as st

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


def get_cursor(conn: object) -> object:
    """Returns a database cursor"""
    return conn.cursor()


def get_data(conn: object) -> object:

    with get_cursor(conn) as cur:
        cur.execute("""
        SELECT g.game_id, g.game_name, gpa.platform_score, g.release_date, g.game_image, gpa.platform_price
        FROM game g
        JOIN game_platform_assignment gpa
        ON g.game_id = gpa.game_id;
        """)
        data = cur.fetchall()

    columns = ['ID', 'Title', 'Score', 'Release Date', 'Image', 'Price']

    return pd.DataFrame(data, columns=columns)


def format_price(price: int) -> str:
    """Returns the price in £ format."""

    if price > 99:    
        return "£" + str(price)[:-2] + "." + str(price)[-2:]

    if price > 9:
        return "£0." + str(price)[:]
    
    if price > 0:
        return "£0.0" + str(price)[:]
    
    return "Free to play"


def format_score(score: int) -> str:
    """Returns the score out of 100."""

    if score != -1:
        return str(score) + "/100"
    
    return "No ratings yet"


def format_date(date: datetime) -> str:
    """Returns the date formatted as DD/MM/YYYY"""
    return datetime.strftime(date, "%d/%m/%Y")


if __name__ == "__main__":

    load_dotenv()

    conn = get_connection()

    data = get_data(conn)

    print(data)

    st.write("Game Data Table:")


    for idx, row in data.iterrows():
        st.image(row["Image"], caption=row["Title"])
        st.write(f"Release Date: {format_date(row['Release Date'])}")
        st.write(f"Score: {format_score(row['Score'])}")
        st.write(f"Price: {format_price(row['Price'])}")
        st.markdown("---")