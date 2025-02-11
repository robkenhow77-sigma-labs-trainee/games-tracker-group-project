"""Script containing all tests for the functions in transform.py."""

from datetime import datetime

import pytest

from transform import (get_data, is_valid_data, is_valid_title, is_valid_genres, is_valid_publisher,
                       is_valid_developer, is_valid_tag, is_valid_score, is_valid_price, is_valid_discount,
                       is_valid_release, is_valid_image, format_data, format_title, format_genres,
                       format_publisher, format_developer, format_tag, format_score, format_price,
                       format_discount, format_release, format_image)



string_validation_fail_test = [123, True, datetime.now(), -2.99, None, ""]
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


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_publisher_as_list_negative(test_input):
    """Tests if is_valid_publisher returns False when an invalid publisher is passed."""
    assert is_valid_publisher([test_input, test_input]) is False


def test_valid_publishers_negative_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_publisher([]) is False


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


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_developer_as_list_negative(test_input):
    """Tests if is_valid_developer returns False when an invalid developer is passed."""
    assert is_valid_developer([test_input, test_input]) is False


def test_valid_developer_negative_empty_array():
    """Tests if is_valid_genres returns False when invalid genres are passed."""
    assert is_valid_developer([]) is False


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


@pytest.mark.parametrize("test_input", string_validation_fail_test)
def test_valid_tag_as_list_negative(test_input):
    """Tests if is_valid_tag returns False when invalid tags are passed."""
    assert is_valid_tag([test_input, test_input]) is False


# Tests for is_valid_score
#TODO: parameterise this
def test_valid_score_positive():
    """Tests if is_valid_score returns True when a valid score is passed."""
    assert is_valid_score('80') is True

#TODO: parameterise this
def test_valid_score_negative():
    """Tests if is_valid_score returns False when an invalid score is passed."""
    assert is_valid_score(-10) is False
    assert is_valid_score("Not a Number") is False

#TODO: parameterise this
# Tests for is_valid_price
def test_valid_price_positive():
    """Tests if is_valid_price returns True when a valid price is passed."""
    assert is_valid_price("3000") is True

#TODO: parameterise this
def test_valid_price_negative():
    """Tests if is_valid_price returns False when an invalid price is passed."""
    assert is_valid_price(1.99) is False
    assert is_valid_price("Free") is False

#TODO: parameterise this
# Tests for is_valid_discount
def test_valid_discount_positive():
    """Tests if is_valid_discount returns True when a valid discount percentage is passed."""
    assert is_valid_discount("50") is True

#TODO: parameterise this
def test_valid_discount_negative():
    """Tests if is_valid_discount returns False when an invalid discount is passed."""
    assert is_valid_discount(150) is False
    assert is_valid_discount("Fifty Percent") is False
    assert is_valid_discount("150%") is False


# Tests for is_valid_release
#TODO: parameterise this
def test_valid_release_positive():
    """Tests if is_valid_release returns True when a valid release date is passed."""
    assert is_valid_release(datetime.strftime(datetime.now(), "%d %b, %Y"))


#TODO: parameterise this
def test_valid_release_negative():
    """Tests if is_valid_release returns False when an invalid release date is passed."""
    assert is_valid_release("Not a Date") is False
    assert is_valid_release("") is False
    #TODO: set a date that is two days before today with mocking
    assert is_valid_release("") is False


# Tests for is_valid_image
#TODO: parameterise this
def test_valid_image_positive():
    """Tests if is_valid_image returns True when a valid image URL is passed."""
    #TODO: add a real picture here
    assert is_valid_image("http://example.com/image.jpg") is True


#TODO: parameterise this
def test_valid_image_negative():
    """Tests if is_valid_image returns False when an invalid image URL is passed."""
    assert is_valid_image("Not a URL") is False
    assert is_valid_image("") is False


# Format function tests would involve more thorough testing frameworks, such as using mocked data.
# Here's an example for format_data:
#TODO: parameterise this
def test_format_data():
    """Tests format_data to ensure it returns correctly formatted data."""
    input_data = {
        "title": " Unformatted TITLE ",
        "genres": "ACtion,!adventure",
        # ...other raw data...
    }
    expected_output = {
        "title": "Unformatted Title",
        "genres": ["action", "Adventure"],
        # ...expected formatted data...
    }
    assert format_data(input_data) == expected_output


# Tests for format_title
#TODO: parameterise this
def test_format_title():
    """Tests to ensure format_title formats correctly."""
    assert format_title(" Unformatted TITLE ") == "unformatted title"
    assert format_title("") == ""


# Tests for format_genres
#TODO: parameterise this
def test_format_genres():
    """Tests to ensure format_genres formats correctly."""
    assert format_genres("actiON,advENTure") == ["action", "adventure"]
    assert format_genres("") == []


# Tests for format_publisher
#TODO: parameterise this
def test_format_publisher():
    """Tests to ensure format_publisher formats correctly."""
    assert format_publisher(" unformatted publisher ") == "unformatted publisher"
    assert format_publisher("") == ""


# Tests for format_developer
#TODO: parameterise this
def test_format_developer():
    """Tests to ensure format_developer formats correctly."""
    assert format_developer(" UNFORMATTED developer ") == "unformatted developer"
    assert format_developer("") == ""


# Tests for format_tag
#TODO: parameterise this
def test_format_tag():
    """Tests to ensure format_tag formats correctly."""
    assert format_tag("multiplayer,singleplayer") == ["Multiplayer", "Singleplayer"]
    assert format_tag("") == []


# Tests for format_score
#TODO: parameterise this
def test_format_score():
    """Tests to ensure format_score formats correctly."""
    assert format_score(" 85 ") == 85
    assert format_score(" invalid ") is None


# Tests for format_price
#TODO: parameterise this
def test_format_price():
    """Tests to ensure format_price formats correctly."""
    assert format_price(" 59.99 ") == 5999
    assert format_price("invalid") is None


# Tests for format_discount
#TODO: parameterise this
def test_format_discount():
    """Tests to ensure format_discount formats correctly."""
    assert format_discount(" 50% ") == 50
    assert format_discount("invalid") is None


# Tests for format_release
#TODO: parameterise this
def test_format_release():
    """Tests to ensure format_release formats correctly."""
    #TODO: make this datetime
    assert format_release(" 2023-10-01 ") == "2023-10-01"
    assert format_release("Invalid Date") == ""


# Tests for format_image
#TODO: parameterise this
def test_format_image():
    """Tests to ensure format_image formats correctly."""
    assert format_image("< http://example.com/image.jpg >") == "http://example.com/image.jpg"
    assert format_image("Invalid URL") == ""
