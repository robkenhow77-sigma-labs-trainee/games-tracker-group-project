"""dashboard page allowing users to subscribe to newsletters"""
import streamlit as st
import boto3
from os import environ as ENV
from dotenv import load_dotenv
from components import dashboard_title


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

    for topic in topics:
        if genre in topic["TopicArn"]:
            print(f"Topic '{genre}' already exists.")
            return topic["TopicArn"]
    
    res = client.create_topic(Name = f'play_stream_{genre}')
    print('Created new topic ', genre)
    
    return res['TopicArn']


def subscribe_user(email, genre):
    """subscribes the user to sns emailing list"""

    if not email or not genre:
        st.error("Email and genre are required!")
        return

    client = sns_connect()

    topic_arn = get_or_create_topic(client, genre)
    try:
        res = client.subscribe(
            TopicArn=topic_arn,
            Protocol="email",
            Endpoint=email
        )
        st.success(f'Subscription request has been sent to {email}')
        print(f'Subscribed {email} to {genre}')
    except Exception as e:
        st.error(f'Subscription failed: {str(e)}')

    return res


if __name__ == "__main__":
    load_dotenv()
    dashboard_title()
    st.title("Subscribe to the Newsletter")
    st.html("<marquee>Welcome to MySpace!</marquee>")
    f_name = st.text_input("First Name")
    l_name = st.text_input("Last Name")
    email = st.text_input("Email")
    genre = st.text_input("Genre")
    
    st.button("Submit", on_click=lambda: subscribe_user(email, genre.lower()))