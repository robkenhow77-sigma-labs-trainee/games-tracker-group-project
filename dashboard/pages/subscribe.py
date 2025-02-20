"""dashboard page allowing users to subscribe to newsletters"""
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
from os import environ as ENV
import streamlit as st
import boto3
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor


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


def sns_connect():
    """connect to sns client"""
    client = boto3.client(
        'sns',
        aws_access_key_id=ENV['AWS_ACCESS_KEY'],
        aws_secret_access_key=ENV['AWS_SECRET_ACCESS_KEY']
    )
    return client


def get_or_create_topic(client, genre):
    """fetches an existing topic. if not present, create the topic"""
    topics = client.list_topics().get('Topics', [])

    genre = genre.replace(' ', '_')

    print('SELECTED GENRE: ', genre)

    for topic in topics:
        if f'play_stream_{genre}' in topic["TopicArn"]:
            print(f"Topic '{genre}' already exists.")
            return topic["TopicArn"]

    res = client.create_topic(Name=f'play_stream_{genre.lower()}')
    print('Created new topic ', genre)

    return res['TopicArn']


def is_already_subscribed(client, email, topic_arn):
    """checks if a user's email is already subscribed to the given genre/weekly digest"""
    existing_subs = client.list_subscriptions_by_topic(
        TopicArn=topic_arn).get('Subscriptions', [])
    print('existing subs: ', existing_subs)

    for sub in existing_subs:
        if sub['Protocol'] == 'email' and sub['Endpoint'] == email and sub['SubscriptionArn'] != 'PendingConfirmation':
            print(f'{sub['Endpoint']} is an existing sub. Return True')
            return True
    return False


def subscribe_user(email, genres, weekly_digest):
    """subscribes the user to sns emailing list for genres and weekly digest"""

    if not email:
        st.error("Email is required!")

    if not genres and not weekly_digest:
        st.error("A genre or weekly digest needs to be included")

    client = sns_connect()

    if email and genres:  # if inputted a genre and email do this
        for genre in genres:
            topic_arn = get_or_create_topic(client, genre)
            if is_already_subscribed(client, email, topic_arn):
                st.info('This email is already subscribed to the following genres')
            else:
                try:
                    client.subscribe(
                        TopicArn=topic_arn,
                        Protocol="email",
                        Endpoint=email
                    )
                    st.success(
                        f'Subscription request has been sent to {email}')
                    print(f'Subscribed {email} to {genre}')
                except Exception as e:
                    st.error(f'Subscription to genre {genre} failed: {str(e)}')

    if email and weekly_digest:
        digest_topic_arn = get_or_create_topic(client, 'weekly_digest')
        if is_already_subscribed(client, email, digest_topic_arn):
            st.info('This email is already subscribed to the weekly digest')
        else:
            try:
                client.subscribe(
                    TopicArn=digest_topic_arn,
                    Protocol="email",
                    Endpoint=email
                )
                st.success(
                    'Your email has been subscribed to the weekly digest')
                print(f'Subscribed {email} to newsletter')
            except Exception as e:
                st.error(f'Subscription to newsletter failed: {e}')


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()

    st.sidebar.image("logo.png", width=100)

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css?family=Press+Start+2P&display=swap');
        
        body {
            font-family: 'Press Start 2P', cursive;
            font-size: 15px;
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
    st.markdown('<h4 style="font-family: \'Press Start 2P\', cursive; color: yellow; font-size: 30px;">Subscribe to the Newsletter</h4>',
                unsafe_allow_html=True)
    st.html("<marquee>Subscribe to receive updates on new game releases!</marquee>")
    f_name = st.text_input("First Name")
    l_name = st.text_input("Last Name")
    user_email = st.text_input("Email")
    selected_genres = st.multiselect(
        "Select Genres to Subscribe To", get_all_genres(conn))
    accepted_weekly_digest = st.checkbox(
        "Subscribe to Weekly Digest", value=True)
    st.button("Submit", on_click=lambda: subscribe_user(
        user_email, selected_genres, accepted_weekly_digest))
