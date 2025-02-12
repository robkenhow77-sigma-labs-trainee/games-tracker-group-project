"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime

from requests import get

#TODO: add age formatting and validation to this
#TODO: add ability to insert data from previous days with timedelta
#TODO: ensure logger is imported and config-ed

#TODO: write function that gets data from extract
def get_data() -> list[dict]:
    """Gets the data from extract."""
    ...


def clean_data(data: list[dict]) -> list[dict]:
    """Cleans the data extracted from the Steam scraper."""

    cleaned_data = []

    for row in data:
        if is_valid_data(row):
            cleaned_data.append(format_data(row))

    return cleaned_data


#TODO: we should put this in load (function that queries DB to see if need to add tag/genre/dev/pub)
# def find_data_to_add() -> dict:
#     """Queries the database to see what data we need to input."""

#     genres_to_add = {}
#     tags_to_add = {}
#     publishers_to_add = {}
#     developers_to_add = {}

#     #need to define these functions
#     current_genres = get_db_genres()
#     current_tags = get_db_tags()
#     current_publishers = get_db_publishers()
#     current_developers = get_db_developers()

#     #for row in cleaned_data:
#     #    for genre in genres


def is_valid_data(game: dict) -> bool:
    """Returns true if all the data is valid."""

    expected_keys = ['title', 'genres', 'publisher',
    'developer', 'tag', 'platform_score', 'platform_score',
    'platform_price', 'platform_discount', 'release_date',
    'game_image', 'age_rating']

    missing_keys = [key for key in expected_keys if key not in game.keys()]

    if missing_keys:
        logging.error("game is not a valid entry, missing keys: %s", missing_keys)
        return False

    #TODO: figure out if we want to include some invalid data.
    return (is_valid_title(game['title']) and is_valid_genres(game['genres']) and
            is_valid_publisher(game['publisher']) and is_valid_developer(game['developer']) and
            is_valid_tag(game['tag']) and is_valid_score(game['platform_score']) and
            is_valid_price(game['platform_price']) and is_valid_discount(game['platform_discount'])
            and is_valid_release(game['release_date']) and is_valid_image(game['game_image']) and
            is_valid_age(game['age_rating']))


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

        if len(genre) == 0:
            logging.error("%s is not a valid genre, cannot be empty.", genre)
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

        if len(publisher) == 0:
            logging.error("%s is not a valid publisher, cannot be empty", publisher)
            return False

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

        if len(developer) == 0:
            logging.error("%s is not a valid developer, cannot be empty", developer)
            return False

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

        if len(tag) == 0:
            logging.error("%s is not a valid tag, cannot be empty", tag)
            return False

        if len(tag) > 26:
            logging.error("%s is not a valid tag, too long.", tag)
            return False

    return True


def is_valid_score(score: str) -> bool:
    """Returns true if score is valid."""

    if not isinstance(score, str):
        logging.error("%s is not a valid score, not a string", score)
        return False

    score = score.strip()

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

    price = price.strip()

    if not price.isnumeric():
        logging.error("%s is not a valid price, not numeric.", price)
        return False

    return True


def is_valid_discount(discount: int) -> bool:
    """Returns true if discount is valid."""

    #Not on discount currently
    if discount is None:
        return True

    if not isinstance(discount, str):
        logging.error("%s is not a valid discount, not a string", discount)
        return False

    discount = discount.strip()

    if not discount.isnumeric():
        logging.error("%s is not a valid price, not numeric.", discount)
        return False

    if not 0 <= int(discount) <= 100:
        logging.error("%s is not a valid discount, not between 0 and 100.", discount)
        return False

    return True


def is_valid_release(release: str) -> bool:
    """Returns true if release is valid."""

    try:
        datetime_release = datetime.strptime(release, "%d %b, %Y")
    except:
        logging.error("%s is not in the valid release form.", release)
        return False

    if datetime.now().date() != datetime_release.date():
        logging.error("%s is not a valid date, not released today.", release)
        return False

    return True


def is_valid_image(image: str) -> bool:
    """Returns true if image is valid."""

    if not isinstance(image, str):
        logging.error("%s is not a valid image, not a string", image)
        return False

    image = image.strip()

    if len(image) > 256:
        logging.error("%s is not a valid image, url too long", image)
        return False

    if len(image) == 0:
        logging.error("%s is not a valid image, empty string", image)
        return False

    try:
        response = get(image, timeout=5)
    except Exception as e:
        logging.error("""%s is not a valid image, not loading properly.
                        Error: %s""", image, e)
        return False

    if not response.status_code == 200:
        logging.error("%s is not a valid image, not loading properly.", image)
        return False

    return True


def is_valid_age(age: str) -> bool:
    """Returns if the age conforms to PEGI standards."""

    if age is None:
        return True

    if not isinstance(age, str):
        logging.error("%s is not a valid age rating, not a string", age)
        return False

    age = age.strip()

    if age not in ['3', '7', '12', '16', '18']:
        logging.error("%s is not a valid age rating, not a standard PEGI age", age)
        return False

    return True


def format_data(game: dict) -> bool:
    """Formats all the data."""

    formatted_data = {}

    formatted_data['title'] = format_string(game['title'])
    formatted_data['genre'] = format_list(game['genres'])
    formatted_data['publisher'] = format_list(game['publisher'])
    formatted_data['developer'] = format_list(game['developer'])
    formatted_data['tag'] = format_list(game['tag'])
    formatted_data['score'] = format_integer(game['platform_score'])
    formatted_data['price'] = format_integer(game['platform_price'])
    formatted_data['discount'] = format_integer(game['platform_discount'])
    formatted_data['release'] = format_release(game['release_date'])
    formatted_data['image'] = format_string(game['game_image'])
    formatted_data['platform'] = "Steam"
    formatted_data['age_rating'] = format_string(game['age_rating'])

    return formatted_data


def format_string(string: str) -> str:
    """Formats title."""
    return string.strip().replace('%20', ' ')


def format_list(values: list[str]) -> list[str]:
    """Formats genres are valid."""

    formatted_list = []

    for value in values:
        formatted_list.append(format_string(value))

    return formatted_list


def format_integer(integer: str) -> int:
    """Formats number."""

    if isinstance(integer, str):
        integer = integer.strip()

    if integer is not None:
        return int(integer)

    return None


def format_release(release: str) -> datetime:
    """Formats release."""

    release = release.strip()

    release = format_string(release)
    return datetime.strptime(release, "%d %b, %Y")


if __name__ == "__main__":

    test_input = [{'title': 'Hearts of Iron IV',
                    'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy',
                                'Simulation', 'Strategy'],
                    'publisher': [],
                    'developer': [],
                    'tag': ['Strategy', 'World%20War%20II', 'Grand%20Strategy',
                            'War', 'Historical', 'Military',
                            'Alternate%20History', 'Multiplayer', 'Simulation',
                            'Tactical', 'Real-Time%20with%20Pause', 'Singleplayer',
                            'RTS', 'Diplomacy', 'Sandbox',
                            'Co-op', 'Strategy%20RPG', 'Competitive',
                            'Open%20World', 'Action'],
                    'platform_score': '90',
                    'platform_price': '4199',
                    'platform_discount': None,
                    'release_date': '12 Feb, 2025', 
                    'game_image':
                    'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786',
                    'age_rating': '7'}]

    print(clean_data(test_input))
