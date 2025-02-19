#pylint: disable=line-too-long, ungrouped-imports
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

def get_game_suggestions(partial_name: str, conn: psycopg_connection) -> list:
    """Fetches a list of game names that match the partial input."""
    query = """
    SELECT game_name 
    FROM game 
    WHERE game_name ILIKE %s
    LIMIT 10;
    """
    cur = conn.cursor()
    cur.execute(query, ('%' + partial_name + '%',))
    game_names = [row[0] for row in cur.fetchall()]
    cur.close()
    return game_names

def get_game_info(game_name: str, conn: psycopg_connection) -> pd.DataFrame:
    """Fetches detailed game information from the database, including all genres."""
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
    GROUP BY g.game_name, g.game_image, ar.age_rating_name, g.is_nsfw, p.platform_name, pga.platform_release_date,
             pga.platform_score, pga.platform_price, pga.platform_discount, pub.publisher_name, dev.developer_name;
    """

    cur = conn.cursor()
    cur.execute(query, (game_name,))
    game_info = cur.fetchall()
    cur.close()

    if not game_info:
        return pd.DataFrame()

    columns = [
        'game_name', 'game_image', 'age_rating_name', 'is_nsfw', 'platform_name', 'platform_release_date', 
        'platform_score', 'platform_price', 'platform_discount', 'publisher_name', 'developer_name', 'genres'
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

    game_search_input = st.text_input("Search for a game by name:")

    if game_search_input:
        game_suggestions = get_game_suggestions(game_search_input, conn)
        if game_suggestions:
            game_name = st.selectbox("Select a game:", game_suggestions)

            if game_name:
                game_info_df = get_game_info(game_name, conn)

                if not game_info_df.empty:
                    st.markdown(f"<h3 style='text-align: center; font-family: \"Press Start 2P\", cursive; color: yellow;'>"
                                f"{game_info_df['game_name'][0]} Details</h3>", unsafe_allow_html=True)

                    platforms = game_info_df['platform_name'].unique()
                    selected_platform = st.sidebar.selectbox("Select Platform", platforms)

                    game_info_df_filtered = game_info_df[game_info_df['platform_name'] == selected_platform]

                    score = game_info_df_filtered['platform_score'].iloc[0]
                    if score == -1:
                        rating_display = "No rating at release"
                    else:
                        rating_display = f"Score: {score}"

                    st.markdown(f"<div style='text-align: center;'>"
                                f"<img src='{game_info_df_filtered['game_image'].iloc[0]}' alt='{game_info_df_filtered['game_name'].iloc[0]}' width='500' />"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Age Rating:</b> {rating_display}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>NSFW Content:</b> {'Yes' if game_info_df_filtered['is_nsfw'].iloc[0] else 'No'}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Publisher:</b> {game_info_df_filtered['publisher_name'].iloc[0]}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Developer:</b> {game_info_df_filtered['developer_name'].iloc[0]}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Genres:</b> {game_info_df_filtered['genres'].iloc[0]}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Platform:</b> {game_info_df_filtered['platform_name'].iloc[0]}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Release Date:</b> {game_info_df_filtered['platform_release_date'].iloc[0]}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Price:</b> £{game_info_df_filtered['platform_price'].iloc[0] / 100:.2f}</p>"
                                f"<p style='font-family: \"Press Start 2P\", cursive; color: yellow;'><b>Discount:</b> {game_info_df_filtered['platform_discount'].iloc[0]}%</p>"
                                f"</div>", unsafe_allow_html=True)

        else:
            st.write("No game found with that name!")
    else:
        st.write("Start typing to search for a game...")

if __name__ == "__main__":
    load_dotenv()
    main()
