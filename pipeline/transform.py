"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime, timedelta

from requests import get

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


def is_valid_data(game: dict) -> bool:
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
            is_valid_price(game['platform_price']) and is_valid_release(game['release_date']))


def is_valid_title(title: str) -> bool:
    """Returns true if title is valid."""

    if not isinstance(title, str):
        logging.info("%s is not a valid title, not a string", title)
        return False

    title = title.strip()

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
            logging.info("%s is not a valid genre, not a list", genre)
            return False

    #genreless games are not okay
    if len(genres) == 0:
        return False

    valid_genres = []

    for genre in genres:

        if not isinstance(genre, str):
            logging.info("%s is not a valid genre, not a string", genre)
            continue

        genre = genre.strip()

        if len(genre) > 31:
            logging.info("%s is not a valid genre, too long.", genre)
            continue

        if len(genre) == 0:
            logging.info("%s is not a valid genre, cannot be empty.", genre)
            continue

        valid_genres.append(genre)

    return len(valid_genres) > 0


def is_valid_publisher(publishers: list[str]) -> bool:
    """Returns true if publishers are valid."""

    if not isinstance(publishers, list):
            logging.info("%s is not a valid publisher, not a list", publishers)
            return False

    #publisherless games are not okay
    if len(publishers) == 0:
        return False

    valid_publishers = []

    for publisher in publishers:

        if not isinstance(publisher, str):
            logging.info("%s is not a valid publisher, not a string", publisher)
            continue

        publisher = publisher.strip()

        if len(publisher) == 0:
            logging.info("%s is not a valid publisher, cannot be empty", publisher)
            continue

        if len(publisher) > 26:
            logging.info("%s is not a valid publisher, too long.", publisher)
            continue
        
        valid_publishers.append(publisher)

    return len(valid_publishers) > 0


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


        if not isinstance(developer, str):
            logging.info("%s is not a valid developer, not a string", developer)
            continue

        developer = developer.strip()

        if len(developer) == 0:
            logging.info("%s is not a valid developer, cannot be empty", developer)
            continue

        if len(developer) > 26:
            logging.info("%s is not a valid developer, too long.", developer)
            continue
    
        valid_developers.append(developer)

    return len(valid_developers) > 0


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

        if not isinstance(tag, str):
            logging.info("%s is not a valid tag, not a string", tag)
            continue

        tag = tag.strip()

        if len(tag) == 0:
            logging.info("%s is not a valid tag, cannot be empty", tag)
            continue

        if len(tag) > 26:
            logging.info("%s is not a valid tag, too long.", tag)
            continue

        valid_tags.append(tag)

    return len(valid_tags) > 0


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

    return True


def is_valid_discount(discount: int) -> bool:
    """Returns true if discount is valid."""

    #Not on discount currently
    if discount is None:
        return True

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


def is_valid_release(release: str, days_before_today_allowed=0) -> bool:
    """Returns true if release is valid."""

    try:
        datetime_release = datetime.strptime(release, "%d %b, %Y")
    except Exception as e:
        logging.info("""%s is not in the valid release form.
                                %s""", (release,e))
        return False

    earliest_allowed_date = datetime.now().date() - timedelta(days=days_before_today_allowed)

    if not (earliest_allowed_date <= datetime_release.date() <= datetime.now().date()):
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
        return True

    if not isinstance(age, str):
        logging.info("%s is not a valid age rating, not a string", age)
        return False

    age = age.strip()

    if age not in ['3', '7', '12', '16', '18']:
        logging.info("%s is not a valid age rating, not a standard PEGI age", age)
        return False

    return True


def format_data(game: dict) -> bool:
    """Formats all the data."""

    formatted_data = {}

    # Minimum required data
    formatted_data['title'] = format_string(game['title'])
    formatted_data['genres'] = format_genre_list(game['genres'])
    formatted_data['platform_price'] = format_integer(game['platform_price'])
    formatted_data['platform'] = "Steam"

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
        formatted_data['platform_score'] = None
    if is_valid_discount(game['platform_discount']):
        formatted_data['platform_discount'] = format_integer(game['platform_discount'])
    else:
        formatted_data['platform_discount'] = None
    if is_valid_release(game['release_date']):
        formatted_data['release_date'] = format_release(game['release_date'])
    else:
        formatted_data['release_date'] = None
    if is_valid_image(game['game_image']):
        formatted_data['game_image'] = format_string(game['game_image'])
    else:
        formatted_data['game_image'] = None
    if is_valid_age(game['age_rating']):
        formatted_data['age_rating'] = format_string(game['age_rating'])
    else:
        formatted_data['age_rating'] = None

    return formatted_data


def format_string(string: str) -> str:
    """Formats title."""

    if not string or not isinstance(string, str):
        return None

    return string.strip().replace('%20', ' ')


def format_genre_list(values: list[str]) -> list[str]:
    """Formats genres which are valid."""

    if not values or not isinstance(values, list):
        return []

    formatted_list = []

    for value in values:
           if isinstance(value, str) and is_valid_genres([value]):
               formatted_list.append(format_string(value))

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
               formatted_list.append(format_string(value))

    return formatted_list


def format_tag_list(values: list[str]) -> list[str]:
    """Formats genres which are valid."""

    if not values or not isinstance(values, list):
        return []

    formatted_list = []

    for value in values:
           if isinstance(value, str) and is_valid_tag([value]):
               formatted_list.append(format_string(value))

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
        return formatted_release
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
                            'Open%20World', 'Action'],
                    'platform_score': '90',
                    'platform_price': '4199',
                    'platform_discount': None,
                    'release_date': '12 Feb, 2025', 
                    'game_image':
                    'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786',
                    'age_rating': '7'}]

    print(clean_data(test_input))

    valid_games = [{'title': 'Hearts of Iron IV', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy', 'Simulation', 'Strategy'], 'publisher': [], 'developer': [], 'tag': ['Strategy', 'World%20War%20II', 'Grand%20Strategy', 'War', 'Historical', 'Military', 'Alternate%20History', 'Multiplayer', 'Simulation', 'Tactical', 'Real-Time%20with%20Pause', 'Singleplayer', 'RTS', 'Diplomacy', 'Sandbox', 'Co-op', 'Strategy%20RPG', 'Competitive', 'Open%20World', 'Action'], 'platform_score': '90', 'platform_price': '4199', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786', 'age_rating': '7'}]

    valid_game = valid_games[0]

    list_of_games_missing_value = [
    {key:(False if (key == changing_key and changing_key not in ['title', 'genre', 'price', 'platform']) else value)
    for key, value in valid_game.items()} for changing_key in valid_game]

    # Generate a list of games but how it should look after formatting.
    list_of_games_missing_value_formatted = [
    {key:(None if (key == changing_key and changing_key not in ['title', 'genre', 'price', 'platform']) else value)
    for key, value in valid_game.items()} for changing_key in valid_game]

    print("\n\n\n")
    print(list_of_games_missing_value)
    print("\n\n\n")
    print(list_of_games_missing_value_formatted)
