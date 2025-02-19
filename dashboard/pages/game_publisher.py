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

def get_publisher_info(conn, publisher_name):
    """Fetches information about the publisher based on partial search."""

    query = """
    SELECT 
        publisher.publisher_name,
        game.game_name
    FROM 
        publisher
    JOIN 
        publisher_game_assignment dga ON publisher.publisher_id = dga.publisher_id
    JOIN 
        game ON game.game_id = dga.game_id
    WHERE 
        publisher.publisher_name ILIKE %s;
    """
    
    
    cursor = conn.cursor()
    cursor.execute(query, (f"%{publisher_name}%",))
    publisher_data = cursor.fetchall()
    
    return publisher_data

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
        
        .sidebar-image {
            border-radius: 15px;
            border: 3px solid lightblue;
            width: 200px;  /* Adjust the width as per your requirement */
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

    st.markdown('<h3 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Publisher Information</h3>',
                unsafe_allow_html=True)

    
    publisher_name = st.text_input("Enter Publisher Name:", "")

    if publisher_name:
        publisher_data = get_publisher_info(conn, publisher_name)
        
        if publisher_data:
            
            st.write(f"**publisher: {publisher_data[0][0]}**")
            st.write(f"**Number of Games Developed: {len(publisher_data)}**")
            
            
            game_names = [game[1] for game in publisher_data]
            st.write("**Games Developed:**")
            st.write(", ".join(game_names))
        else:
            st.write("No publisher found with that name.")
    else:
        st.write("Enter a publisher name to search.")

if __name__ == "__main__":
    load_dotenv()
    main()
