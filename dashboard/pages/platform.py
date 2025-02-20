"""Information about each platform."""
# pylint: disable=unused-import, line-too-long, unused-variable
import logging
from os import environ as ENV
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from psycopg2 import connect
from dotenv import load_dotenv
from psycopg2.extensions import connection as psycopg_connection

@st.cache_resource
def get_connection() -> psycopg_connection:
    """Returns a connection to the database."""
    logging.info("Getting connection to database...")
    dbname = ENV['DB_NAME']
    user = ENV['DB_USERNAME']
    host = ENV['DB_HOST']
    port = ENV['DB_PORT']
    password = ENV['DB_PASSWORD']
    return connect(dbname=dbname, user=user, password=password, host=host, port=port)

def get_platform_data(conn, platform_name):
    """Fetch platform-related data from the database."""
    query = """
    SELECT
        p.platform_name,
        COUNT(g.game_id) AS num_games,
        COUNT(DISTINCT ggpa.genre_id) AS num_genres
    FROM
        platform p
        JOIN game_platform_assignment gpa ON p.platform_id = gpa.platform_id
        JOIN game g ON gpa.game_id = g.game_id
        LEFT JOIN genre_game_platform_assignment ggpa ON gpa.platform_assignment_id = ggpa.platform_assignment_id
    WHERE
        p.platform_name = %s
    GROUP BY
        p.platform_name
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (platform_name,))
        result = cursor.fetchone()
        if result:
            platform_name, num_games, num_genres = result
            return pd.DataFrame({
                'Platform': [platform_name],
                'Number of Games': [num_games],
                'Number of Genres': [num_genres]
            })
        else:
            return pd.DataFrame(columns=['Platform', 'Number of Games', 'Number of Genres'])

def get_genre_breakdown(conn, platform_name):
    """Fetch genre breakdown for the selected platform."""
    query = """
    SELECT
        g.genre_name,
        COUNT(gpa.game_id) AS num_games
    FROM
        genre g
        JOIN genre_game_platform_assignment ggpa ON g.genre_id = ggpa.genre_id
        JOIN game_platform_assignment gpa ON ggpa.platform_assignment_id = gpa.platform_assignment_id
        JOIN platform p ON gpa.platform_id = p.platform_id
    WHERE
        p.platform_name = %s
    GROUP BY
        g.genre_name
    ORDER BY
        num_games DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (platform_name,))
        result = cursor.fetchall()
        genres = [row[0] for row in result]
        num_games = [row[1] for row in result]
        
        return pd.DataFrame({
            'Genre': genres,
            'Number of Games': num_games
        })

def get_publisher_breakdown(conn, platform_name):
    """Fetch publisher breakdown for the selected platform."""
    query = """
    SELECT
        p.publisher_name,
        COUNT(g.game_id) AS num_games
    FROM
        publisher p
        JOIN publisher_game_assignment pga ON p.publisher_id = pga.publisher_id
        JOIN game g ON pga.game_id = g.game_id
        JOIN game_platform_assignment gpa ON g.game_id = gpa.game_id
        JOIN platform pl ON gpa.platform_id = pl.platform_id
    WHERE
        pl.platform_name = %s
    GROUP BY
        p.publisher_name
    ORDER BY
        num_games DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (platform_name,))
        result = cursor.fetchall()
        publishers = [row[0] for row in result]
        num_games = [row[1] for row in result]
        
        return pd.DataFrame({
            'Publisher': publishers,
            'Number of Games': num_games
        })

def get_developer_breakdown(conn, platform_name):
    """Fetch developer breakdown for the selected platform."""
    query = """
    SELECT
        d.developer_name,
        COUNT(g.game_id) AS num_games
    FROM
        developer d
        JOIN developer_game_assignment dga ON d.developer_id = dga.developer_id
        JOIN game g ON dga.game_id = g.game_id
        JOIN game_platform_assignment gpa ON g.game_id = gpa.game_id
        JOIN platform pl ON gpa.platform_id = pl.platform_id
    WHERE
        pl.platform_name = %s
    GROUP BY
        d.developer_name
    ORDER BY
        num_games DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (platform_name,))
        result = cursor.fetchall()
        developers = [row[0] for row in result]
        num_games = [row[1] for row in result]
        
        return pd.DataFrame({
            'Developer': developers,
            'Number of Games': num_games
        })

def get_age_rating_breakdown(conn, platform_name):
    """Fetch age rating breakdown for the selected platform."""
    query = """
    SELECT
        ar.age_rating_name,
        COUNT(g.game_id) AS num_games
    FROM
        age_rating ar
        JOIN game g ON ar.age_rating_id = g.age_rating_id
        JOIN game_platform_assignment gpa ON g.game_id = gpa.game_id
        JOIN platform p ON gpa.platform_id = p.platform_id
    WHERE
        p.platform_name = %s
    GROUP BY
        ar.age_rating_name
    ORDER BY
        num_games DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (platform_name,))
        result = cursor.fetchall()
        age_ratings = [row[0] for row in result]
        num_games = [row[1] for row in result]
        
        return pd.DataFrame({
            'Age Rating': age_ratings,
            'Number of Games': num_games
        })

def main():
    """Main function which displays everything on the page."""
    conn = get_connection()

    st.sidebar.image("logo.png", width=100)

    st.markdown("""
    <style>
        /* Custom CSS */
        @import url('https://fonts.googleapis.com/css?family=Press+Start+2P&display=swap');
        
        body {
            font-family: 'Press Start 2P', cursive;
            font-size: 22px;
            color: yellow;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #05122B;
        }

        [data-testid="stHeader"] {
            background-color: #05122B;
        }

        .st-bb {
            background-color: #05122B;
        }

        .sidebar-image {
            border-radius: 15px;
            border: 3px solid lightblue;
            width: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }

        .stSidebar .stSelectbox > div, 
        .stSidebar .stCheckbox > div,
        .stSidebar .stMultiSelect > div {
            color: yellow;
            font-family: 'Press Start 2P', cursive;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h3 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Platform Information</h3>',
                unsafe_allow_html=True)

    platform_name = st.selectbox("Select a Platform", ['Steam', 'Epic Games Store', 'GOG'])

    platform_data = get_platform_data(conn, platform_name)
    st.write(platform_data)

    genre_breakdown = get_genre_breakdown(conn, platform_name)
    st.write(genre_breakdown)

    publisher_breakdown = get_publisher_breakdown(conn, platform_name)
    st.write(publisher_breakdown)

    developer_breakdown = get_developer_breakdown(conn, platform_name)
    st.write(developer_breakdown)

    age_rating_breakdown = get_age_rating_breakdown(conn, platform_name)
    st.write(age_rating_breakdown)

    fig = px.bar(genre_breakdown, x='Genre', y='Number of Games', title=f"Genre Breakdown for {platform_name}")
    st.plotly_chart(fig)

if __name__ == "__main__":
    load_dotenv()
    main()
