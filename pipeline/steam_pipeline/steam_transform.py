"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime, timedelta
import urllib.parse

from requests import get

#TODO: ensure logger is imported and config-ed

def clean_data(data: list[dict], target_date=None) -> list[dict]:
    """Cleans the data extracted from the Steam scraper."""

    if target_date is not None:
        days_to_accept = turn_date_to_num_days(target_date)
    else:
        days_to_accept = 0

    cleaned_data = []

    for row in data:
        if is_valid_data(row, days_to_accept):
            cleaned_data.append(format_data(row, days_to_accept))

    return cleaned_data


def turn_date_to_num_days(target_date: str) -> int:
    """Returns the number of days ago """

    input_date = datetime.strptime(target_date, "%d %b, %Y").date()
    today = datetime.now().date()
    return today-input_date


def is_valid_data(game: dict, days_to_accept=0) -> bool:
    """Returns true if all the data is valid."""

    expected_keys = ['title', 'genres', 'publisher',
    'developer', 'tag', 'platform_score', 'platform_score',
    'platform_price', 'platform_discount', 'release_date',
    'game_image', 'age_rating']

    missing_keys = [key for key in expected_keys if key not in game.keys()]

    if missing_keys:
        logging.info("game is not a valid entry, missing keys: %s", missing_keys)
        return False

    return (is_valid_title(game['title']) and is_valid_genres(game['genres']) and
            is_valid_price(game['platform_price']) and
            is_valid_release(game['release_date'], days_to_accept))


def is_valid_title(title: str) -> bool:
    """Returns true if title is valid."""

    if not isinstance(title, str):
        logging.info("%s is not a valid title, not a string", title)
        return False

    title = title.strip().replace('%20', ' ')

    if len(title) > 101:
        logging.info("%s is not a valid title, too long", title)
        return False

    if len(title) == 0:
        logging.info("%s is not a valid title, empty title", title)
        return False

    return True


def is_valid_genres(genres: list[str]) -> bool:
    """Returns true if genres are valid."""

    if not isinstance(genres, list):
        logging.info("%s is not a valid genre, not a list", genres)
        return False

    #genreless games are not okay
    if len(genres) == 0:
        return False

    valid_genres = []

    for genre in genres:

        if is_valid_genre(genre):
            valid_genres.append(genre)

    return len(valid_genres) > 0


def is_valid_genre(genre: str) -> bool:
    """Returns true if genre is valid."""

    if not isinstance(genre, str):
        logging.info("%s is not a valid genre, not a string", genre)
        return False

    genre = genre.strip()

    if len(genre) > 51:
        logging.info("%s is not a valid genre, too long.", genre)
        return False

    if len(genre) == 0:
        logging.info("%s is not a valid genre, cannot be empty.", genre)
        return False

    return True


def is_valid_publisher(publishers: list[str]) -> bool:
    """Returns true if publishers are valid."""

    if not isinstance(publishers, list):
        logging.info("%s is not a valid publisher, not a list", publishers)
        return False

    # publisherless games are not okay
    if len(publishers) == 0:
        return False

    valid_publishers = []

    for publisher in publishers:

        if is_valid_pub(publisher):
            valid_publishers.append(publisher)

    return len(valid_publishers) > 0


def is_valid_pub(publisher: str) -> bool:
    """Returns true if publisher is valid."""

    if not isinstance(publisher, str):
        logging.info("%s is not a valid publisher, not a string", publisher)
        return False

    publisher = publisher.strip().replace('%20', ' ')

    if len(publisher) == 0:
        logging.info("%s is not a valid publisher, cannot be empty", publisher)
        return False

    if len(publisher) > 151:
        logging.info("%s is not a valid publisher, too long.", publisher)
        return False

    return True


def is_valid_developer(developers: list[str]) -> bool:
    """Returns true if developers are valid."""

    if not isinstance(developers, list):
        logging.info("%s is not a valid developers, not a list", developers)
        return False

    #developerless games are not okay
    if len(developers) == 0:
        return False

    valid_developers = []

    for developer in developers:

        if is_valid_dev(developer):
            valid_developers.append(developer)

    return len(valid_developers) > 0


def is_valid_dev(developer: str) -> bool:
    """Checks a single developer."""

    if not isinstance(developer, str):
        logging.info("%s is not a valid developer, not a string", developer)
        return False

    developer = developer.strip().replace('%20', ' ')

    if len(developer) == 0:
        logging.info("%s is not a valid developer, cannot be empty", developer)
        return False

    if len(developer) > 151:
        logging.info("%s is not a valid developer, too long.", developer)
        return False

    return True


def is_valid_tag(tags: list[str]) -> bool:
    """Returns true if tags are valid."""

    if not isinstance(tags, list):
        logging.info("%s is not a valid tag, not a list", tags)
        return False

    #tagless games are not okay
    if len(tags) == 0:
        return False

    valid_tags = []

    for tag in tags:

        if is_valid_single_tag(tag):
            valid_tags.append(tag)

    return len(valid_tags) > 0


def is_valid_single_tag(tag: str) -> bool:
    """
    Returns true if the single tag is valid, false if otherwise.
    """

    if not isinstance(tag, str):
        logging.info("%s is not a valid tag, not a string", tag)
        return False

    tag = tag.strip().replace('%20', ' ')

    if len(tag) == 0:
        logging.info("%s is not a valid tag, cannot be empty", tag)
        return False

    if len(tag) > 51:
        logging.info("%s is not a valid tag, too long.", tag)
        return False

    return True


def is_valid_score(score: str) -> bool:
    """Returns true if score is valid."""

    if not isinstance(score, str):
        logging.info("%s is not a valid score, not a string", score)
        return False

    score = score.strip()

    if not score.isnumeric():
        logging.info("%s is not a valid score, not an integer.", score)
        return False

    if not 0 <= int(score) <= 100:
        logging.info("%s is not a valid score, not between 0 and 100.", score)
        return False

    return True


def is_valid_price(price: int) -> bool:
    """Returns true if price is valid."""

    if not isinstance(price, str):
        logging.info("%s is not a valid price, not a string", price)
        return False

    price = price.strip()

    if not price.isnumeric():
        logging.info("%s is not a valid price, not numeric.", price)
        return False

    return 0 <= int(price) <= 32767


def is_valid_discount(discount: int) -> bool:
    """Returns true if discount is valid."""

    #Not on discount currently
    if discount is None:
        return False

    if not isinstance(discount, str):
        logging.info("%s is not a valid discount, not a string", discount)
        return False

    discount = discount.strip()

    if not discount.isnumeric():
        logging.info("%s is not a valid price, not numeric.", discount)
        return False

    if not 0 <= int(discount) <= 100:
        logging.info("%s is not a valid discount, not between 0 and 100.", discount)
        return False

    return True


def is_valid_release(release: str,
                     days_before_today_allowed=0) -> bool:
    """Returns true if release is valid."""

    try:
        datetime_release = datetime.strptime(release, "%d %b, %Y")
    except Exception as e:
        logging.info("""%s is not in the valid release form.
                                %s""", release, e)
        return False

    earliest_allowed_date = datetime.now().date() - timedelta(days=days_before_today_allowed)

    if not earliest_allowed_date <= datetime_release.date() <= datetime.now().date():
        logging.info("%s is not within the allowed release date range.", release)
        return False

    return True


def is_valid_image(image: str) -> bool:
    """Returns true if image is valid."""

    if not isinstance(image, str):
        logging.info("%s is not a valid image, not a string", image)
        return False

    image = image.strip()

    if len(image) > 256:
        logging.info("%s is not a valid image, url too long", image)
        return False

    if len(image) == 0:
        logging.info("%s is not a valid image, empty string", image)
        return False

    try:
        response = get(image, timeout=5)
    except Exception as e:
        logging.info("""%s is not a valid image, not loading properly.
                        Error: %s""", image, e)
        return False

    if not response.status_code == 200:
        logging.info("%s is not a valid image, not loading properly.", image)
        return False

    return True


def is_valid_age(age: str) -> bool:
    """Returns if the age conforms to PEGI standards."""

    if age is None:
        return False

    if not isinstance(age, str):
        logging.info("%s is not a valid age rating, not a string", age)
        return False

    age = age.strip()

    if age not in ['3', '7', '12', '16', '18']:
        logging.info("%s is not a valid age rating, not a standard PEGI age", age)
        return False

    return True


def format_data(game: dict, days_to_accept=0) -> bool:
    """Formats all the data."""

    formatted_data = {}

    # Minimum required data
    formatted_data['title'] = format_string(game['title'])
    formatted_data['genres'] = format_genre_list(game['genres'])
    formatted_data['platform_price'] = format_integer(game['platform_price'])
    formatted_data['platform'] = "Steam"
    formatted_data['link'] = game['link']

    # Optional data formatting
    if is_valid_publisher(game['publisher']):
        formatted_data['publisher'] = format_publisher_list(game['publisher'])
    else:
        formatted_data['publisher'] = []
    if is_valid_developer(game['developer']):
        formatted_data['developer'] = format_developer_list(game['developer'])
    else:
        formatted_data['developer'] = []
    if is_valid_tag(game['tag']):
        formatted_data['tag'] = format_tag_list(game['tag'])
    else:
        formatted_data['tag'] = []
    if is_valid_score(game['platform_score']):
        formatted_data['platform_score'] = format_integer(game['platform_score'])
    else:
        formatted_data['platform_score'] = -1
    if is_valid_discount(game['platform_discount']):
        formatted_data['platform_discount'] = format_integer(game['platform_discount'])
    else:
        formatted_data['platform_discount'] = 0
    if is_valid_release(game['release_date'], days_to_accept):
        formatted_data['release_date'] = format_release(game['release_date'])
    else:
        formatted_data['release_date'] = None
    if is_valid_image(game['game_image']):
        formatted_data['game_image'] = format_string(game['game_image'])
    else:
        formatted_data['game_image'] = "N/A"
    if is_valid_age(game['age_rating']):
        formatted_data['age_rating'] = "PEGI " + format_string(game['age_rating'])
    else:
        formatted_data['age_rating'] = "Not Assigned"

    formatted_data = format_nsfw(formatted_data)

    return formatted_data


def format_nsfw(data: dict) -> dict:
    """Adds a NSFW tag to a game"""

    nsfw_tags = ['Hentai', 'Mature', 'Gore', 'Nudity', 'NSFW', 'Sexual Content']

    if any(tag in data.get('tag', []) for tag in nsfw_tags) or any(genre in data.get('genres', []) for genre in nsfw_tags):
        data['NSFW'] = True
    
    else:
        data['NSFW'] = False
    
    return data


def format_string(string: str) -> str:
    """Formats title."""

    if not string or not isinstance(string, str):
        return None

    string = string.strip()
    string = urllib.parse.unquote(string)

    return string


def format_genre_list(values: list[str]) -> list[str]:
    """Formats genres which are valid."""

    if not values or not isinstance(values, list):
        return []

    formatted_list = []

    for value in values:
        if isinstance(value, str) and is_valid_genres([value]):
            formatted_list.append(format_string(value).replace(',',''))

    return formatted_list


def format_developer_list(values: list[str]) -> list[str]:
    """Formats genres which are valid."""

    if not values or not isinstance(values, list):
        return []

    formatted_list = []

    for value in values:
        if isinstance(value, str) and is_valid_developer([value]):
            formatted_list.append(format_string(value))

    return formatted_list


def format_publisher_list(values: list[str]) -> list[str]:
    """Formats genres which are valid."""

    if not values or not isinstance(values, list):
        return []

    formatted_list = []

    for value in values:
        if isinstance(value, str) and is_valid_publisher([value]):
            formatted_list.append(format_string(value).replace(',',''))

    return formatted_list


def format_tag_list(values: list[str]) -> list[str]:
    """Formats genres which are valid."""

    if not values or not isinstance(values, list):
        return []

    formatted_list = []

    for value in values:
        if isinstance(value, str) and is_valid_tag([value]):
            formatted_list.append(format_string(value).replace(',',''))

    return formatted_list


def format_integer(integer: str) -> int:
    """Formats number."""

    if isinstance(integer, str):
        integer = integer.strip()

    if integer and integer.isdigit():  # Ensure it's numeric
        return int(integer)

    return None


def format_release(release: str) -> datetime:
    """Formats release."""

    if not release or not isinstance(release, str):
        return None

    release = release.strip()

    try:
        formatted_release = datetime.strptime(release, "%d %b, %Y")
        return formatted_release.date()
    except ValueError:
        return None


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
                            'Open%20World', 'Action','Nudity,'],
                    'platform_score': '90',
                    'platform_price': '4199',
                    'platform_discount': None,
                    'release_date': '17 Feb, 2025', 
                    'game_image':
                    'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786',
                    'age_rating': '7',
                    'link': 'https://store.steampowered.com/app/394360/Hearts_of_Iron_IV/'}]

    print(clean_data(test_input))
