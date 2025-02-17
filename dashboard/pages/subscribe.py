"""dashboard page allowing users to subscribe to newsletters"""
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
from os import environ as ENV
import streamlit as st
import boto3
from dotenv import load_dotenv
from components import dashboard_title
from data_source import get_connection, get_all_genres


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
        if sub['Protocol'] == 'email' and sub['Endpoint'] == email and sub['SubscriptionArn'] != 'PendingConfirmation' and sub['SubscriptionArn'] != 'Deleted':
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
    dashboard_title()
    st.title("Subscribe to the Newsletter")
    st.html("<marquee>Welcome to MySpace!</marquee>")
    f_name = st.text_input("First Name")
    l_name = st.text_input("Last Name")
    user_email = st.text_input("Email")
    selected_genres = st.multiselect(
        "Select Genres to Subscribe To", get_all_genres(conn))
    accepted_weekly_digest = st.checkbox(
        "Subscribe to Weekly Digest", value=True)
    st.button("Submit", on_click=lambda: subscribe_user(
        user_email, selected_genres, accepted_weekly_digest))
