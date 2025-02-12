"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime

from requests import get

#TODO: write this
def get_data() -> list[dict]:
    """Gets the data from extract."""
    ...

#TODO: write this
def clean_data(data: list[dict]) -> list[dict]:
    """Cleans the data extracted from the Steam scraper."""

    cleaned_data = []

    for row in data:
        if is_valid_data(row):
            cleaned_data.append(format_data(row))


#TODO: write this
def find_data_to_add() -> dict:
    """Queries the database to see what data we need to input."""

    genres_to_add = {}
    tags_to_add = {}
    publishers_to_add = {}
    developers_to_add = {}

    #need to define these functions
    current_genres = get_db_genres()
    current_tags = get_db_tags()
    current_publishers = get_db_publishers()
    current_developers = get_db_developers()

    #for row in cleaned_data:
    #    for genre in genres


def is_valid_data(game: dict) -> bool:
    """Returns true if all the data is valid."""

    #TODO: figure out if we want to include some invalid data.
    return (is_valid_title(game['title']) and is_valid_genres(game['genres']) and
            is_valid_publisher(game['publisher']) and is_valid_developer(game['developer']) and
            is_valid_tag(game['tag']) and is_valid_score(game['platform_score']) and 
            is_valid_price(game['platform_price']) and is_valid_discount(game['platform_discount']) and
            is_valid_release(game['release_date']) and is_valid_image(game['game_image']))


def is_valid_title(title: str) -> bool:
    """Returns true if title is valid."""

    if not isinstance(title, str):
        logging.error("%s is not a valid title, not a string", title)
        return False

    title = title.strip()

    if len(title) > 101:
        logging.error("%s is not a valid title, too long", title)
        return False

    if len(title) == 0:
        logging.error("%s is not a valid title, empty title", title)
        return False

    return True


def is_valid_genres(genres: list[str]) -> bool:
    """Returns true if genres are valid."""

    #genreless games are okay
    if len(genres) == 0:
        return True


    for genre in genres:

        if not isinstance(genre, str):
            logging.error("%s is not a valid genre, not a string", genre)
            return False

        genre = genre.strip()

        if len(genre) > 31:
            logging.error("%s is not a valid genre, too long.", genre)
            return False

    return True


def is_valid_publisher(publishers: list[str]) -> bool:
    """Returns true if publishers are valid."""

    #publisherless games are okay
    if len(publishers) == 0:
        return True

    for publisher in publishers:

        if not isinstance(publisher, str):
            logging.error("%s is not a valid publisher, not a string", publisher)
            return False

        publisher = publisher.strip()

        if len(publisher) > 26:
            logging.error("%s is not a valid publisher, too long.", publisher)
            return False

    return True


def is_valid_developer(developers: list[str]) -> bool:
    """Returns true if developers are valid."""

    #developerless games are okay
    if len(developers) == 0:
        return True

    for developer in developers:

        if not isinstance(developer, str):
            logging.error("%s is not a valid developer, not a string", developer)
            return False

        developer = developer.strip()

        if len(developer) > 26:
            logging.error("%s is not a valid developer, too long.", developer)
            return False

    return True


def is_valid_tag(tags: list[str]) -> bool:
    """Returns true if tags are valid."""

    #tagless games are okay
    if len(tags) == 0:
        return True

    for tag in tags:

        if not isinstance(tag, str):
            logging.error("%s is not a valid tag, not a string", tag)
            return False

        tag = tag.strip()

        if len(tag) > 26:
            logging.error("%s is not a valid tag, too long.", tag)
            return False

    return True


def is_valid_score(score: int) -> bool:
    """Returns true if score is valid."""

    if not isinstance(score, str):
        logging.error("%s is not a valid score, not a string", score)
        return False

    if not score.isnumeric():
        logging.error("%s is not a valid score, not an integer.", score)
        return False

    if not 0 <= int(score) <= 100:
        logging.error("%s is not a valid score, not between 0 and 100.", score)
        return False

    return True


def is_valid_price(price: int) -> bool:
    """Returns true if price is valid."""

    if not isinstance(price, str):
        logging.error("%s is not a valid price, not a string", price)
        return False

    if not price.isnumeric():
        logging.error("%s is not a valid price, not numeric.", price)
        return False

    return True


def is_valid_discount(discount: int) -> bool:
    """Returns true if discount is valid."""

    if not isinstance(discount, str):
        logging.error("%s is not a valid discount, not a string", discount)
        return False

    if not discount.isnumeric() or None:
        logging.error("%s is not a valid price, not numeric.", discount)
        return False

    return True


def is_valid_release(release: str) -> bool:
    """Returns true if release is valid."""

    try:
        datetime_release = datetime.strptime(release, "%d %b, %Y")
    except:
        logging.error("%s is not in the valid release form.", release)
        return False

    if not datetime.now().date() == datetime_release:
        logging.error("%s is not a valid date, not released today.", release)
        return False

    return True


def is_valid_image(image: str) -> bool:
    """Returns true if image is valid."""

    try:
        response = get(image)
    except Exception as e:
        logging.error("""%s is not a valid image, not loading properly.
                            Error: %s""", (image, e))

    if not response.status_code == 200:
        logging.error("%s is not a valid image, not loading properly.", image)
        return False

    return True


def format_data(game: dict) -> bool:
    """Formats all the data."""

    formatted_data = {}

    formatted_data['title'] = format_title(game['title'])
    formatted_data['genre'] = format_genres(game['genre'])
    formatted_data['publisher'] = format_publisher(game['publisher'])
    formatted_data['developer'] = format_developer(game['developer'])
    formatted_data['tag'] = format_tag(game['tag'])
    formatted_data['score'] = format_score(game['score'])
    formatted_data['price'] = format_price(game['price'])
    formatted_data['discount'] = format_discount(game['discount'])
    formatted_data['release'] = format_release(game['release'])
    formatted_data['image'] = format_image(game['image'])

    return formatted_data


def format_title(title: str) -> bool:
    """Formats title."""
    ...


def format_genres(genre: list[str]) -> bool:
    """Formats genres are valid."""
    ...


def format_publisher(publisher: list[str]) -> bool:
    """Formats publishers are valid."""
    ...


def format_developer(developer: list[str]) -> bool:
    """Formats developers are valid."""
    ...


def format_tag(tag: list[str]) -> bool:
    """Formats tags are valid."""
    ...


def format_score(score: int) -> bool:
    """Formats score."""
    ...


def format_price(price: int) -> bool:
    """Formats price."""
    ...


def format_discount(discount: int) -> bool:
    """Formats discount."""
    ...


def format_release(release: str) -> bool:
    """Formats release."""
    ...


def format_image(image: str) -> bool:
    """Formats image."""
    ...
