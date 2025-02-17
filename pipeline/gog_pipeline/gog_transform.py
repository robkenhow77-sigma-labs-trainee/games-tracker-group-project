"""Script containing all functions pertaining to cleaning the data before insertion."""

from datetime import datetime, timedelta
import urllib.parse

from requests import get

#TODO: ensure logger is imported and config-ed

def clean_data(data: list[dict], target_date=None) -> list[dict]:
    """Cleans the data extracted from the GoG scraper."""

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
    return (today-input_date).days


def is_valid_data(game: dict, days_to_accept=0) -> bool:
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
            is_valid_price(game['platform_price']) and
            is_valid_release(game['release_date'], days_to_accept))


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

    return 0 <= int(price) <= 32767 # smallint limit


def is_valid_discount(discount: int) -> bool:
    """Returns true if discount is valid."""

    #Not on discount currently
    if discount is None:
        return False

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
                     days_before_today_allowed=0) -> bool:
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
    if image[-2:] == "1x":
        image = image[:-2]

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


def format_data(game: dict, days_before_today_allowed=0) -> bool:
    """Formats all the data."""

    formatted_data = {}

    # Minimum required data
    formatted_data['title'] = format_string(game['title'])
    formatted_data['genres'] = format_genre_list(game['genres'])
    formatted_data['platform_price'] = format_price(game['platform_price'])
    formatted_data['platform'] = "GOG"

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
    if is_valid_release(game['release_date'], days_before_today_allowed):
        formatted_data['release_date'] = format_release(game['release_date'])
    else:
        formatted_data['release_date'] = None
    if is_valid_image(game['game_image']):
        formatted_data['game_image'] = format_image(game['game_image'])
        if formatted_data['game_image'][-2:] == "1x":
            formatted_data['game_image'] = formatted_data['game_image'][:-2]
    else:
        formatted_data['game_image'] = 'N/A'
    if is_valid_age(game['age_rating']):
        formatted_data['age_rating'] = "PEGI " + format_string(game['age_rating'])
    else:
        formatted_data['age_rating'] = "Not Assigned"
    return formatted_data


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

    integer = integer.strip()
    return int(integer)


def format_price(price: str) -> int:
    """Returns the price in pence."""

    price = price.strip().replace('.','')

    return int(price)


def format_score(score: str) -> int:
    """Formats the score as a percentage."""

    score = score.strip()

    if '.' in score:
        unit, decimal = score.split('.')
        score = int(unit) * 20 + int(decimal) * 2

    else:
        score = int(score) * 20

    return int(score)


def format_image(image: str) -> str:
    """returns the URL for the first image."""

    image = image.replace(" ",'')
    image = image.replace("\n",'')
    image = image.split(',')[0]
    image = image.strip()
    if image[-2:] == "1x":
        image = image[:-2]
    
    return image


def format_release(release: str) -> datetime:
    """Formats release."""

    if not release or not isinstance(release, str):
        return None

    release = release.strip()
    release = release[:10]

    try:
        formatted_release = datetime.strptime(release, "%Y-%m-%d")
        return formatted_release.date()
    except ValueError:
        return None


if __name__ == "__main__":

    test_input = [{'title': 'The Witcher 3: Wild Hunt - Complete Edition', 'genres': ['Role-playing', 'Adventure', 'Fantasy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'CD PROJEKT RED'], 'developer': ['CD PROJEKT RED'], 'tag': ['Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Exploration, ', 'Great Soundtrack, ', 'Choices Matter, ', 'Open World, ', 'Third Person, ', 'Sexual Content, ', 'Violent, ', 'Nudity, ', 'Gore, ', 'Multiple Endings, ', 'Mature, ', 'Magic, ', 'Medieval, ', 'Vampire, ', 'Werewolves', 'Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, '], 'platform_score': '4.8', 'platform_price': '34.99', 'platform_discount': '80', 'release_date': '2016-08-30T00:00:00+03:00', 'game_image': '\n                https://images.gog-statics.com/90dc4e2c86b036c2b2c392adea197ad7dc6b750ce01af0416ed8b37f3d0101c9_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/90dc4e2c86b036c2b2c392adea197ad7dc6b750ce01af0416ed8b37f3d0101c9_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': '18'}]

    clean = clean_data(test_input, '01 Jan, 2015')
    print(test_input)
    print(clean)
    print(len(test_input))
    print(len(clean))
