"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime, timedelta

from requests import get

DAYS_BEFORE_TODAY_THAT_WILL_BE_ACCEPTED = 0

#TODO: ensure logger is imported and config-ed

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

    return int(price) >= 0


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


def is_valid_release(release: str,
                     days_before_today_allowed=DAYS_BEFORE_TODAY_THAT_WILL_BE_ACCEPTED) -> bool:
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
                            'Open%20World', 'Action'],
                    'platform_score': '90',
                    'platform_price': '4199',
                    'platform_discount': None,
                    'release_date': '12 Feb, 2025', 
                    'game_image':
                    'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786',
                    'age_rating': '7'}]

    Data = [{'title': 'Sancticide', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Indie', 'RPG', 'Early%20Access'], 'publisher': ['Sylen%20Studio'], 'developer': ['Sylen%20Studio'], 'tag': ['Action%20RPG', 'Roguelite', 'Souls-like', 'Difficult', 'Third%20Person', 'Action%20Roguelike', 'Action', 'Hack%20and%20Slash', 'Dark%20Fantasy', 'Post-apocalyptic', 'Magic', 'RPG', 'Early%20Access', 'Atmospheric', 'Violent', 'Combat', 'Singleplayer', 'Dark', 'Lore-Rich', 'Swordplay'], 'platform_score': None, 'platform_price': '1429', 'platform_discount': '10', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2635050/header.jpg?t=1739379785', 'age_rating': None}, {'title': 'Going for Nuts', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Action', 'Adventure', 'Casual', 'Indie'], 'publisher': ['Crazy%20Mage'], 'developer': ['Crazy%20Mage'], 'tag': ['Side%20Scroller', '2D%20Platformer', 'Platformer', 'Arcade', '2D', 'Cute', 'Comic%20Book', 'Relaxing', 'Action', 'Funny', 'Controller', 'Casual', 'Hand-drawn', 'Pixel%20Graphics', 'Fantasy', 'Family%20Friendly', 'Adventure', 'Comedy', 'Retro', 'Old%20School'], 'platform_score': None, 'platform_price': '249', 'platform_discount': '15', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3489520/header.jpg?t=1739376452', 'age_rating': None}, {'title': 'CyberCook', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Action', 'Adventure', 'Indie', 'RPG'], 'publisher': [], 'developer': [], 'tag': ['Exploration', 'Cyberpunk', 'Cooking', 'Atmospheric', 'Psychological%20Horror', 'Retro', 'Detective', 'Horror', 'Surreal', 'Narration', 'Story%20Rich', 'Abstract', 'Lovecraftian', 'Mystery', 'Physics', 'Old%20School', 'Philosophical', 'Sci-fi', 'Investigation', 'Crime'], 'platform_score': None, 'platform_price': '749', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3366140/header.jpg?t=1739376181', 'age_rating': None}, {'title': "Night at Grandma's", 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure', 'Casual', 'Indie'], 'publisher': [], 'developer': ['ToQly'], 'tag': ['Adventure', 'Survival%20Horror', 'Horror', 'Puzzle', 'Walking%20Simulator', '3D', 'First-Person', 'Realistic', 'Atmospheric', 'Crafting', 'Dark', 'Mystery', 'Stealth', 'Surreal', 'Casual', 'Inventory%20Management', 'Linear', 'Perma%20Death', 'PvE', 'Singleplayer'], 'platform_score': None, 'platform_price': '499', 'platform_discount': '20', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3320780/header.jpg?t=1739375811', 'age_rating': None}, {'title': "Jon's Jigsaw Puzzle", 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual', 'Indie'], 'publisher': ['Jon'], 'developer': ['Jon'], 'tag': ['Casual', 'Singleplayer', 'Puzzle', 'Moddable', 'Relaxing', '2D', 'Minimalist', 'Indie', 'Retro'], 'platform_score': None, 'platform_price': '249', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3485480/header.jpg?t=1739374976', 'age_rating': None}, {'title': 'Sunny Shores Coaster Ride', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Simulation', 'Action', 'Adventure', 'Casual', 'Indie', 'Simulation'], 'publisher': ['Land%20Rays%20Studio'], 'developer': ['Land%20Rays%20Studio'], 'tag': ['Simulation', 'Casual', 'Action-Adventure', 'Atmospheric', 'Colorful', 'Singleplayer', 'Action', 'Adventure', 'Indie'], 'platform_score': None, 'platform_price': '249', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3472030/header.jpg?t=1739374850', 'age_rating': None}, {'title': 'Leafscape', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual'], 'publisher': ['Dagrooms'], 'developer': ['Dagrooms'], 'tag': ['Casual', 'Relaxing', '2D', 'Top-Down', 'Atmospheric', 'Physics', 'Singleplayer', 'Farming%20Sim', 'Exploration', 'Clicker', 'Collectathon', 'Colorful'], 'platform_score': None, 'platform_price': '429', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3487850/header.jpg?t=1739373504', 'age_rating': None}, {'title': 'Urban Myth Dissolution Center', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure'], 'publisher': [], 'developer': ['Hakababunko'], 'tag': ['Adventure', 'Visual%20Novel', 'Exploration', 'Singleplayer', '2D', 'Psychological%20Horror', 'Drama', 'Story%20Rich', 'Mystery', '2D%20Platformer', 'Well-Written', 'Text-Based', 'Pixel%20Graphics', 'Illuminati', 'Horror', 'Supernatural', 'Point%20%26%20Click', 'Detective', 'Choose%20Your%20Own%20Adventure', 'Anime'], 'platform_score': None, 'platform_price': '1499', 'platform_discount': '10', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2089600/header.jpg?t=1739373880', 'age_rating': None}, {'title': 'Apocalypse Island', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Early%20Access', 'Action', 'Adventure', 'Free%20to%20Play', 'Early%20Access'], 'publisher': [], 'developer': [], 'tag': ['Survival', 'Zombies', 'Action', 'Post-apocalyptic', '3D', 'Adventure', 'Action-Adventure', 'Singleplayer', 'First-Person', 'Early%20Access', 'Sandbox', 'Exploration', 'Crafting', 'Open%20World', 'Multiple%20Endings', 'Free%20to%20Play'], 'platform_score': None, 'platform_price': None, 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3274800/header.jpg?t=1739371794', 'age_rating': None}, {'title': 'zu xing', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Simulation', 'Adventure', 'Casual', 'Indie', 'Simulation'], 'publisher': ['Archor%20Games'], 'developer': ['Archor%20Wright'], 'tag': ['Adventure', 'Casual', 'Simulation', 'Colony%20Sim', 'Side%20Scroller', '3D', 'Agriculture', 'Conversation', 'Indie', 'Singleplayer'], 'platform_score': None, 'platform_price': '089', 'platform_discount': '30', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3484470/header.jpg?t=1739378501', 'age_rating': None}, {'title': 'WonderLang Portuguese', 'genres': ['Free%20to%20Play', 'Early%20Access', 'RPG', 'Casual', 'Indie', 'RPG'], 'publisher': ['bair%20games'], 'developer': ['bair%20games'], 'tag': ['Casual', 'RPG', 'Adventure', 'Education', 'JRPG', 'Word%20Game', 'Exploration', 'Spelling', 'Typing', '2D', 'Anime', 'Cartoon', 'Cartoony', 'Cute', 'Top-Down', '1980s', '1990%27s', 'Family%20Friendly', 'Fantasy', 'Funny'], 'platform_score': None, 'platform_price': '2099', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3456730/header.jpg?t=1739376249', 'age_rating': None}, {'title': 'Youtopia', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Simulation', 'Adventure', 'Casual', 'Indie', 'Simulation'], 'publisher': ['Archor%20Games'], 'developer': ['Archor%20Wright'], 'tag': ['Adventure', 'Casual', 'Simulation', 'Life%20Sim', 'Collectathon', '3D', 'Atmospheric', 'Choices%20Matter', 'Indie', 'Singleplayer'], 'platform_score': None, 'platform_price': '089', 'platform_discount': '30', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3491850/header.jpg?t=1739378459', 'age_rating': None}, {'title': 'Backrooms: The Yellow Dream', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action'], 'publisher': ['Crow%20Games'], 'developer': ['Crow%20Games'], 'tag': ['Action', 'Action-Adventure', 'Shooter', 'Hero%20Shooter', 'First-Person', 'Supernatural', 'Thriller', 'Surreal', 'Hacking', 'Survival%20Horror', 'Building', 'Horror', 'Psychological%20Horror', 'Multiple%20Endings', 'Inventory%20Management', 'Perma%20Death', 'Time%20Manipulation', 'Combat', 'Crafting', 'Base%20Building'], 'platform_score': None, 'platform_price': '429', 'platform_discount': '10', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3469140/header.jpg?t=1739368781', 'age_rating': None}, {'title': "The Seabed's Shining Star", 'genres': ['Free%20to%20Play', 'Early%20Access', 'Free%20to%20Play', 'Casual', 'Indie', 'Free%20to%20Play'], 'publisher': [], 'developer': [], 'tag': ['Visual%20Novel', 'Hand-drawn', 'Story%20Rich', 'Free%20to%20Play', 'Short', 'Text-Based', 'Casual', 'Anime', 'Female%20Protagonist', 'Relaxing', 'Modern', 'Indie', 'Mythology', 'Singleplayer', 'Colorful', 'Cute', 'Atmospheric', 'Conversation'], 'platform_score': None, 'platform_price': 'Free To Play!', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3401890/header.jpg?t=1739366355', 'age_rating': None}, {'title': 'Super Jagger Bomb 2: Go East', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Casual', 'Indie'], 'publisher': ['Eastasiasoft%20Limited'], 'developer': ['CheapeeSoft%20Games', 'Eastasiasoft%20Limited'], 'tag': ['Action', 'Casual', 'Platformer', 'Arcade', '2.5D', 'Family%20Friendly', 'Score%20Attack', 'Old%20School', 'Indie', 'Retro', 'Singleplayer'], 'platform_score': None, 'platform_price': '429', 'platform_discount': '20', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3360930/header.jpg?t=1739365813', 'age_rating': None}, {'title': 'Evaluate', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual', 'Racing'], 'publisher': ['Evaluate'], 'developer': ['Evaluate'], 'tag': ['Casual', 'Racing', 'Action%20Roguelike', 'RTS', 'Pixel%20Graphics', 'Moddable', 'Singleplayer'], 'platform_score': None, 'platform_price': '2950', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3459910/header.jpg?t=1739362856', 'age_rating': None}, {'title': 'Fractious', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual', 'RPG'], 'publisher': ['Fractious'], 'developer': ['Fractious'], 'tag': ['RPG', 'Casual', 'Interactive%20Fiction', 'RTS', 'Top-Down%20Shooter', 'Action%20Roguelike', 'Pixel%20Graphics', 'FMV', 'LGBTQ%2B', 'Singleplayer'], 'platform_score': None, 'platform_price': '2499', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3459920/header.jpg?t=1739362857', 'age_rating': None}, {'title': 'IcoNick Duster - Planets Defender', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual'], 'publisher': ['ima%20shouganai'], 'developer': ['ima%20shouganai'], 'tag': ['Casual', 'Arcade', 'Shooter', 'On-Rails%20Shooter', 'Shoot%20%27Em%20Up', '2D', 'Colorful', 'Pixel%20Graphics', '1990%27s', 'Sci-fi', 'Funny', 'Space', 'Aliens', 'Futuristic', 'Family%20Friendly', 'Retro', 'Vehicular%20Combat', 'PvE', 'Singleplayer'], 'platform_score': None, 'platform_price': '850', 'platform_discount': '40', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3472510/header.jpg?t=1739362766', 'age_rating': None}, {'title': 'Eternal Rifts', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure', 'Indie', 'Massively%20Multiplayer', 'RPG', 'Strategy'], 'publisher': ['Montece%20Gaming'], 'developer': ['Montece%20Gaming'], 'tag': ['Adventure', 'Strategy', 'Trading%20Card%20Game', 'Turn-Based%20Strategy', 'Card%20Game', 'Tabletop', 'Exploration', 'Creature%20Collector', 'Singleplayer', 'Multiplayer', 'Hidden%20Object', 'Turn-Based%20Tactics', '2D', '3D', 'Pixel%20Graphics', 'Hand-drawn', 'Futuristic', 'Stylized', 'Colorful', 'eSports'], 'platform_score': None, 'platform_price': '249', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3212880/header.jpg?t=1739361658', 'age_rating': None}, {'title': 'Sweet Tooth', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Casual', 'Indie'], 'publisher': ['Blind%20Eye%20Studios%2C%20LLC'], 'developer': ['Blind%20Eye%20Studios%2C%20LLC'], 'tag': ['Action', 'Casual', 'Arcade', 'Beat%20%27em%20up', 'Hack%20and%20Slash', '3D', 'Cartoony', 'Colorful', 'Third%20Person', 'Atmospheric', 'Family%20Friendly', 'Fantasy', 'Loot', 'Supernatural', 'Combat', 'Controller', 'PvE', 'Singleplayer', 'Indie'], 'platform_score': None, 'platform_price': '850', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3274470/header.jpg?t=1739361570', 'age_rating': None}, {'title': 'Aria Skies', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Free%20to%20Play', 'Action', 'Indie', 'Free%20to%20Play'], 'publisher': [], 'developer': [], 'tag': ['PvP', '2D%20Fighter', '2.5D', 'Action', 'Stylized', 'Local%20Multiplayer', 'Indie', 'Free%20to%20Play', 'Cartoony', 'Combat', 'Multiplayer', 'Third%20Person', 'Fighting', 'Controller'], 'platform_score': None, 'platform_price': 'Free To Play!', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2984630/header.jpg?t=1739361504', 'age_rating': None}, {'title': 'BallQuizzle', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual', 'Early%20Access'], 'publisher': [], 'developer': [], 'tag': ['Puzzle%20Platformer', 'Trivia', 'Puzzle', 'Casual', '3D%20Platformer', 'Logic', 'Family%20Friendly', 'Arcade', '3D', 'Physics', 'Early%20Access', 'Linear', 'Singleplayer'], 'platform_score': None, 'platform_price': '169', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3407180/header.jpg?t=1739359890', 'age_rating': None}, {'title': 'My Gambian Boyfriend', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Adventure', 'Casual', 'Indie', 'RPG', 'Simulation', 'Strategy'], 'publisher': ['Alright%20Peaches%20Studio'], 'developer': ['Alright%20Peaches%20Studio'], 'tag': ['Casual', 'Simulation', 'Life%20Sim', '2D%20Platformer', '2D', 'Anime', 'Cute', '1980s', '1990%27s', 'Atmospheric', 'Comedy', 'Drama', 'Emotional', 'Funny', 'LGBTQ%2B', 'Old%20School', 'Romance', 'Female%20Protagonist', 'Multiple%20Endings', 'Singleplayer'], 'platform_score': None, 'platform_price': '089', 'platform_discount': '40', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3453290/header.jpg?t=1739359683', 'age_rating': None}, {'title': 'Puzzle Summit: Solve & Rise', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual', 'Indie', 'Strategy'], 'publisher': ['Joygame'], 'developer': ['Mafia%20Games'], 'tag': ['Indie', 'Typing', 'Singleplayer', 'Colorful', 'Relaxing', 'Strategy', 'Casual', 'Board%20Game', '2D', 'Puzzle', 'Match%203', 'Arcade', 'Choices%20Matter', 'Tactical', 'Tutorial'], 'platform_score': None, 'platform_price': '249', 'platform_discount': '15', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3079430/header.jpg?t=1739352995', 'age_rating': None}, {'title': 'Plague Doctor And Panacea', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Action', 'Adventure', 'Indie', 'Simulation'], 'publisher': [], 'developer': [], 'tag': ['Exploration', 'Dungeon%20Crawler', 'Hidden%20Object', 'Simulation', 'Action', 'Survival', 'Adventure', 'PvE', 'Walking%20Simulator', 'Action-Adventure', '3D', 'Third%20Person', 'Indie', 'Atmospheric', 'Retro', 'Singleplayer'], 'platform_score': None, 'platform_price': '089', 'platform_discount': '30', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3486590/header.jpg?t=1739352452', 'age_rating': None}, {'title': 'Gimme Space Battle', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Action', 'Indie', 'Early%20Access'], 'publisher': ['Lotus%20Game'], 'developer': ['Fran%C3%A7ois%20Provansal'], 'tag': ['Early%20Access', 'Top-Down%20Shooter', 'Local%20Multiplayer', 'Team-Based', 'PvP', 'Local%20Co-Op', '4%20Player%20Local', 'Co-op%20Campaign', 'Family%20Friendly', 'Split%20Screen', 'Space', 'Funny', 'Action', 'Arcade', 'Score%20Attack', 'Shoot%20%27Em%20Up', 'Colorful', 'Cute', 'Combat', 'Shooter'], 'platform_score': None, 'platform_price': '1279', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3447820/header.jpg?t=1739347878', 'age_rating': None}, {'title': 'Dungeon Battles', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure', 'Indie', 'RPG', 'Strategy'], 'publisher': [], 'developer': [], 'tag': ['NSFW', 'Female%20Protagonist', 'Roguelike', 'Sexual%20Content', 'Mature', 'Nudity', 'Adventure', 'Strategy', 'RPG', 'Turn-Based%20Combat', 'Turn-Based%20Strategy', 'Turn-Based%20Tactics', 'Roguelite', '3D', 'Cartoony', 'Dark%20Humor', 'Singleplayer', 'Indie'], 'platform_score': None, 'platform_price': '169', 'platform_discount': '20', 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3443440/header.jpg?t=1739347429', 'age_rating': None}, {'title': 'The Secret Story', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Action', 'Adventure', 'Indie', 'RPG', 'Simulation', 'Free%20to%20Play'], 'publisher': ['UDAGameLab'], 'developer': ['UDAGameLab', 'Gagang'], 'tag': ['Horror', 'Episodic', 'Multiple%20Endings', 'Story%20Rich', 'Psychedelic', 'Adventure', 'Action', 'Survival%20Horror', 'Nonlinear', 'Interactive%20Fiction', 'Action-Adventure', 'First-Person', '3D', 'RPG', 'Exploration', 'Simulation', 'Walking%20Simulator', 'Level%20Editor', 'Atmospheric', 'Conversation'], 'platform_score': None, 'platform_price': '749', 'platform_discount': '40', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3367740/header.jpg?t=1739335082', 'age_rating': None}, {'title': 'Gem Exploration', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual'], 'publisher': ['me'], 'developer': ['me'], 'tag': ['Casual', '2D', 'Pixel%20Graphics', 'Cute', 'Colorful'], 'platform_score': None, 'platform_price': '89', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3427470/header.jpg?t=1739328961', 'age_rating': None}, {'title': 'scratched!', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Indie'], 'publisher': ['Second%20Row%20Software'], 'developer': ['Second%20Row%20Software'], 'tag': ['Precision%20Platformer', '2D%20Platformer', 'Difficult', 'Physics', 'Pool', 'Platformer', '2D', 'Relaxing', 'Indie', 'Linear', 'Singleplayer', 'Adventure'], 'platform_score': None, 'platform_price': '499', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3477680/header.jpg?t=1739328645', 'age_rating': None}, {'title': 'Dark Genesis', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Action', 'Adventure'], 'publisher': ['Seoung%20Jin%20Kim'], 'developer': ['Seoung%20Jin%20Kim'], 'tag': ['Adventure', 'Action', 'FPS', '3D', 'Horror', 'Dark', 'Zombies', 'Gore', 'Violent', 'Singleplayer', 'Realistic'], 'platform_score': None, 'platform_price': '499', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3431380/header.jpg?t=1739328577', 'age_rating': None}, {'title': 'Pop DS', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy', 'Casual', 'Indie', 'Strategy'], 'publisher': ['XPS%20Technology'], 'developer': ['XPS%20Technology'], 'tag': ['Strategy', 'Casual', 'Match%203', 'Puzzle', '2D', 'Colorful', 'Cute', 'Dog', 'Family%20Friendly', 'Logic', 'Indie', 'Relaxing', 'Grid-Based%20Movement', 'Singleplayer'], 'platform_score': None, 'platform_price': '339', 'platform_discount': '40', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2714340/header.jpg?t=1739325305', 'age_rating': None}, {'title': 'Primal Hearts 2', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure'], 'publisher': [], 'developer': ['Marmalade'], 'tag': ['Visual%20Novel', 'Romance', 'Casual', 'Choose%20Your%20Own%20Adventure', 'Story%20Rich', 'Anime', 'Cute', 'Martial%20Arts', 'Interactive%20Fiction', 'Funny', 'Sports', 'Life%20Sim', 'Dating%20Sim', '2D', 'Relaxing', 'Conversation', 'Multiple%20Endings', 'Narration', 'Colorful', 'Hand-drawn'], 'platform_score': None, 'platform_price': '2099', 'platform_discount': '20', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1368010/header.jpg?t=1739321961', 'age_rating': None}, {'title': 'Primal Hearts', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure'], 'publisher': [], 'developer': ['Marmalade'], 'tag': ['Comedy', 'Romance', 'Visual%20Novel', 'Multiple%20Endings', 'Cute', 'Martial%20Arts', 'Nature', '2D', 'Anime', 'Casual', 'Funny', 'Relaxing', 'Conversation', 'Life%20Sim', 'Choose%20Your%20Own%20Adventure', 'Narration', 'Story%20Rich', 'Interactive%20Fiction', 'Hand-drawn', 'Dating%20Sim'], 'platform_score': None, 'platform_price': '2099', 'platform_discount': '20', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1359400/header.jpg?t=1739321923', 'age_rating': None}, {'title': 'DescTop', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Casual', 'Casual', 'Indie', 'Simulation'], 'publisher': ['K3D'], 'developer': ['K3D'], 'tag': ['Typing', 'Casual', 'Idler', 'Simulation', 'Sandbox', 'Character%20Customization', '3D', 'Cute', 'Relaxing', 'Indie', 'Minimalist', 'Old%20School', 'Singleplayer'], 'platform_score': None, 'platform_price': '89', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3458030/header.jpg?t=1739316028', 'age_rating': None}, {'title': 'Stop and Breathe', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Free%20to%20Play', 'Casual', 'Indie', 'Free%20to%20Play'], 'publisher': [], 'developer': [], 'tag': ['3D%20Platformer', 'Casual', 'Puzzle%20Platformer', 'Education', 'Singleplayer', 'Stylized', 'Platformer', 'Side%20Scroller', 'Colorful', 'Third%20Person', 'Indie', 'Free%20to%20Play', 'Controller', 'Linear', 'Physics', '3D'], 'platform_score': None, 'platform_price': None, 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3219880/header.jpg?t=1739321599', 'age_rating': None}, {'title': 'Fly Rocket Die', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Casual', 'Indie'], 'publisher': ['CD_Games'], 'developer': ['Bunny'], 'tag': ['Casual', 'Adventure', 'Action', 'Platformer', 'Rhythm', '2D%20Platformer', '3D%20Platformer', 'Precision%20Platformer', '2D', '3D', 'Stylized', '1990%27s', 'Old%20School', 'Relaxing', 'Retro', 'Physics', 'Singleplayer', 'Indie'], 'platform_score': None, 'platform_price': '089', 'platform_discount': '40', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3447600/header.jpg?t=1739301111', 'age_rating': None}, {'title': 'Hand Simulator: Shooter', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Simulation', 'Action', 'Indie', 'Massively%20Multiplayer', 'Simulation', 'Early%20Access'], 'publisher': ['HFM%20Games'], 'developer': ['HFM%20Games'], 'tag': ['Simulation', 'Action', 'Shooter', 'Wargame', 'FPS', '3D', 'First-Person', 'Realistic', 'Military', 'War', 'PvP', 'Massively%20Multiplayer', 'Indie', 'Early%20Access', 'Team-Based', 'Physics', 'Multiplayer', 'Local%20Multiplayer'], 'platform_score': '33', 'platform_price': '169', 'platform_discount': '40', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3066260/header.jpg?t=1739298495', 'age_rating': None}, {'title': 'The Executive - Movie Industry Tycoon', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy', 'Simulation', 'Strategy'], 'publisher': ['Maple%20Whispering%20Limited'], 'developer': ['Aniki%20Games'], 'tag': ['Management', 'Simulation', 'Movie', 'Economy', 'Strategy', 'Capitalism', '2D', 'Sandbox', 'Isometric', 'Singleplayer', 'Replay%20Value', 'Indie', 'Building', 'Moddable', 'Cinematic', 'Casual', 'Funny', 'Comedy', 'Trading', 'Point%20%26%20Click'], 'platform_score': '66', 'platform_price': '1279', 'platform_discount': '10', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2315430/header.jpg?t=1739356766', 'age_rating': None}, {'title': 'SteamDolls - Order Of Chaos', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Indie', 'Early%20Access'], 'publisher': ['The%20Shady%20Gentlemen'], 'developer': ['The%20Shady%20Gentlemen'], 'tag': ['Early%20Access', 'Metroidvania', 'Dark%20Fantasy', 'Action', 'Indie', 'Violent', 'Gore', 'Adventure', 'Steampunk', 'Platformer', 'Open%20World', 'Nudity', '2D%20Platformer', 'Side%20Scroller', 'Hand-drawn', 'Lore-Rich', 'Story%20Rich', 'Blood', 'Controller', 'Great%20Soundtrack'], 'platform_score': None, 'platform_price': '1675', 'platform_discount': '15', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1305260/header.jpg?t=1739296843', 'age_rating': None}, {'title': 'Cards!', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Free%20to%20Play', 'Indie', 'Simulation', 'Free%20to%20Play'], 'publisher': ['Good%20And%20Bad%20Games%20Corp'], 'developer': ['Good%20And%20Bad%20Games%20Corp'], 'tag': ['Trading%20Card%20Game', 'Creature%20Collector', 'Clicker', 'Idler', 'Card%20Game', 'Simulation', 'Pixel%20Graphics', 'Deckbuilding', 'Sandbox', 'Inventory%20Management', 'Hidden%20Object', 'Management', 'Resource%20Management', 'Economy', 'Crafting', 'Loot', 'Relaxing', '2D', 'Colorful', 'Minimalist'], 'platform_score': '80', 'platform_price': 'Free To Play!', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3383700/header.jpg?t=1739294205', 'age_rating': None}, {'title': 'Mournight', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Action', 'Adventure', 'Casual', 'Indie', 'Early%20Access'], 'publisher': ['Fround%20Interactive'], 'developer': ['Fround%20Interactive'], 'tag': ['Early%20Access', 'Horror', 'Action', 'Thriller', 'Survival%20Horror', 'Surreal', 'Adventure', 'Dark', 'FPS', 'Action-Adventure', 'First-Person', 'Split%20Screen', 'Realistic', 'Supernatural', 'Atmospheric', 'Dark%20Fantasy', 'Fantasy', 'Mystery', 'Survival', '3D'], 'platform_score': None, 'platform_price': '589', 'platform_discount': '15', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3436970/header.jpg?t=1739293217', 'age_rating': None}, {'title': 'SpyFall', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Casual', 'Indie', 'Early%20Access'], 'publisher': ['MB%20Studio'], 'developer': ['Mamkalo', 'Bario'], 'tag': ['Action', 'Casual', 'PvP', 'Multiplayer', 'Online%20Co-Op', 'Indie', 'Early%20Access'], 'platform_score': None, 'platform_price': '429', 'platform_discount': '20', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3334280/header.jpg?t=1739289623', 'age_rating': None}, {'title': 'Poker Clicker', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Free%20to%20Play', 'Casual', 'Indie', 'Strategy', 'Free%20to%20Play'], 'publisher': ['Software24601'], 'developer': ['Software24601'], 'tag': ['Casual', 'Free%20to%20Play', 'Clicker', 'Idler', 'Collectathon', '2D', 'Loot', 'Singleplayer', 'Relaxing', 'Score%20Attack', 'Tabletop', 'Card%20Game', 'Board%20Game', 'Strategy', 'Arcade', 'Colorful', 'Family%20Friendly', 'Tactical', 'Open%20World', 'Simulation'], 'platform_score': '37', 'platform_price': 'Free To Play!', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3433030/header.jpg?t=1739289503', 'age_rating': None}, {'title': 'AmaZoo', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure', 'Indie'], 'publisher': ['Turbo%20Soda%20Games'], 'developer': ['Turbo%20Soda%20Games'], 'tag': ['Singleplayer', 'Puzzle', '2D', 'Sokoban', 'Grid-Based%20Movement', 'Casual', 'Cute', 'Comic%20Book', 'Adventure', 'Indie', 'Cartoony', 'Colorful'], 'platform_score': None, 'platform_price': '1057', 'platform_discount': '20', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3066360/header.jpg?t=1739287005', 'age_rating': None}, {'title': 'Infection Roots Deluxe', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Adventure'], 'publisher': [], 'developer': [], 'tag': ['Action', 'Adventure', 'Action-Adventure', 'Shooter', 'Top-Down%20Shooter', '2D', 'Dark', 'Horror', 'Atmospheric', 'Survival', 'Survival%20Horror', 'Zombies', 'Linear', 'PvE', 'Singleplayer'], 'platform_score': None, 'platform_price': '169', 'platform_discount': None, 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3284750/header.jpg?t=1739286096', 'age_rating': None}, {'title': 'THE BRiLLiANT COUP', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Indie', 'Adventure', 'Casual', 'Indie'], 'publisher': ['Markus%20Creative'], 'developer': ['Markus%20Creative'], 'tag': ['Point%20%26%20Click', 'Pixel%20Graphics', 'Puzzle', '2D', 'Funny', 'Comedy', 'Adventure', '1980s', 'Old%20School', 'Casual', 'Multiple%20Endings', 'Heist', 'Singleplayer', 'Exploration', 'Cartoony', 'Hand-drawn', '1990%27s', 'Narration', 'Indie'], 'platform_score': None, 'platform_price': '1499', 'platform_discount': '10', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2709360/header.jpg?t=1739284677', 'age_rating': None}, {'title': 'Oirbo', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Action', 'Action', 'Adventure', 'Casual', 'Indie'], 'publisher': [], 'developer': [], 'tag': ['Metroidvania', 'Adventure', 'Difficult', 'Action', 'Open%20World', 'Exploration', 'Action-Adventure', '2D%20Platformer', 'Puzzle%20Platformer', 'Sci-fi', 'Precision%20Platformer', 'Puzzle', 'Platformer', '2D', 'Controller', 'Old%20School', 'Multiple%20Endings', 'Singleplayer', 'Futuristic', 'Side%20Scroller'], 'platform_score': '94', 'platform_price': '1499', 'platform_discount': '15', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/1074280/header.jpg?t=1739282673', 'age_rating': None}, {'title': 'ZAMOK', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Adventure', 'Adventure', 'Indie'], 'publisher': [], 'developer': ['HouseInMotion'], 'tag': ['Exploration', 'Walking%20Simulator', '3D', 'First-Person', 'Noir', 'Surreal', 'Story%20Rich', 'Simulation', 'Abstract', 'Stylized', 'Dystopian%20', 'Philosophical', 'Atmospheric', 'Drama', 'Emotional', 'Mystery', 'Psychological', '1990%27s', 'Conspiracy', 'Singleplayer'], 'platform_score': None, 'platform_price': '429', 'platform_discount': '10', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3346610/header.jpg?t=1739282525', 'age_rating': None}, {'title': 'Transylvania Drift', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Racing', 'Casual', 'Racing', 'Simulation'], 'publisher': ['Andrasfi%20Games'], 'developer': ['Andrasfi%20Games'], 'tag': ['Racing', 'Simulation', 'Arcade', '3D', 'Open%20World', 'Driving', 'Singleplayer', 'Exploration', 'First-Person', 'Third%20Person', 'Atmospheric', 'Automobile%20Sim', 'Funny', 'Relaxing', 'Realistic', 'Old%20School', 'Retro', '1990%27s', 'Controller', 'Physics'], 'platform_score': None, 'platform_price': '169', 'platform_discount': '10', 'release_date': '11 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/3421010/header.jpg?t=1739318429', 'age_rating': None}]


    logging.info(clean_data(Data))
    logging.info(len(Data))
    logging.info(len(clean_data(Data)))
