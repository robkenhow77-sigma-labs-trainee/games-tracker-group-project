#pylint: disable=invalid-name, ungrouped-imports, too-many-positional-arguments, too-many-arguments, too-many-locals
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
from psycopg2.extensions import connection as psycopg_connection, cursor as psycopg_cursor

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


def get_genre_tag_platform_options(cursor: psycopg_cursor) -> tuple[list[str],
                                                           list[str], list[str]]:
    """Gets all the genres, tags, and platforms to filter by."""
    genre_query = "SELECT genre_name FROM genre"
    tag_query = "SELECT tag_name FROM tag"
    platform_query = "SELECT platform_name FROM platform"


    cursor.execute(genre_query)
    available_genres = [row[0] for row in cursor.fetchall()]


    cursor.execute(tag_query)
    available_tags = [row[0] for row in cursor.fetchall()]


    cursor.execute(platform_query)
    available_platforms = [row[0] for row in cursor.fetchall()]

    return available_genres, available_tags, available_platforms


def get_filtered_games(cursor: psycopg_cursor, genre: str = None, tag: str = None,
                   price: float = None, platform: str = None, top_n: int = None) -> pd.DataFrame:
    """Fetches games based on the user's filter selection."""
    query = """
    SELECT DISTINCT g.game_name, g.game_image, gp.platform_score, gp.platform_price, p.platform_name
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


    if top_n:
        query += " ORDER BY gp.platform_score DESC LIMIT %s"

    params = []
    if genre and genre != "All":
        params.append(genre)
    if tag and tag != "All":
        params.append(tag)
    if price:
        params.append(price * 100)
    if platform and platform != "All":
        params.append(platform)
    if top_n:
        params.append(top_n)


    cursor.execute(query, tuple(params))
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=["game_name", "game_image", "platform_score",
                                        "platform_price", "platform_name"])
    df['platform_price'] = df['platform_price'] / 100
    return df

def get_top_10_best_reviewed_games(cursor: psycopg_cursor) -> pd.DataFrame:
    """Fetch the top 10 best-reviewed games and include platform name in the title."""
    query = """
    SELECT g.game_name, g.game_image, gp.platform_score, gp.platform_price, p.platform_name
    FROM game g
    JOIN game_platform_assignment gp ON g.game_id = gp.game_id
    JOIN platform p ON gp.platform_id = p.platform_id
    ORDER BY gp.platform_score DESC
    LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=["game_name", "game_image", "platform_score",
                                        "platform_price", "platform_name"])
    df['game_name'] = df['game_name'] + " (" + df['platform_name'] + ")"
    df['platform_price'] = df['platform_price'] / 100
    return df


def get_price_filter_options() -> list[str]:
    """Returns a list of price ranges for user-friendly filtering."""
    return ["Free", "Under £10", "£10 - £50", "£50 - £100", "Above £100"]


def main():
    """Main function to manage the Streamlit app interface."""


    conn = get_connection()
    cursor = conn.cursor()


    st.markdown(
        """
        <style>
        body {
            background-color:
            color: white;
        }
        .sidebar .sidebar-content {
            background-color:
        }
        .st-bb {
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )


    genres, tags, platforms = get_genre_tag_platform_options(cursor)




    selected_genre = st.sidebar.selectbox("Genre", options=["All"] + genres)
    selected_tag = st.sidebar.selectbox("Tag", options=["All"] + tags)
    selected_platform = st.sidebar.selectbox("Platform", options=["All"] + platforms)
    price_range = st.sidebar.selectbox("Price Range", options=get_price_filter_options())




    price_mapping = {
        "Free": 0,
        "Under £10": 10,
        "£10 - £50": 50,
        "£50 - £100": 100,
        "Above £100": 300
    }


    selected_price = price_mapping[price_range]


    st.subheader("Top 10 Best Reviewed Games")
    top_games = get_top_10_best_reviewed_games(cursor)
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


    st.subheader("Best Reviewed Games by Filter")
    filtered_games = get_filtered_games(cursor, selected_genre,
                selected_tag, selected_price, selected_platform, top_n=10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='platform_score', y='game_name', data=filtered_games,
                palette="magma", ax=ax)


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


    st.subheader("Price vs Rating Scatter Plot")
    fig, ax = plt.subplots(figsize=(10, 6))


    all_games = get_filtered_games(cursor, selected_genre,
                selected_tag, selected_price, selected_platform)
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
