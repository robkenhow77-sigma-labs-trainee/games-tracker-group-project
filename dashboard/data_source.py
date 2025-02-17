"""Functions that interact with the database"""
from os import environ as ENV

import psycopg2
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
import streamlit as st
import pandas as pd


@st.cache_resource
def get_connection():
    """connects to the games database"""
    connection = psycopg2.connect(
        dbname=ENV['DB_NAME'],
        user=ENV['DB_USERNAME'],
        password=ENV['DB_PASSWORD'],
        host=ENV['DB_HOST'],
        port=ENV['DB_PORT'],
        cursor_factory=RealDictCursor)

    return connection


@st.cache_data
def get_all_genres(_conn):
    """gets all game genres listed in the database"""
    query = "select genre_name from genre"
    with _conn.cursor() as cur:
        cur.execute(query)
        res = cur.fetchall()
    return pd.DataFrame(res)
