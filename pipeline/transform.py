"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime

from requests import get

def get_data() -> list[dict]:
    """Gets the data from extract."""
    ...


def is_valid_data(game: dict) -> bool:
    """Returns true if all the data is valid."""

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
    ...


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