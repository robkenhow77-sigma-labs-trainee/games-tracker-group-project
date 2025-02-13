"""Script containing all functions pertaining to cleaning the data before insertion."""

import logging
from datetime import datetime, timedelta

from requests import get

DAYS_BEFORE_TODAY_THAT_WILL_BE_ACCEPTED = 100

#TODO: ensure logger is imported and config-ed
#TODO: clean image data!

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
        print("game is not a valid entry, missing keys: %s", missing_keys)
        return False

    return (is_valid_title(game['title']) and is_valid_genres(game['genres']) and
            is_valid_price(game['platform_price']) and is_valid_release(game['release_date']))


def is_valid_title(title: str) -> bool:
    """Returns true if title is valid."""

    if not isinstance(title, str):
        print("%s is not a valid title, not a string", title)
        return False

    title = title.strip().replace('%20', ' ')

    if len(title) > 101:
        print("%s is not a valid title, too long", title)
        return False

    if len(title) == 0:
        print("%s is not a valid title, empty title", title)
        return False

    return True


def is_valid_genres(genres: list[str]) -> bool:
    """Returns true if genres are valid."""

    if not isinstance(genres, list):
        print("%s is not a valid genre, not a list", genres)
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
        print("%s is not a valid genre, not a string", genre)
        return False

    genre = genre.strip()

    if len(genre) > 51:
        print("%s is not a valid genre, too long.", genre)
        return False

    if len(genre) == 0:
        print("%s is not a valid genre, cannot be empty.", genre)
        return False

    return True


def is_valid_publisher(publishers: list[str]) -> bool:
    """Returns true if publishers are valid."""

    if not isinstance(publishers, list):
        print("%s is not a valid publisher, not a list", publishers)
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
        print("%s is not a valid publisher, not a string", publisher)
        return False

    publisher = publisher.strip().replace('%20', ' ')

    if len(publisher) == 0:
        print("%s is not a valid publisher, cannot be empty", publisher)
        return False

    if len(publisher) > 151:
        print("%s is not a valid publisher, too long.", publisher)
        return False
    
    return True


def is_valid_developer(developers: list[str]) -> bool:
    """Returns true if developers are valid."""

    if not isinstance(developers, list):
        print("%s is not a valid developers, not a list", developers)
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
        print("%s is not a valid developer, not a string", developer)
        return False

    developer = developer.strip().replace('%20', ' ')

    if len(developer) == 0:
        print("%s is not a valid developer, cannot be empty", developer)
        return False

    if len(developer) > 151:
        print("%s is not a valid developer, too long.", developer)
        return False

    return True


def is_valid_tag(tags: list[str]) -> bool:
    """Returns true if tags are valid."""

    if not isinstance(tags, list):
        print("%s is not a valid tag, not a list", tags)
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
        print("%s is not a valid tag, not a string", tag)
        return False

    tag = tag.strip().replace('%20', ' ')

    if len(tag) == 0:
        print("%s is not a valid tag, cannot be empty", tag)
        return False

    if len(tag) > 51:
        print("%s is not a valid tag, too long.", tag)
        return False

    return True


def is_valid_score(score: str) -> bool:
    """Returns true if score is valid."""

    if not isinstance(score, str):
        print("%s is not a valid score, not a string", score)
        return False

    score = score.strip()
    if '.' in score:
        unit, decimal = score.split('.')

        if not unit.isnumeric():
            print("%s is not a valid score, not an integer.", score)
            return False

        if not decimal.isnumeric():
            print("%s is not a valid score, not an integer.", score)
            return False

        score = int(unit) * 20 + int(decimal) * 2

        if not 0 <= int(score) <= 100:
            print("%s is not a valid score, not between 0 and 100.", score)
            return False

    else:
        if not score.isnumeric():
            print("%s is not a valid score, not an integer.", score)
            return False
        
        score = int(score) * 20
        
        if not 0 <= int(score) <= 100:
            print("%s is not a valid score, not between 0 and 100.", score)
            return False

    return True


def is_valid_price(price: float) -> bool:
    """Returns true if price is valid."""

    if not isinstance(price, str):
        print("%s is not a valid price, not a string", price)
        return False

    price = price.strip().replace('.','')

    if not price.isnumeric():
        print("%s is not a valid price, not numeric.", price)
        return False

    return int(price) >= 0


def is_valid_discount(discount: int) -> bool:
    """Returns true if discount is valid."""

    #Not on discount currently
    if discount is None:
        return True

    if not isinstance(discount, str):
        print("%s is not a valid discount, not a string", discount)
        return False

    discount = discount.strip().replace('.','')

    if not discount.isnumeric():
        print("%s is not a valid price, not numeric.", discount)
        return False

    if not 0 <= int(discount) <= 100:
        print("%s is not a valid discount, not between 0 and 100.", discount)
        return False

    return True


def is_valid_release(release: str,
                     days_before_today_allowed=DAYS_BEFORE_TODAY_THAT_WILL_BE_ACCEPTED) -> bool:
    """Returns true if release is valid."""

    if not isinstance(release, str):
        print("%s is not a string, not a valid release date.", release)
        return False
    
    try:
        release = release[:10]
    except:
        print("%s is not a string, not a long enough to be  date.", release)


    try:
        datetime_release = datetime.strptime(release, "%Y-%m-%d")
    except Exception as e:
        print("""%s is not in the valid release form.
                                %s""", release, e)
        return False

    earliest_allowed_date = datetime.now().date() - timedelta(days=days_before_today_allowed)

    if not earliest_allowed_date <= datetime_release.date() <= datetime.now().date():
        print("%s is not within the allowed release date range.", release)
        return False

    return True


def is_valid_image(image: str) -> bool:
    """Returns true if image is valid."""

    if not isinstance(image, str):
        print("%s is not a valid image, not a string", image)
        return False

    image = image.replace(" ",'')
    image = image.replace("\n",'')
    image = image.split(',')[0]
    image = image.strip()

    if len(image) > 256:
        print("%s is not a valid image, url too long", image)
        return False

    if len(image) == 0:
        print("%s is not a valid image, empty string", image)
        return False

    try:
        response = get(image, timeout=5)
    except Exception as e:
        print("""%s is not a valid image, not loading properly.
                        Error: %s""", image, e)
        return False

    if not response.status_code == 200:
        print("%s is not a valid image, not loading properly.", image)
        return False

    return True


def is_valid_age(age: str) -> bool:
    """Returns if the age conforms to PEGI standards."""

    if age is None:
        return False

    if not isinstance(age, str):
        print("%s is not a valid age rating, not a string", age)
        return False

    age = age.strip()

    if age not in ['3', '7', '12', '16', '18']:
        print("%s is not a valid age rating, not a standard PEGI age", age)
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
        formatted_data['platform_score'] = format_score(game['platform_score'])
    else:
        formatted_data['platform_score'] = -1
    if is_valid_discount(game['platform_discount']):
        formatted_data['platform_discount'] = format_integer(game['platform_discount'])
    else:
        formatted_data['platform_discount'] = 0
    if is_valid_release(game['release_date']):
        formatted_data['release_date'] = format_release(game['release_date'])
    else:
        formatted_data['release_date'] = None
    if is_valid_image(game['game_image']):
        formatted_data['game_image'] = format_string(game['game_image'])
    else:
        formatted_data['game_image'] = 'N/A'
    if is_valid_age(game['age_rating']):
        formatted_data['age_rating'] = format_string(game['age_rating'])
    else:
        formatted_data['age_rating'] = 'Not Assigned'

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

#TODO: write tests for this
def format_score(score: str) -> int:
    """Formats the score as a percentage."""

    score = score.strip()

    if '.' in score:
        unit, decimal = score.split('.')
        score = int(unit) * 20 + int(decimal) * 2

    else:
        score = int(score) * 20
    
    return int(score)


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

    Data = [{'title': 'Recall: Empty Wishes', 'genres': ['Adventure', 'Visual Novel', 'Horror'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'DANGEN Entertainment'], 'developer': ['Puff Hook Studio'], 'tag': ['Adventure, ', 'Indie, ', 'Story Rich, ', 'Role-playing, ', '2D, ', 'First-Person, ', 'Pixel Graphics, ', 'Horror, ', 'Platformer, ', 'Visual Novel, ', 'Multiple Endings, ', 'Psychological Horror, ', 'Detective-mystery', 'Adventure, ', 'Indie, ', 'Story Rich, ', 'Role-playing, ', '2D, '], 'platform_score': '5', 'platform_price': '12.79', 'platform_discount': '9', 'release_date': '2025-02-13T13:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/60d30a967f6baf4b52800cb76070c5eb102edc545828c26a67f563ac604ef752_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/60d30a967f6baf4b52800cb76070c5eb102edc545828c26a67f563ac604ef752_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Primal Hearts', 'genres': ['Adventure', 'Visual Novel', 'JRPG'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Shiravune'], 'developer': ['Marmalade'], 'tag': ['Adventure, ', 'Story Rich, ', '2D, ', 'Casual, ', 'Choices Matter, ', 'Funny, ', 'Visual Novel, ', 'Sexual Content, ', 'JRPG, ', 'Nudity, ', 'Multiple Endings, ', 'Mature, ', 'NSFW, ', 'Relaxing, ', 'Narrative, ', 'Choose Your Own Adventure, ', 'Romance, ', 'Dating Sim, ', 'Comedy, ', 'Text-Based, ', 'Nature, ', 'LifeSim, ', 'Martial Arts', 'Adventure, ', 'Story Rich, ', '2D, ', 'Casual, ', 'Choices Matter, '], 'platform_score': '3', 'platform_price': '20.99', 'platform_discount': '20', 'release_date': '2025-02-12T10:58:00+02:00', 'game_image': '\n                https://images.gog-statics.com/dfaf4160a85c10b80bd663119cc2295c6dbd0ccc69e2c08ac3a12f5c119ca24f_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/dfaf4160a85c10b80bd663119cc2295c6dbd0ccc69e2c08ac3a12f5c119ca24f_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Primal Hearts 2', 'genres': ['Adventure', 'Visual Novel', 'JRPG'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Shiravune'], 'developer': ['Marmalade'], 'tag': ['Adventure, ', 'Story Rich, ', '2D, ', 'Casual, ', 'Choices Matter, ', 'Funny, ', 'Visual Novel, ', 'Sexual Content, ', 'JRPG, ', 'Nudity, ', 'Multiple Endings, ', 'Mature, ', 'NSFW, ', 'Relaxing, ', 'Narrative, ', 'Choose Your Own Adventure, ', 'Romance, ', 'Dating Sim, ', 'Comedy, ', 'Text-Based, ', 'Nature, ', 'LifeSim, ', 'Martial Arts', 'Adventure, ', 'Story Rich, ', '2D, ', 'Casual, ', 'Choices Matter, '], 'platform_score': '5', 'platform_price': '20.99', 'platform_discount': '20', 'release_date': '2025-02-12T10:58:00+02:00', 'game_image': '\n                https://images.gog-statics.com/952fe84cb74e323eb3a4b2f388da777a2b5545201af0dd990a32c6424fd422fd_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/952fe84cb74e323eb3a4b2f388da777a2b5545201af0dd990a32c6424fd422fd_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'The Executive - Movie Industry Tycoon', 'genres': ['Simulation', 'Strategy', 'Sandbox'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Goblinz Studio, Maple Whispering Limited'], 'developer': ['Aniki Games'], 'tag': ['Indie, ', 'Strategy, ', 'Simulation, ', 'Management, ', 'Sandbox, ', 'Family Friendly, ', 'Relaxing, ', 'Text-Based, ', 'Movie', 'Indie, ', 'Strategy, ', 'Simulation, ', 'Management, ', 'Sandbox, '], 'platform_score': '', 'platform_price': '12.79', 'platform_discount': '9', 'release_date': '2025-02-11T19:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/eb54825a9f77baab130eabe90c55e8b01e9ceb56cabf209c6e1351e432db9d71_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/eb54825a9f77baab130eabe90c55e8b01e9ceb56cabf209c6e1351e432db9d71_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Reality Break', 'genres': ['Action', 'Role-playing', 'Sci-fi'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Element Games, LLC'], 'developer': ['Element Games, LLC'], 'tag': ['Action, ', 'Role-playing, ', 'Sci-fi, ', 'Choices Matter, ', 'Space, ', 'Roguelike, ', 'Crafting, ', 'Roguelite, ', 'Looter Shooter', 'Action, ', 'Role-playing, ', 'Sci-fi, ', 'Choices Matter, ', 'Space, '], 'platform_score': '', 'platform_price': '20.99', 'platform_discount': '10', 'release_date': '2025-02-10T13:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/29aa39848abfddf37f6cdd451b40440368d39e02041620ade759cc3a172b3955_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/29aa39848abfddf37f6cdd451b40440368d39e02041620ade759cc3a172b3955_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Slender Threads', 'genres': ['Adventure', 'Point-and-click', 'Horror'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Blyts'], 'developer': ['Blyts'], 'tag': ['Adventure, ', 'Indie, ', 'Dark, ', 'Horror, ', 'Point&Click', 'Adventure, ', 'Indie, ', 'Dark, ', 'Horror, ', 'Point&Click'], 'platform_score': '', 'platform_price': '16.75', 'platform_discount': '10', 'release_date': '2025-02-07T13:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/f2354fa4520dc75b176d6e38e879960179f7470e4aeff18032d5b6ce7c0e26e5_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/f2354fa4520dc75b176d6e38e879960179f7470e4aeff18032d5b6ce7c0e26e5_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Starlight Legacy', 'genres': ['Adventure', 'Turn-based', 'JRPG'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Eastasiasoft Limited, Decafesoft'], 'developer': ['Decafesoft'], 'tag': ['Adventure, ', 'Indie, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', '2D, ', 'Turn-Based, ', 'Exploration, ', 'Pixel Graphics, ', 'JRPG, ', 'Magic, ', 'Retro', 'Adventure, ', 'Indie, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, '], 'platform_score': '', 'platform_price': '14.29', 'platform_discount': '10', 'release_date': '2025-02-05T16:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/bbc92c99a140d3c6a009655961fda2efebacdc444f4ca6eba7be27b60c452bfa_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/bbc92c99a140d3c6a009655961fda2efebacdc444f4ca6eba7be27b60c452bfa_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Citizen Sleeper 2: Starward Vector', 'genres': ['Role-playing', 'Adventure', 'Sci-fi'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Fellow Traveller'], 'developer': ['Jump Over The Age'], 'tag': ['Adventure, ', 'Indie, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Sci-fi, ', 'Exploration, ', 'Point&Click, ', 'Multiple Endings, ', 'Space, ', 'Cyberpunk, ', 'Dystopian, ', 'Text-Based, ', 'Tabletop', 'Adventure, ', 'Indie, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, '], 'platform_score': '', 'platform_price': '20.99', 'platform_discount': '10', 'release_date': '2025-01-31T17:58:00+02:00', 'game_image': '\n                https://images.gog-statics.com/ad625cbee57cb633ade30e88b9dbeca73bf0fb9c24b8f5ed10a84a107025d076_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/ad625cbee57cb633ade30e88b9dbeca73bf0fb9c24b8f5ed10a84a107025d076_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Citizen Sleeper 2: Starward Vector Deluxe Edition', 'genres': ['Role-playing', 'Adventure', 'Sci-fi'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Fellow Traveller'], 'developer': ['Jump Over The Age'], 'tag': ['Adventure, ', 'Indie, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Sci-fi, ', 'Exploration, ', 'Point&Click, ', 'OST, ', 'Multiple Endings, ', 'Space, ', 'Artbook, ', 'Cyberpunk, ', 'Dystopian, ', 'Text-Based, ', 'Tabletop', 'Adventure, ', 'Indie, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, '], 'platform_score': '', 'platform_price': '31.79', 'platform_discount': '7', 'release_date': '2025-01-31T17:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/26bc5bf6632ca1b188952ab87eef35f04fa7240a56ff4c5873a59bb9c4360a8f_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/26bc5bf6632ca1b188952ab87eef35f04fa7240a56ff4c5873a59bb9c4360a8f_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Foundation Supporter Edition', 'genres': ['Strategy', 'Building', 'Managerial'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Polymorph Games'], 'developer': ['Polymorph Games'], 'tag': ['Indie, ', 'Strategy, ', 'Atmospheric, ', 'Choices Matter, ', 'Management, ', 'Open World, ', 'Sandbox, ', 'Resource Management, ', 'Survival, ', 'Relaxing, ', 'Managerial, ', 'Medieval, ', 'Building, ', 'Base Building, ', 'RTS, ', 'City builder', 'Indie, ', 'Strategy, ', 'Atmospheric, ', 'Choices Matter, ', 'Management, '], 'platform_score': '3', 'platform_price': '36.19', 'platform_discount': '25', 'release_date': '2025-01-31T16:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/f4dfd20abc6f9348164426052b13f149a276498b35c24caadfdc1e3a9c3c5be9_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/f4dfd20abc6f9348164426052b13f149a276498b35c24caadfdc1e3a9c3c5be9_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Heart of the Machine', 'genres': ['Role-playing', 'Strategy', 'Managerial'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Hooded Horse'], 'developer': ['Arcen Games'], 'tag': ['Strategy, ', 'Role-playing, ', 'Managerial', 'Strategy, ', 'Role-playing, ', 'Managerial'], 'platform_score': '4.9', 'platform_price': '24.99', 'platform_discount': '20', 'release_date': '2025-01-31T15:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/a02afe553323807983f9b25fcf9af68f1e7cc7b6bd25bb4318b24e22bdbcc939_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/a02afe553323807983f9b25fcf9af68f1e7cc7b6bd25bb4318b24e22bdbcc939_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Techno Banter', 'genres': ['Role-playing', 'Simulation', 'Comedy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Crunching Koalas'], 'developer': ['Dexai Arts'], 'tag': ['Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Exploration, ', 'Simulation, ', 'First-Person, ', 'Casual, ', 'Pixel Graphics, ', 'Choices Matter, ', 'Funny, ', 'Multiple Endings, ', 'Retro, ', 'Choose Your Own Adventure, ', 'Cyberpunk, ', 'CRPG, ', 'Dark Comedy, ', 'Comedy, ', 'Walking Simulator, ', 'Dystopian, ', 'Underground', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Exploration, ', 'Simulation, '], 'platform_score': '', 'platform_price': '14.99', 'platform_discount': '20', 'release_date': '2025-01-30T18:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/7421ae3a4ecbbcbdf930941ee3f2cd303d06c6b5ba76373c4ef6f155542247d3_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/7421ae3a4ecbbcbdf930941ee3f2cd303d06c6b5ba76373c4ef6f155542247d3_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Techno Banter: Ultimate Mix', 'genres': ['Role-playing', 'Simulation', 'Comedy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Crunching Koalas'], 'developer': ['Dexai Arts'], 'tag': ['Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Exploration, ', 'Simulation, ', 'First-Person, ', 'Pixel Graphics, ', 'Choices Matter, ', 'Multiple Endings, ', 'Retro, ', 'Choose Your Own Adventure, ', 'Cyberpunk, ', 'Dark Comedy, ', 'Comedy, ', 'Underground', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Exploration, ', 'Simulation, '], 'platform_score': '0', 'platform_price': '16.99', 'platform_discount': '10', 'release_date': '2025-01-30T18:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/7421ae3a4ecbbcbdf930941ee3f2cd303d06c6b5ba76373c4ef6f155542247d3_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/7421ae3a4ecbbcbdf930941ee3f2cd303d06c6b5ba76373c4ef6f155542247d3_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Coridden', 'genres': ['Role-playing', 'Action', 'Fantasy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Anshar Publishing'], 'developer': ['Aftnareld'], 'tag': ['Action, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', 'Exploration, ', 'Isometric, ', 'Top-Down, ', 'Hack and Slash, ', 'Local Co-Op, ', 'Post-apocalyptic, ', 'Local Multiplayer, ', 'Dinosaurs', 'Action, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', 'Exploration, '], 'platform_score': '5', 'platform_price': '16.75', 'platform_discount': '0', 'release_date': '2025-01-29T18:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/984e3c9df81cebbc4d546006ad677f2fe5fc850c465c7277b951ca29b2f81915_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/984e3c9df81cebbc4d546006ad677f2fe5fc850c465c7277b951ca29b2f81915_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Coridden - Deluxe Edition', 'genres': ['Role-playing', 'Action', 'Fantasy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Anshar Publishing'], 'developer': ['Aftnareld'], 'tag': ['Action, ', 'Indie, ', 'Fantasy, ', 'Role-playing, ', 'Sci-fi, ', 'Local Co-Op, ', 'Dungeon Crawler, ', 'Combat, ', 'Nature, ', 'Split Screen, ', 'Dinosaurs', 'Action, ', 'Indie, ', 'Fantasy, ', 'Role-playing, ', 'Sci-fi, '], 'platform_score': '0', 'platform_price': '21.59', 'platform_discount': '0', 'release_date': '2025-01-29T18:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/121a898aa4dae55dafcbc8d89cbb5b8d7a6d2473045d1885c1368ace51e86442_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/121a898aa4dae55dafcbc8d89cbb5b8d7a6d2473045d1885c1368ace51e86442_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'The End of the Sun', 'genres': ['Adventure', 'Point-and-click', 'Puzzle'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'The End of the Sun Team'], 'developer': ['The End of the Sun Team'], 'tag': ['Adventure, ', 'Indie, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, ', 'Puzzle, ', 'Point&Click, ', 'Open World, ', 'Mystery, ', 'Walking Simulator, ', 'Supernatural, ', 'Mythology, ', 'Time Manipulation', 'Adventure, ', 'Indie, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, '], 'platform_score': '', 'platform_price': '21.59', 'platform_discount': '0', 'release_date': '2025-01-29T18:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/c03ed9914b703db5205542a847d70cf514238bfd55b8177aba8d1ae5dd124c1e_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/c03ed9914b703db5205542a847d70cf514238bfd55b8177aba8d1ae5dd124c1e_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'The End of the Sun - Soundtrack Edition', 'genres': ['Adventure', 'Point-and-click', 'Puzzle'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'The End of the Sun Team'], 'developer': ['The End of the Sun Team'], 'tag': ['Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, ', 'Puzzle, ', 'First-Person, ', 'Casual, ', 'Point&Click, ', 'Open World, ', 'Mystery, ', 'Emotional, ', 'Walking Simulator, ', 'Thriller, ', 'Short, ', 'Mythology, ', 'Time Manipulation', 'Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, '], 'platform_score': '', 'platform_price': '23.43', 'platform_discount': '0', 'release_date': '2025-01-29T18:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/1524642c20ac33f2f0fa9a592d88f7dd621f3cc2c59d9dd89ad30ca87b469273_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/1524642c20ac33f2f0fa9a592d88f7dd621f3cc2c59d9dd89ad30ca87b469273_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Learning Factory Catopia Visionary Edition', 'genres': ['Simulation', 'Strategy', 'Programming'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Luden.io'], 'developer': ['Learning Factory Support the Developers & Poster Pack', 'Luden.io', 'Learning Factory Support the Developers & Poster Pack\n                                                In library\n                    \n                                                In cart\n                    \n                                                Soon\n                    \n                                                GOOD OLD GAME\n                    \n                                                Wishlisted\n                    \n                                                        In library\n                        \n                                                        In cart\n                        \n                                                        Soon\n                        \n                                                        GOOD OLD GAME\n                        \n                                                        Wishlisted\n                        4.29Free\n                        \n                Play for free\n            \n                Coming soon'], 'tag': ['Strategy, ', 'Simulation, ', 'Science, ', 'Management, ', 'Sandbox, ', 'Resource Management, ', 'Family Friendly, ', 'Relaxing, ', 'Building, ', 'Crafting, ', 'Base Building, ', 'Procedural Generation, ', 'Education, ', 'Cats, ', 'Fishing, ', 'Programming', 'Strategy, ', 'Simulation, ', 'Science, ', 'Management, ', 'Sandbox, '], 'platform_score': '', 'platform_price': '17.53', 'platform_discount': '0', 'release_date': '2025-01-31T11:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/2f324b6cf7405d40b6a5e9b2d435abd5d4c7cb2577e574f2f4619d5f09235a39_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/2f324b6cf7405d40b6a5e9b2d435abd5d4c7cb2577e574f2f4619d5f09235a39_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'The Stone of Madness', 'genres': ['Adventure', 'Strategy', 'Tactical'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Tripwire Interactive'], 'developer': ['The Game Kitchen'], 'tag': ['Adventure, ', 'Indie, ', 'Strategy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, ', 'Puzzle, ', 'Dark, ', 'Choices Matter, ', 'Tactical, ', 'Point&Click, ', 'Mystery, ', 'Historical, ', 'Survival, ', 'Violent, ', 'Difficult, ', 'Multiple Endings, ', 'Isometric, ', 'Medieval, ', 'Investigation, ', 'Stealth, ', 'Psychological', 'Adventure, ', 'Indie, ', 'Strategy, ', 'Story Rich, ', 'Atmospheric, '], 'platform_score': '', 'platform_price': '24.99', 'platform_discount': '0', 'release_date': '2025-01-28T17:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/3867e8bec4380768f6550a084aa9f2d82b749817198660ab9824b089905f047b_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/3867e8bec4380768f6550a084aa9f2d82b749817198660ab9824b089905f047b_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'The Stone of Madness - Special Edition', 'genres': ['Adventure', 'Strategy', 'Tactical'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Tripwire Interactive'], 'developer': ['The Game Kitchen'], 'tag': ['Adventure, ', 'Indie, ', 'Strategy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, ', 'Puzzle, ', 'Dark, ', 'Choices Matter, ', 'Tactical, ', 'Point&Click, ', 'Mystery, ', 'Historical, ', 'Survival, ', 'Violent, ', 'Difficult, ', 'Multiple Endings, ', 'Isometric, ', 'Medieval, ', 'Investigation, ', 'Stealth, ', 'Psychological', 'Adventure, ', 'Indie, ', 'Strategy, ', 'Story Rich, ', 'Atmospheric, '], 'platform_score': '0', 'platform_price': '29.50', 'platform_discount': '0', 'release_date': '2025-01-28T17:59:00+02:00', 'game_image': '\n                https://images.gog-statics.com/3bdae2a60a574be626a375a1eb9250c4df87bc96c602b02feae91ebf397371d0_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/3bdae2a60a574be626a375a1eb9250c4df87bc96c602b02feae91ebf397371d0_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Darkest Dungeon® II: Resolute Edition', 'genres': ['Strategy', 'Turn-based', 'Fantasy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Red Hook Studios'], 'developer': ['Red Hook Studios'], 'tag': ['Fantasy, ', 'Strategy, ', 'Story Rich, ', '2D, ', 'Turn-Based, ', 'Roguelike, ', 'Roguelite, ', 'Procedural Generation, ', 'Dungeon Crawler, ', 'CRPG, ', 'Lovecraftian, ', 'Perma Death', 'Fantasy, ', 'Strategy, ', 'Story Rich, ', '2D, ', 'Turn-Based, '], 'platform_score': '3.5', 'platform_price': '39.59', 'platform_discount': '0', 'release_date': '2025-01-27T19:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/1de0880c2f67795958d9429a235a2e6fd82064eedb2917891791a0bbc745e3d7_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/1de0880c2f67795958d9429a235a2e6fd82064eedb2917891791a0bbc745e3d7_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': '12'}, {'title': 'Mark of the Deep', 'genres': ['Action', 'Adventure', 'Metroidvania'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Light Up Games'], 'developer': ['Mad Mimic'], 'tag': ['Adventure, ', 'Action, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, ', 'Multiple Endings, ', 'Isometric, ', 'Metroidvania, ', 'Souls-like, ', 'Pirates', 'Adventure, ', 'Action, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, '], 'platform_score': '3.5', 'platform_price': '24.99', 'platform_discount': '0', 'release_date': '2025-01-24T18:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/6a428724419287a475df7c405fff6cd9c2fa739fbdd569de994f9ba6b0d73b8e_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/6a428724419287a475df7c405fff6cd9c2fa739fbdd569de994f9ba6b0d73b8e_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Mark of the Deep - Deluxe Edition', 'genres': ['Action', 'Adventure', 'Metroidvania'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Light Up Games'], 'developer': ['Mad Mimic'], 'tag': ['Adventure, ', 'Action, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, ', 'Exploration, ', 'Multiple Endings, ', 'Isometric, ', 'Metroidvania, ', 'Souls-like, ', 'Pirates', 'Adventure, ', 'Action, ', 'Fantasy, ', 'Story Rich, ', 'Atmospheric, '], 'platform_score': '0', 'platform_price': '28.86', 'platform_discount': '0', 'release_date': '2025-02-05T15:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/a86d69c72a440b8ec15917867a695eab99dd1d91771d04031c102a4e9d26931d_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/a86d69c72a440b8ec15917867a695eab99dd1d91771d04031c102a4e9d26931d_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'Star Wars™: Episode I: Jedi Power Battles™', 'genres': ['Action', 'Adventure', 'Sci-fi'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Aspyr'], 'developer': ['Aspyr'], 'tag': ['Adventure, ', 'Action, ', 'Sci-fi, ', 'Third Person, ', 'Space, ', 'Robots', 'Adventure, ', 'Action, ', 'Sci-fi, ', 'Third Person, ', 'Space, '], 'platform_score': '3.7', 'platform_price': '16.75', 'platform_discount': '0', 'release_date': '2025-01-23T17:59:59+02:00', 'game_image': '\n                https://images.gog-statics.com/e1e971f0b61fc21a66ebf4607e8992fd33477777470b0c67b1f38abde1769dba_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/e1e971f0b61fc21a66ebf4607e8992fd33477777470b0c67b1f38abde1769dba_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'The Shell Part III: Paradiso', 'genres': ['Adventure', 'Visual Novel', 'Detective-mystery'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Shiravune'], 'developer': ['Innocent Grey'], 'tag': ['Adventure, ', 'Story Rich, ', 'Atmospheric, ', '2D, ', 'Dark, ', 'Choices Matter, ', 'Horror, ', 'Mystery, ', 'Historical, ', 'Visual Novel, ', 'Sexual Content, ', 'Nudity, ', 'Gore, ', 'Multiple Endings, ', 'Logic, ', 'Mature, ', 'NSFW, ', 'Retro, ', 'Investigation, ', 'Choose Your Own Adventure, ', 'Romance, ', 'Detective-mystery, ', 'Crime, ', 'Text-Based, ', 'Noir, ', 'Philosophical', 'Adventure, ', 'Story Rich, ', 'Atmospheric, ', '2D, ', 'Dark, '], 'platform_score': '3.3', 'platform_price': '16.75', 'platform_discount': '0', 'release_date': '2025-01-23T11:55:00+02:00', 'game_image': '\n                https://images.gog-statics.com/5a8884a41b9269e382f6b9fef93d9bb5048a803b5ae0cd9750c1ceeafb81f438_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/5a8884a41b9269e382f6b9fef93d9bb5048a803b5ae0cd9750c1ceeafb81f438_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': 'SACRIFICE VILLAINS', 'genres': ['Adventure', 'Visual Novel', 'Sci-fi'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Shiravune'], 'developer': ['CLOCKUP'], 'tag': ['Adventure, ', 'Fantasy, ', 'Story Rich, ', '2D, ', 'Sci-fi, ', 'Visual Novel, ', 'Sexual Content, ', 'Nudity, ', 'Mature, ', 'NSFW, ', 'Cartoony, ', 'Post-apocalyptic, ', 'Crime, ', 'Short, ', 'Superhero', 'Adventure, ', 'Fantasy, ', 'Story Rich, ', '2D, ', 'Sci-fi, '], 'platform_score': '2.3', 'platform_price': '16.75', 'platform_discount': '0', 'release_date': '2025-01-21T10:58:00+02:00', 'game_image': '\n                https://images.gog-statics.com/c37c1ee52043af665b4533acefbbddaba1f0b09c5091575d2fb74be8ce836d9b_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/c37c1ee52043af665b4533acefbbddaba1f0b09c5091575d2fb74be8ce836d9b_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}, {'title': "Another Way of Gettin' Paid", 'genres': ['Adventure', 'Visual Novel', 'Fantasy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Shiravune'], 'developer': ['PacoPaco Soft'], 'tag': ['Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Casual, ', 'Funny, ', 'Visual Novel, ', 'Sexual Content, ', 'Nudity, ', 'Mature, ', 'NSFW, ', 'Romance', 'Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Casual, ', 'Funny, '], 'platform_score': '1', 'platform_price': '16.75', 'platform_discount': '0', 'release_date': '2025-01-14T10:58:00+02:00', 'game_image': '\n                https://images.gog-statics.com/5b7ca3bf8e385742fed03ea34fb5b0a287d85f83c82074bd06ec8a2093b2ac41_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/5b7ca3bf8e385742fed03ea34fb5b0a287d85f83c82074bd06ec8a2093b2ac41_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}]


    print(Data)
    print(clean_data(Data))
    print(len(Data))
    print(len(clean_data(Data)))
