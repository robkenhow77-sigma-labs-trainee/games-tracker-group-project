"""Script containing all tests for the functions in transform.py."""
# pylint: skip-file

from datetime import datetime, timedelta

import pytest

from gog_transform import (is_valid_data, is_valid_title, is_valid_genres, is_valid_publisher,
                       is_valid_developer, is_valid_tag, is_valid_score, is_valid_price, is_valid_discount,
                       is_valid_release, is_valid_image, format_data, format_string,
                       format_integer, format_release, is_valid_age, format_genre_list, format_developer_list,
                       format_publisher_list, format_tag_list, is_valid_genre, is_valid_pub, is_valid_dev,
                       is_valid_single_tag)

#TODO: rewrite tests that will fail due to it not being today.
string_validation_fail_test = [123, True, datetime.now(), -2.99, None, "", " "]
string_validation_succeed_test= ["A correct string", "Testing. punctuation!", "numbers 123", "adding", "more", 'for', "zip"]

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


@pytest.mark.parametrize("test_input", [[x, y] for x, y in zip(string_validation_fail_test, string_validation_succeed_test)])
def test_valid_genres_positive_if_one_passes(test_input):
    assert is_valid_genres(test_input) is True


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_genres_as_list_negative(test_input):
    """Tests if is_valid_genres returns False when valid genres are passed."""
    assert is_valid_genres([test_input, test_input]) is False


def test_valid_genres_negative_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_genres([]) is False


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


def test_valid_publishers_negative_empty_array():
    """Tests if is_valid_publishers returns False when invalid publishers are passed."""
    assert is_valid_publisher([]) is False


@pytest.mark.parametrize("test_input", [[x, y] for x, y in zip(string_validation_fail_test, string_validation_succeed_test)])
def test_valid_publisher_positive_if_one_passes(test_input):
    assert is_valid_publisher(test_input) is True


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


def test_valid_developer_negative_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_developer([]) is False


@pytest.mark.parametrize("test_input", [[x, y] for x, y in zip(string_validation_fail_test, string_validation_succeed_test)])
def test_valid_developer_positive_if_one_passes(test_input):
    assert is_valid_developer(test_input) is True


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

test_list = [
    ("Action", True),
    ("Drama123", True),
    ("Comedy!!", True),
    ("Sci-Fi", True),
    ("Thril_ler", True),
    ("", False),
    (" ", False),
    ("""
    [[ ]] The story goes like this: Earth is captured by a technocapital singularity as renaissance
    rationalitization and oceanic navigation lock into commoditization take-off.
    Logistically accelerating techno-economic interactivity crumbles social order in
    auto-sophisticating machine runaway. As markets learn to manufacture intelligence,
    politics modernizes, upgrades paranoia, and tries to get a grip.
    """, False),
    ("  ", False),
    (123, False),
    (None, False), 
    ("genre with spaces", True),
    (False, False)]

@pytest.mark.parametrize("test_input,output", test_list)
def test_is_valid_genre(test_input, output):
    """Tests is_valid_genre outputs the correct output."""
    assert is_valid_genre(test_input) == output


@pytest.mark.parametrize("test_input,output", test_list)
def test_is_valid_pub(test_input, output):
    """Tests is_valid_pub outputs the correct output."""
    assert is_valid_pub(test_input) == output


@pytest.mark.parametrize("test_input,output", test_list)
def test_is_valid_dev(test_input, output):
    """Tests is_valid_dev outputs the correct output."""
    assert is_valid_dev(test_input) == output


@pytest.mark.parametrize("test_input,output", test_list)
def test_is_valid_single_tag(test_input, output):
    """Tests is_valid_single_tag outputs the correct output."""
    assert is_valid_single_tag(test_input) == output


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


def test_valid_tag_negative_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_tag([]) is False


@pytest.mark.parametrize("test_input", [[x, y] for x, y in zip(string_validation_fail_test, string_validation_succeed_test)])
def test_valid_tag_positive_if_one_passes(test_input):
    assert is_valid_tag(test_input) is True


pos_score = ['5', '0', '1.7', '  4.5   ']
@pytest.mark.parametrize("test_input", pos_score)
def test_valid_score_positive(test_input):
    """Tests if is_valid_score returns True when a valid score is passed."""
    assert is_valid_score(test_input) is True


neg_score = [None, 100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", [], ""]
@pytest.mark.parametrize("test_input", neg_score)
def test_valid_score_negative(test_input):
    """Tests if is_valid_score returns False when an invalid score is passed."""
    assert is_valid_score(test_input) is False


pos_price = ['10', '100', '5500', '       9 ', '0','2.99',' 30.99']
@pytest.mark.parametrize("test_input", pos_price)
def test_valid_price_positive(test_input):
    """Tests if is_valid_price returns True when a valid price is passed."""
    assert is_valid_price(test_input) is True


neg_price = [None, 100, 'words', True, datetime.now(), -2.99, "89%", "-10", [], ""]
@pytest.mark.parametrize("test_input", neg_price)
def test_valid_price_negative(test_input):
    """Tests if is_valid_price returns False when an invalid price is passed."""
    assert is_valid_price(test_input) is False


pos_discount = ['0', '100', '55', '1', '  11  ']
@pytest.mark.parametrize("test_input", pos_discount)
def test_valid_discount_positive(test_input):
    """Tests if is_valid_discount returns True when a valid discount percentage is passed."""
    assert is_valid_discount(test_input) is True


neg_discount = [100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", "110", [], "", None]
@pytest.mark.parametrize("test_input", neg_discount)
def test_valid_discount_negative(test_input):
    """Tests if is_valid_discount returns False when an invalid discount is passed."""
    assert is_valid_discount(test_input) is False


#TODO: parameterise this
def test_valid_release_positive():
    """Tests if is_valid_release returns True when a valid release date is passed."""
    assert is_valid_release(datetime.strftime(datetime.now(), "%Y-%m-%d"))


neg_release = [None, 100, 'words', True, -2.99, "50.3", "89%", "-10", "110", []]
@pytest.mark.parametrize("test_input", neg_discount)
def test_valid_release_negative(test_input):
    """Tests if is_valid_release returns False when an invalid release date is passed."""
    assert is_valid_release(test_input) is False


def test_valid_release_day_way_out_of_range():
    """Tests if is_valid_release returns False when an invalid release date is passed."""
    assert is_valid_release("10 Jan, 2001") is False


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


pos_age = ['3', '7', '12', '       16 ', '18 ']
@pytest.mark.parametrize("test_input", pos_age)
def test_valid_age_positive(test_input):
    """Tests if is_valid_price returns True when a valid price is passed."""
    assert is_valid_age(test_input) is True


neg_age = [None, 100, 'words', True, datetime.now(), -2.99, "50.3", "89%", "-10", [], "", "15", " "]
@pytest.mark.parametrize("test_input", neg_age)
def test_valid_age_negative(test_input):
    """Tests if is_valid_price returns False when an invalid price is passed."""
    assert is_valid_age(test_input) is False


valid_games = [{'title': 'SACRIFICE VILLAINS', 'genres': ['Adventure', 'Visual Novel', 'Sci-fi'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'Shiravune'], 'developer': ['CLOCKUP'], 'tag': ['Adventure, ', 'Fantasy, ', 'Story Rich, ', '2D, ', 'Sci-fi, ', 'Visual Novel, ', 'Sexual Content, ', 'Nudity, ', 'Mature, ', 'NSFW, ', 'Cartoony, ', 'Post-apocalyptic, ', 'Crime, ', 'Short, ', 'Superhero', 'Adventure, ', 'Fantasy, ', 'Story Rich, ', '2D, ', 'Sci-fi, '], 'platform_score': '2.3', 'platform_price': '16.75', 'platform_discount': '0', 'release_date': '2025-01-21T10:58:00+02:00', 'game_image': '\n                https://images.gog-statics.com/c37c1ee52043af665b4533acefbbddaba1f0b09c5091575d2fb74be8ce836d9b_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/c37c1ee52043af665b4533acefbbddaba1f0b09c5091575d2fb74be8ce836d9b_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': None}]

@pytest.mark.parametrize("missing_key", [
    'title', 'genres', 'publisher', 'developer', 'tag',
    'platform_score', 'platform_price', 'platform_discount',
    'release_date', 'game_image', 'age_rating'
])
def test_is_valid_data_with_missing_keys(missing_key):
    # Base dictionary with all valid keys
    valid_game = {'title': 'Hearts of Iron IV', 'genres': ['Free%20to%20Play', 'Early%20Access', 'Strategy', 'Simulation', 'Strategy'], 'publisher': [], 'developer': [], 'tag': ['Strategy', 'World%20War%20II', 'Grand%20Strategy', 'War', 'Historical', 'Military', 'Alternate%20History', 'Multiplayer', 'Simulation', 'Tactical', 'Real-Time%20with%20Pause', 'Singleplayer', 'RTS', 'Diplomacy', 'Sandbox', 'Co-op', 'Strategy%20RPG', 'Competitive', 'Open%20World', 'Action'], 'platform_score': '90', 'platform_price': '4199', 'platform_discount': None, 'release_date': '12 Feb, 2025', 'game_image': 'https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/394360/header.jpg?t=1739207786', 'age_rating': '7'}

    # Remove one key to simulate the missing key scenario
    invalid_game = valid_game.copy()
    invalid_game.pop(missing_key)

    # Assert that the function returns False when a key is missing
    assert not is_valid_data(invalid_game)

today = datetime.now().date()
today_string = today.strftime("%Y-%m-%d")
input_game = {'title': 'The Witcher 3: Wild Hunt - Complete Edition', 'genres': ['Role-playing', 'Adventure', 'Fantasy'], 'publisher': ['Browse all CD PROJEKT RED games »', 'CD PROJEKT RED', 'CD PROJEKT RED'], 'developer': ['CD PROJEKT RED'], 'tag': ['Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, ', 'Exploration, ', 'Great Soundtrack, ', 'Choices Matter, ', 'Open World, ', 'Third Person, ', 'Sexual Content, ', 'Violent, ', 'Nudity, ', 'Gore, ', 'Multiple Endings, ', 'Mature, ', 'Magic, ', 'Medieval, ', 'Vampire, ', 'Werewolves', 'Adventure, ', 'Fantasy, ', 'Story Rich, ', 'Role-playing, ', 'Atmospheric, '], 'platform_score': '4.8', 'platform_price': '34.99', 'platform_discount': '80', 'release_date': today_string, 'game_image': '\n                https://images.gog-statics.com/90dc4e2c86b036c2b2c392adea197ad7dc6b750ce01af0416ed8b37f3d0101c9_product_card_v2_logo_480x285.png 1x,\n                https://images.gog-statics.com/90dc4e2c86b036c2b2c392adea197ad7dc6b750ce01af0416ed8b37f3d0101c9_product_card_v2_logo_960x570.png 2x\n            ', 'age_rating': '18'}
expected_output = {'title': 'The Witcher 3: Wild Hunt - Complete Edition', 'genres': ['Role-playing', 'Adventure', 'Fantasy'], 'platform_price': 3499, 'platform': 'GOG', 'publisher': ['CD PROJEKT RED', 'CD PROJEKT RED'], 'developer': ['CD PROJEKT RED'], 'tag': ['Adventure', 'Fantasy', 'Story Rich', 'Role-playing', 'Atmospheric', 'Exploration', 'Great Soundtrack', 'Choices Matter', 'Open World', 'Third Person', 'Sexual Content', 'Violent', 'Nudity', 'Gore', 'Multiple Endings', 'Mature', 'Magic', 'Medieval', 'Vampire', 'Werewolves', 'Adventure', 'Fantasy', 'Story Rich', 'Role-playing', 'Atmospheric'], 'platform_score': 96, 'platform_discount': 80, 'release_date': today, 'game_image': 'https://images.gog-statics.com/90dc4e2c86b036c2b2c392adea197ad7dc6b750ce01af0416ed8b37f3d0101c9_product_card_v2_logo_480x285.png', 'age_rating': 'PEGI 18', 'NSFW': True}

#TODO: parameterise this
def test_format_data():
    """Tests format_data to ensure it returns correctly formatted data."""

    assert format_data(input_game) == expected_output

data = [(" ", ""), ("string   ", "string"), ("normal", "normal"), ("normal%20test", "normal test")]
@pytest.mark.parametrize("string,expected", data)
def test_format_string(string, expected):
    """Tests format_string function."""
    assert format_string(string) == expected

data = [("1", 1), ("2   ", 2), ("   100 ", 100)]
@pytest.mark.parametrize("string,expected", data)
def test_format_integer(string, expected):
    """Tests format_integer function."""
    assert format_integer(string) == expected


def test_format_release():
    """Tests format_release function"""
    assert format_release('  2025-01-31T16:59:00+02:00  ') == datetime.strptime("2025-01-31", "%Y-%m-%d").date()

def test_valid_game():
    """Tests that a valid game passes."""
    assert is_valid_data(input_game)

list_test_values = [("fail", []), ([], []), ([123, "test"], ["test"]),
(["test1", "test2"], ["test1", "test2"]),(["    test", False, 123, "test2  "], ["test","test2"])]

@pytest.mark.parametrize("test_input,correct_output", list_test_values)
def test_format_genre(test_input, correct_output):
    """Tests the format_genre_list function."""
    assert format_genre_list(test_input) == correct_output


@pytest.mark.parametrize("test_input,correct_output", list_test_values)
def test_format_developer(test_input, correct_output):
    """Tests the format_developer_list function."""
    assert format_developer_list(test_input) == correct_output


@pytest.mark.parametrize("test_input,correct_output", list_test_values)
def test_format_publisher(test_input, correct_output):
    """Tests the format_publisher_list function."""
    assert format_publisher_list(test_input) == correct_output


@pytest.mark.parametrize("test_input,correct_output", list_test_values)
def test_format_tag(test_input, correct_output):
    """Tests the format_tag_list function."""
    assert format_tag_list(test_input) == correct_output


def test_valid_release_delta_input():
    """Tests that games before today are allowed if timedelta is set."""
    today = datetime.now().date()
    a_week_ago = today - timedelta(days=7)
    string_a_week_ago = datetime.strftime(a_week_ago, "%Y-%m-%d")
    assert is_valid_release(string_a_week_ago, 7)


def test_format_data_invalid_publisher():
    """Tests that an empty list is returned for publisher if no valid specified publisher."""
    test_input = input_game
    test_input['publisher'] = ""
    test_output = expected_output
    test_output['publisher'] = []
    assert format_data(test_input) == test_output


def test_format_data_invalid_developer():
    """Tests that an empty list is returned for developer if no valid specified developer."""
    test_input = input_game
    test_input['developer'] = ""
    test_output = expected_output
    test_output['developer'] = []
    assert format_data(test_input) == test_output


def test_format_data_invalid_tag():
    """Tests that an empty list is returned for tag if no valid specified tag."""
    test_input = input_game
    test_input['tag'] = ""
    test_output = expected_output
    test_output['NSFW'] = False
    test_output['tag'] = []
    assert format_data(test_input) == test_output


def test_format_data_invalid_score():
    """Tests that None is returned for score if no valid specified score."""
    test_input = input_game
    test_input['platform_score'] = ""
    test_output = expected_output
    test_output['platform_score'] = -1
    assert format_data(test_input) == test_output


def test_format_data_invalid_discount():
    """Tests that None is returned for discount if no valid specified discount."""
    test_input = input_game
    test_input['platform_discount'] = ""
    test_output = expected_output
    test_output['platform_discount'] = 0
    assert format_data(test_input) == test_output


def test_format_data_invalid_release():
    """Tests that None is returned for release if no valid specified release."""
    test_input = input_game
    test_input['release_date'] = ""
    test_output = expected_output
    test_output['release_date'] = None
    assert format_data(test_input) == test_output


def test_format_data_invalid_image():
    """Tests that None is returned for image if no valid specified image."""
    test_input = input_game
    test_input['game_image'] = ""
    test_output = expected_output
    test_output['game_image'] = "N/A"
    assert format_data(test_input) == test_output


def test_format_data_invalid_age():
    """Tests that None is returned for age if no valid specified age."""
    test_input = input_game
    test_input['age_rating'] = ""
    test_output = expected_output
    test_output['age_rating'] = "Not Assigned"
    assert format_data(test_input) == test_output
