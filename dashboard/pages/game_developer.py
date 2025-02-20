# pylint: disable=line-too-long, ungrouped-imports
"""Dashboard that will get information about a selected developer."""
import logging
from os import environ as ENV
import pandas as pd
import streamlit as st
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

def get_developer_info(conn, developer_name):
    """Fetches information about the developer based on partial search."""

    query = """
    SELECT 
        developer.developer_name,
        game.game_name,
        game.game_image
    FROM 
        developer
    JOIN 
        developer_game_assignment dga ON developer.developer_id = dga.developer_id
    JOIN 
        game ON game.game_id = dga.game_id
    WHERE 
        developer.developer_name ILIKE %s;
    """

    cursor = conn.cursor()
    cursor.execute(query, (f"%{developer_name}%",))
    developer_data = cursor.fetchall()

    return developer_data

def main():
    """Main function which displays everything on the page."""
    conn = get_connection()

    st.sidebar.image("logo.png", width=100)

    st.markdown("""
    <style>
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
        
        /* Sidebar filter elements */
        .stSidebar .stSelectbox > div, 
        .stSidebar .stCheckbox > div,
        .stSidebar .stMultiSelect > div {
            color: yellow;
            font-family: 'Press Start 2P', cursive;
        }

        .stSidebar .stSelectbox label, 
        .stSidebar .stCheckbox label, 
        .stSidebar .stMultiSelect label {
            color: yellow;
            font-family: 'Press Start 2P', cursive;
        }

        /* For the selectbox dropdown itself */
        .stSidebar .stSelectbox div[data-baseweb="select"] {
            background-color: black;
            color: yellow;
            font-family: 'Press Start 2P', cursive;
        }

        /* For the selectbox dropdown options */
        .stSidebar .stSelectbox div[data-baseweb="select"] div {
            color: yellow;
            font-family: 'Press Start 2P', cursive;
        }

        /* For the streamlit expander titles */
        .stSidebar .css-1v3fvcr {
            font-family: 'Press Start 2P', cursive;
            color: yellow;
        }

        /* Chart Titles (Plotly) */
        .stChart .plotly-title {
            font-family: 'Press Start 2P', cursive;
            color: yellow;
        }

        /* Subheader titles */
        .stSubheader, .stTitle {
            font-family: 'Press Start 2P', cursive;
            color: yellow;
        }

        /* Sidebar Header */
        .stSidebar .css-1v3fvcr {
            font-family: 'Press Start 2P', cursive;
            color: yellow;
        }

        .markdown-text-container {
            color: yellow;
        }
            
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h3 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Developer Information</h3>',
                unsafe_allow_html=True)

    developer_name = st.text_input("Enter Developer Name:", "")

    if developer_name:
        developer_data = get_developer_info(conn, developer_name)
        if developer_data:
            st.markdown(f'<div style="text-align: center; margin-bottom: 20px;">'
                        f"<h3 style='font-size: 30px;'>Developer: {developer_data[0][0]}</h3>"
                        f'<h2>Number of Games Developed: {len(developer_data)}</h2>'
                        '</div>', unsafe_allow_html=True)

            for game in developer_data:
                game_name, game_image = game[1], game[2]

                st.markdown(f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-top: 20px;">'
                            f'<h2>Game: {game_name}</h2>'
                            f'<img src="{game_image}" alt="{game_name}" style="width: 500px; border-radius: 10px; border: 3px solid #008080;" />'
                            '</div>', unsafe_allow_html=True)

        else:
            st.write("No developer found with that name.")
    else:
        st.write("Enter a developer name to search.")

if __name__ == "__main__":
    load_dotenv()
    main()
