# pylint: disable=line-too-long, ungrouped-imports
"""Dashboard that will get information about a selected game."""
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

def get_game_suggestions(partial_name: str, conn: psycopg_connection, exclude_nsfw: bool) -> list:
    """Fetches a list of game names that match the partial input, with an option to exclude NSFW games."""
    query = """
    SELECT game_name 
    FROM game 
    WHERE game_name ILIKE %s
    """
    
    # If NSFW exclusion is enabled, add the condition
    if exclude_nsfw:
        query += " AND is_nsfw = FALSE"
        
    query += " LIMIT 10;"
    
    cur = conn.cursor()
    cur.execute(query, ('%' + partial_name + '%',))
    game_names = [row[0] for row in cur.fetchall()]
    cur.close()
    return game_names

def get_game_info(game_name: str, conn: psycopg_connection, exclude_nsfw: bool) -> pd.DataFrame:
    """Fetches detailed game information from the database, including all genres, with an option to exclude NSFW games."""
    query = """
    SELECT 
        g.game_name,
        g.game_image,
        ar.age_rating_name,
        g.is_nsfw,
        p.platform_name,
        pga.platform_release_date,
        pga.platform_score,
        pga.platform_price,
        pga.platform_discount,
        pga.platform_url,
        pub.publisher_name,
        dev.developer_name,
        string_agg(gen.genre_name, ', ') AS genres  -- Aggregate genres into a single string
    FROM game g
    LEFT JOIN age_rating ar ON g.age_rating_id = ar.age_rating_id
    LEFT JOIN game_platform_assignment pga ON g.game_id = pga.game_id
    LEFT JOIN platform p ON pga.platform_id = p.platform_id
    LEFT JOIN publisher_game_assignment pga_pub ON g.game_id = pga_pub.game_id
    LEFT JOIN publisher pub ON pga_pub.publisher_id = pub.publisher_id
    LEFT JOIN developer_game_assignment dga ON g.game_id = dga.game_id
    LEFT JOIN developer dev ON dga.developer_id = dev.developer_id
    LEFT JOIN genre_game_platform_assignment gpga ON pga.platform_assignment_id = gpga.platform_assignment_id
    LEFT JOIN genre gen ON gpga.genre_id = gen.genre_id
    WHERE g.game_name = %s
    """
    
    # If NSFW exclusion is enabled, add the condition
    if exclude_nsfw:
        query += " AND g.is_nsfw = FALSE"
        
    query += " GROUP BY g.game_name, g.game_image, ar.age_rating_name, g.is_nsfw, p.platform_name, pga.platform_release_date, \
              pga.platform_score, pga.platform_price, pga.platform_discount, pga.platform_url, pub.publisher_name, \
              dev.developer_name;"
    
    cur = conn.cursor()
    cur.execute(query, (game_name,))
    game_info = cur.fetchall()
    cur.close()

    if not game_info:
        return pd.DataFrame()

    columns = [
        'game_name', 'game_image', 'age_rating_name', 'is_nsfw', 'platform_name', 'platform_release_date', 
        'platform_score', 'platform_price', 'platform_discount', 'platform_url', 'publisher_name', 'developer_name', 
        'genres'
    ]
    return pd.DataFrame(game_info, columns=columns)

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

    st.markdown('<h3 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Search Game</h3>', unsafe_allow_html=True)

    # Add NSFW exclusion checkbox in the sidebar
    exclude_nsfw = st.sidebar.checkbox("Exclude NSFW games", value=True)

    game_search_input = st.text_input("Search for a game by name:")

    if game_search_input:
        game_suggestions = get_game_suggestions(game_search_input, conn, exclude_nsfw)
        if game_suggestions:
            game_name = st.selectbox("Select a game:", game_suggestions)

            if game_name:
                game_info_df = get_game_info(game_name, conn, exclude_nsfw)

                if not game_info_df.empty:
                    st.markdown(f"### {game_info_df['game_name'][0]} Details")
                    st.image(game_info_df['game_image'][0], caption=game_info_df['game_name'][0], width=500)

                    score = game_info_df['platform_score'][0]
                    if score == -1:
                        rating_display = "No rating at release"
                    else:
                        rating_display = f"Score: {score}"

                    st.write(f"**Age Rating:** {rating_display}")
                    st.write(f"**NSFW Content**: {'Yes' if game_info_df['is_nsfw'][0] else 'No'}")
                    st.write(f"**Publisher**: {game_info_df['publisher_name'][0]}")
                    st.write(f"**Developer**: {game_info_df['developer_name'][0]}")
                    st.write(f"**Genres**: {game_info_df['genres'][0]}")
                    st.write(f"**Platform**: {game_info_df['platform_name'][0]}")
                    st.write(f"**Release Date**: {game_info_df['platform_release_date'][0]}")
                    st.write(f"**Price**: £{game_info_df['platform_price'][0] / 100:.2f}")
                    st.write(f"**Discount**: {game_info_df['platform_discount'][0]}%")
                    st.write(f"**Game Link**: {game_info_df['platform_url'][0]}")
        else:
            st.write("No game found with that name!")
    else:
        st.write("Start typing to search for a game...")

if __name__ == "__main__":
    load_dotenv()
    main()
