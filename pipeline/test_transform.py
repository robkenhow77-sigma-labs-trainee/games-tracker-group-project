"""Script containing all tests for the functions in transform.py."""
# pylint: skip-file

from datetime import datetime

import pytest

from transform import (get_data, is_valid_data, is_valid_title, is_valid_genres, is_valid_publisher,
                       is_valid_developer, is_valid_tag, is_valid_score, is_valid_price, is_valid_discount,
                       is_valid_release, is_valid_image, format_data, format_string, format_list,
                       format_integer, format_release, is_valid_age)

#TODO: rewrite tests that will fail due to it not being today.
#TODO: write tests for string fail where the text is too long
string_validation_fail_test = [123, True, datetime.now(), -2.99, None, "", " "]
string_validation_succeed_test= ["A correct string", "Testing. punctuation!", "numbers 123"]

# Tests for is_valid_title
@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_title_positive(test_input):
    """Tests if is_valid_title returns True when valid data is passed."""

    assert is_valid_title(test_input) is True


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_title_negative(test_input):
    """Tests if is_valid_title returns False when invalid data is passed."""
    assert is_valid_title(test_input) is False


def test_valid_title_too_long():
    """Tests if is_valid_title returns False when invalid data is passed."""
    assert is_valid_title("""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """) is False

# Tests for is_valid_genres
@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_genres_positive(test_input):
    """Tests if is_valid_genres returns True when valid genres are passed."""
    assert is_valid_genres([test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_genres_as_list_positive(test_input):
    """Tests if is_valid_genres returns True when valid genres are passed."""
    assert is_valid_genres([test_input, test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_genres_negative(test_input):
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_genres([test_input]) is False


def test_valid_genres_too_long():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_genres(["""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """]) is False


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_genres_as_list_negative(test_input):
    """Tests if is_valid_genres returns False when valid genres are passed."""
    assert is_valid_genres([test_input, test_input]) is False


def test_valid_genres_positive_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_genres([]) is True


# Tests for is_valid_publisher
@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_publisher_positive(test_input):
    """Tests if is_valid_publisher returns True when a valid publisher is passed."""
    assert is_valid_publisher([test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_publisher_as_list_positive(test_input):
    """Tests if is_valid_publisher returns True when a valid publisher is passed."""
    assert is_valid_publisher([test_input, test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_publisher_negative(test_input):
    """Tests if is_valid_publisher returns False when an invalid publisher is passed."""
    assert is_valid_publisher([test_input]) is False


def test_valid_publisher_too_long():
    """Tests if is_valid_publisher returns False when an invalid publisher is passed."""
    assert is_valid_publisher(["""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """]) is False


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_publisher_as_list_negative(test_input):
    """Tests if is_valid_publisher returns False when an invalid publisher is passed."""
    assert is_valid_publisher([test_input, test_input]) is False


def test_valid_publishers_positive_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_publisher([]) is True


# Tests for is_valid_developer
@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_developer_positive(test_input):
    """Tests if is_valid_developer returns True when a valid developer is passed."""
    assert is_valid_developer([test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_developer_as_list_positive(test_input):
    """Tests if is_valid_developer returns True when a valid developer is passed."""
    assert is_valid_developer([test_input, test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_developer_negative(test_input):
    """Tests if is_valid_developer returns False when an invalid developer is passed."""
    assert is_valid_developer([test_input]) is False


def test_valid_developer_too_long():
    """Tests if is_valid_developer returns False when an invalid developer is passed."""
    assert is_valid_developer(["""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """]) is False


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_developer_as_list_negative(test_input):
    """Tests if is_valid_developer returns False when an invalid developer is passed."""
    assert is_valid_developer([test_input, test_input]) is False


def test_valid_developer_positive_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_developer([]) is True


# Tests for is_valid_tag
@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_tag_positive(test_input):
    """Tests if is_valid_tag returns True when valid tags are passed."""
    assert is_valid_tag([test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_succeed_test)
def test_valid_tag_as_list_positive(test_input):
    """Tests if is_valid_tag returns True when valid tags are passed."""
    assert is_valid_tag([test_input, test_input]) is True


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_tag_negative(test_input):
    """Tests if is_valid_tag returns False when invalid tags are passed."""
    assert is_valid_tag([test_input]) is False


def test_valid_tag_too_long():
    """Tests if is_valid_tag returns False when invalid tags are passed."""
    assert is_valid_tag(["""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """]) is False


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_tag_as_list_negative(test_input):
    """Tests if is_valid_tag returns False when invalid tags are passed."""
    assert is_valid_tag([test_input, test_input]) is False


def test_valid_tag_positive_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_tag([]) is True


# Tests for is_valid_score
pos_score = ['0', '100', '55', '  60   ']
@pytest.mark.parametrize("test_input", pos_score)
def test_valid_score_positive(test_input):
    """Tests if is_valid_score returns True when a valid score is passed."""
    assert is_valid_score(test_input) is True


neg_score = [None, 100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", [], ""]
@pytest.mark.parametrize("test_input", neg_score)
def test_valid_score_negative(test_input):
    """Tests if is_valid_score returns False when an invalid score is passed."""
    assert is_valid_score(test_input) is False

#TODO: add free option
pos_price = ['10', '100', '5500', '       9 ']
@pytest.mark.parametrize("test_input", pos_price)
def test_valid_price_positive(test_input):
    """Tests if is_valid_price returns True when a valid price is passed."""
    assert is_valid_price(test_input) is True


neg_price = [None, 100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", [], ""]
@pytest.mark.parametrize("test_input", neg_price)
def test_valid_price_negative(test_input):
    """Tests if is_valid_price returns False when an invalid price is passed."""
    assert is_valid_price(test_input) is False


# Tests for is_valid_discount
pos_discount = ['0', '100', '55', '1', None, '  11  ']
@pytest.mark.parametrize("test_input", pos_discount)
def test_valid_discount_positive(test_input):
    """Tests if is_valid_discount returns True when a valid discount percentage is passed."""
    assert is_valid_discount(test_input) is True


neg_discount = [100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", "110", [], ""]
@pytest.mark.parametrize("test_input", neg_discount)
def test_valid_discount_negative(test_input):
    """Tests if is_valid_discount returns False when an invalid discount is passed."""
    assert is_valid_discount(test_input) is False


# Tests for is_valid_release
#TODO: parameterise this
def test_valid_release_positive():
    """Tests if is_valid_release returns True when a valid release date is passed."""
    assert is_valid_release(datetime.strftime(datetime.now(), "%d %b, %Y"))


neg_release = [None, 100, 'words', True, -2.99, "50.3", "89%", "-10", "110", []]
@pytest.mark.parametrize("test_input", neg_discount)
def test_valid_release_negative(test_input):
    """Tests if is_valid_release returns False when an invalid release date is passed."""
    assert is_valid_release(test_input) is False


def test_valid_release_day_way_out_of_range():
    """Tests if is_valid_release returns False when an invalid release date is passed."""
    assert is_valid_release("10 Jan, 2001") is False


# Tests for is_valid_image
pos_image = ['https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786']
@pytest.mark.parametrize("test_input", pos_image)
def test_valid_image_positive(test_input):
    """Tests if is_valid_image returns True when a valid image URL is passed."""
    assert is_valid_image(test_input) is True


neg_image = [None, 100, 'words', True, -2.99, "50.3", "89%", "-10", "110", [], "http://example.com/image.jpg"]
@pytest.mark.parametrize("test_input", neg_image)
def test_valid_image_negative(test_input):
    """Tests if is_valid_image returns False when an invalid image URL is passed."""
    assert is_valid_image(test_input) is False


def test_valid_image_too_long():
    """Tests if is_valid_image returns False when an invalid image URL is passed."""
    assert is_valid_image("""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """) is False


pos_price = ['3', '7', '12', '       16 ', '18 ', None]
@pytest.mark.parametrize("test_input", pos_price)
def test_valid_age_positive(test_input):
    """Tests if is_valid_price returns True when a valid price is passed."""
    assert is_valid_age(test_input) is True


neg_price = [100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", [], "", "15", " "]
@pytest.mark.parametrize("test_input", neg_price)
def test_valid_age_negative(test_input):
    """Tests if is_valid_price returns False when an invalid price is passed."""
    assert is_valid_age(test_input) is False


valid_games = [{'title': 'Hearts of Iron IV', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy', 'Simulation', 'Strategy'], 'publisher': [], 'developer': [], 'tag': ['Strategy', 'World%20War%20II', 'Grand%20Strategy', 'War', 'Historical', 'Military', 'Alternate%20History', 'Multiplayer', 'Simulation', 'Tactical', 'Real-Time%20with%20Pause', 'Singleplayer', 'RTS', 'Diplomacy', 'Sandbox', 'Co-op', 'Strategy%20RPG', 'Competitive', 'Open%20World', 'Action'], 'platform_score': '90', 'platform_price': '4199', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786', 'age_rating': '7'}]


# Define the list of required keys
REQUIRED_KEYS = [
    'title', 'genres', 'publisher', 'developer', 'tag',
    'platform_score', 'platform_price', 'platform_discount',
    'release_date', 'game_image', 'age_rating', 'platform_score'
]

# Define a function that checks if all required keys are present
def has_all_required_keys(game):
    return all(key in game for key in REQUIRED_KEYS)

# Sample test cases
@pytest.mark.parametrize("game,expected", [
    (
        # Valid example
        {'title': 'Hearts of Iron IV', 'genres': ['Strategy'], 'publisher': [],
         'developer': [], 'tag': [], 'platform_score': '90', 'platform_price': '4199',
         'platform_discount': None, 'release_date': '12 Feb, 2025',
         'game_image': '<https://shared.cloudflare.steamstatic.com/...>', 'age_rating': '7'},
        True
    ),
    (
        # Missing a key
        {'title': 'Hearts of Iron IV', 'genres': ['Strategy'], 'publisher': [],
         'developer': [], 'tag': [], 'platform_score': '90', 'platform_price': '4199',
         'platform_discount': None, 'release_date': '12 Feb, 2025', 'age_rating': '7'},
        False
    ),
    (
        # Extra key but still valid
        {'title': 'Hearts of Iron IV', 'genres': ['Strategy'], 'publisher': [],
         'developer': [], 'tag': [], 'platform_score': '90', 'platform_price': '4199',
         'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': '<https://shared.cloudflare.steamstatic.com/...>',
         'age_rating': '7', 'extra_key': 'some_value'},
        True
    ),
])
def test_valid_game_keys_present(game, expected):
    assert has_all_required_keys(game) == expected


# Define a function that checks if all required keys are present
def has_all_required_keys(game):
    return all(key in game for key in REQUIRED_KEYS)

# Valid complete game example
VALID_GAME = {
    'title': 'Hearts of Iron IV', 
    'genres': ['Strategy'], 
    'publisher': [],
    'developer': [], 
    'tag': [], 
    'platform_score': '90', 
    'platform_price': '4199',
    'platform_discount': None, 
    'release_date': '12 Feb, 2025', 
    'game_image': '<https://shared.cloudflare.steamstatic.com/...>', 
    'age_rating': '7'
}

# Test cases where each key is missing one at a time
@pytest.mark.parametrize("game,expected", [
    # Valid game (all keys present)
    (VALID_GAME, True)
] + [
    # Create a test case for each missing key
    (
        {key: value for key, value in VALID_GAME.items() if key != missing_key},
        False
    )
    for missing_key in REQUIRED_KEYS
])
def test_keys_present(game, expected):
    assert has_all_required_keys(game) == expected


# Format function tests would involve more thorough testing frameworks, such as using mocked data.
# Here's an example for format_data:
#TODO: parameterise this
def test_format_data():
    """Tests format_data to ensure it returns correctly formatted data."""
    input_data = {'title': 'Hearts of Iron IV', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy', 'Simulation', 'Strategy'], 'publisher': [], 'developer': [], 'tag': ['Strategy', 'World%20War%20II', 'Grand%20Strategy', 'War', 'Historical', 'Military', 'Alternate%20History', 'Multiplayer', 'Simulation', 'Tactical', 'Real-Time%20with%20Pause', 'Singleplayer', 'RTS', 'Diplomacy', 'Sandbox', 'Co-op', 'Strategy%20RPG', 'Competitive', 'Open%20World', 'Action'], 'platform_score': '90', 'platform_price': '4199', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786', 'age_rating': '7'}
    expected_output = {'title': 'Hearts of Iron IV', 'genre': ['Free to Play', 'Early Access', 'Strategy', 'Simulation', 'Strategy'], 'publisher': [], 'developer': [], 'score': 90,'tag': ['Strategy', 'World War II', 'Grand Strategy', 'War', 'Historical', 'Military', 'Alternate History', 'Multiplayer', 'Simulation', 'Tactical', 'Real-Time with Pause', 'Singleplayer', 'RTS', 'Diplomacy', 'Sandbox', 'Co-op', 'Strategy RPG', 'Competitive', 'Open World', 'Action'], 'price': 4199, 'discount': None, 'release': datetime(2025, 2, 12, 0, 0), 'image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786', 'platform': 'Steam', 'age_rating': '7'}
    assert format_data(input_data) == expected_output

data = [(" ", ""), ("string   ", "string"), ("normal", "normal"), ("normal%20test", "normal test")]
@pytest.mark.parametrize("string,expected", data)
def test_format_string(string, expected):
    """Tests format_string function."""
    assert format_string(string) == expected

data = [([" ", "string   "], ["", "string"]), (["normal", "normal%20test"], ["normal", "normal test"])]
@pytest.mark.parametrize("string,expected", data)
def test_format_list(string, expected):
    """Tests format_list function."""
    assert format_list(string) == expected

data = [("1", 1), ("2   ", 2), ("   100 ", 100), (None, None)]
@pytest.mark.parametrize("string,expected", data)
def test_format_integer(string, expected):
    """Tests format_integer function."""
    assert format_integer(string) == expected


def test_format_release():
    """Tests format_release function"""
    assert format_release("    10 Feb, 2022") == datetime.strptime("10 Feb, 2022", "%d %b, %Y")


@pytest.mark.parametrize("test_input", valid_games)
def test_valid_game(test_input):
    """Tests that a valid game passes."""
    assert is_valid_data(test_input)
