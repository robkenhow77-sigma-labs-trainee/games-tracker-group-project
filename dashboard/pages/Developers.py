#pylint: disable=invalid-name, ungrouped-imports, too-many-positional-arguments, too-many-arguments, too-many-locals, line-too-long, duplicate-code
"""Dashboard for Developers to see statistics about games."""
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

def get_number_of_games_by_platform(conn: psycopg_connection) -> pd.DataFrame:
    """Fetches the number of games released for each platform, excluding NSFW games."""
    query = """
    SELECT p.platform_name, COUNT(g.game_id) AS game_count
    FROM platform p
    JOIN game_platform_assignment gp ON p.platform_id = gp.platform_id
    JOIN game g ON g.game_id = gp.game_id
    WHERE g.is_nsfw = FALSE  -- Filter out NSFW games
    GROUP BY p.platform_name
    ORDER BY game_count DESC
    """

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    df = pd.DataFrame(result, columns=["platform_name", "game_count"])

    return df

def get_number_of_games_by_genre(conn: psycopg_connection) -> pd.DataFrame:
    """Fetches the number of games released per genre."""
    query = """
    SELECT ge.genre_name, COUNT(DISTINCT g.game_id) AS game_count
    FROM genre ge
    JOIN genre_game_platform_assignment gpa ON ge.genre_id = gpa.genre_id
    JOIN game_platform_assignment gp ON gpa.platform_assignment_id = gp.platform_assignment_id
    JOIN game g ON g.game_id = gp.game_id
    GROUP BY ge.genre_name
    ORDER BY game_count DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return pd.DataFrame(result, columns=["genre_name", "game_count"])


def get_genre_tag_platform_options(conn: psycopg_connection) -> tuple[list[str],
                                                           list[str], list[str]]:
    """Gets all the genres, tags, and platforms to filter by."""
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


def get_filtered_games(conn: psycopg_connection, genre: str = None, tag: str = None, price: float = None,
        platform: str = None, top_n: int = None, exclude_nsfw: bool = True) -> pd.DataFrame:
    """Fetches games based on the user's filter selection."""
    query = """
    SELECT DISTINCT g.game_name, g.game_image, gp.platform_score, gp.platform_price, p.platform_name, g.is_nsfw
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
    if exclude_nsfw:
        filters.append("g.is_nsfw = FALSE")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if top_n:
        query += " ORDER BY gp.platform_score DESC, gp.platform_price DESC LIMIT %s"

    params = []
    if genre and genre != "All":
        params.append(genre)
    if tag and tag != "All":
        params.append(tag)
    if price:
        params.append(price)
    if platform and platform != "All":
        params.append(platform)
    if top_n:
        params.append(top_n)

    with conn.cursor() as cursor:
        cursor.execute(query, tuple(params))
        result = cursor.fetchall()

    df = pd.DataFrame(result, columns=["game_name",
                                       "game_image",
                                       "platform_score",
                                       "platform_price",
                                       "platform_name",
                                       "is_nsfw"])
    df['platform_price'] = df['platform_price'] / 100
    df['platform_score'] = df['platform_score'].apply(
        lambda x: "No rating at release" if x == -1 else x)

    return df


def get_price_filter_options() -> list[str]:
    """Returns a list of price ranges for user-friendly filtering."""
    return ["All", "Free", "Under £10", "£10 - £50", "£50 - £100", "Above £100"]


def main():
    """Main function to manage the Streamlit app interface."""
    conn = get_connection()

    st.sidebar.image("../images/logo.png", width=100)


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


    genres, tags, platforms = get_genre_tag_platform_options(conn)

    selected_genre = st.sidebar.selectbox("Genre", options=["All"] + genres)
    selected_tag = st.sidebar.selectbox("Tag", options=["All"] + tags)
    selected_platform = st.sidebar.selectbox("Platform", options=["All"] + platforms)
    price_range = st.sidebar.selectbox("Price Range", options=get_price_filter_options())
    include_nsfw = st.sidebar.checkbox("Include NSFW Games", value=False)

    price_mapping = {
        "Free": 0,
        "Under £10": 10,
        "£10 - £50": 50,
        "£50 - £100": 100,
        "Above £100": 300
    }

    selected_price = price_mapping.get(price_range, None)

    genre_counts = get_filtered_games(conn,
                                      genre=selected_genre,
                                      tag=selected_tag,
                                      price=selected_price,
                                      platform=selected_platform,
                                      exclude_nsfw=include_nsfw)
    genre_counts = genre_counts.groupby('platform_name').size().reset_index(name='counts')

    st.markdown('<h4 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Games Released by Platform</h4>',
                unsafe_allow_html=True)
    platform_data = get_number_of_games_by_platform(conn)
    fig = px.bar(platform_data, x='platform_name', y='game_count', color='platform_name',
                 labels={'platform_name': 'Platform', 'game_count': 'Number of Games'})
    st.plotly_chart(fig)

    st.markdown('<h4 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Games Released by Genre</h4>',
                unsafe_allow_html=True)
    genre_data = get_number_of_games_by_genre(conn)
    fig = px.bar(genre_data, x='genre_name', y='game_count', color='genre_name',
                 labels={'genre_name': 'Genre', 'game_count': 'Number of Games'})
    st.plotly_chart(fig)

    st.markdown('<h4 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Top 10 Best Reviewed Games</h4>',
                unsafe_allow_html=True)

    top_games = get_filtered_games(conn,
                                   selected_genre,
                                   selected_tag,
                                   selected_price,
                                   selected_platform,
                                   top_n=10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='platform_score', y='game_name', data=top_games, palette="rocket", ax=ax)

    ax.set_xlabel("Score", fontsize=12, color='white')
    ax.set_ylabel("Game Name", fontsize=12, color='white')
    ax.tick_params(axis='both', labelsize=10, labelcolor='white')
    ax.xaxis.set_tick_params(labelcolor='white')
    ax.yaxis.set_tick_params(labelcolor='white')

    fig.patch.set_visible(False)
    ax.patch.set_visible(False)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()

    st.pyplot(fig)

    st.markdown('<h4 style="font-family: \'Press Start 2P\', cursive; color: yellow;">Price vs Rating Scatter Plot</h4>',
                unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    all_games = get_filtered_games(conn, selected_genre, selected_tag, selected_price, selected_platform)
    fig = px.scatter(all_games,
                     x='platform_price',
                     y='platform_score',
                     hover_name='game_name',
                     hover_data={'platform_name': True,
                                 'platform_price': True,
                                 'platform_score': True},
                     labels={'platform_price': 'Price (in Pounds)',
                             'platform_score': 'Rating'})

    fig.update_traces(marker={'size': 12,
                              'opacity': 0.7,
                              'line': {
                                  'width': 2,
                                  'color': 'DarkSlateGrey'
                              }})
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font={'color': 'white'},
        xaxis={'tickformat': '.2f'},
        yaxis={'tickformat': '.2f'}
    )

    st.plotly_chart(fig)

if __name__ == "__main__":
    load_dotenv()
    main()
