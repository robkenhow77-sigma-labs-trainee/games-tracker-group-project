# pylint: skip-file

from unittest.mock import patch, mock_open, MagicMock
import pytest

from epic_extract import (
    extract_games, get_platform_score,
    get_genre_tags, get_pegi_age_control, format_data
)


@patch("requests.post")
@patch("epic_extract.load_query")
def test_extract_games(mock_load_query, mock_post):
    """Checks the extract function gets data from the API response as expected"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {"Catalog": {"searchStore": {"elements": [{"title": "TEST GAME"}]}}}
    }
    mock_post.return_value = mock_response
    assert extract_games("https://graphql.epicgames.com/graphql")[0]['title'] == 'TEST GAME'


@patch("requests.post")
@patch("epic_extract.load_query")
def test_get_platform_score(mock_load_query, mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
	"data": {"RatingsPolls": {"getProductResult": {"averageRating": 5.0}}}
    }
    mock_post.return_value = mock_response
    assert get_platform_score("") == 5.0


@pytest.mark.parametrize(
    "tags, expected_genres, expected_other_tags",
    [
        ([{"groupName": "genre", "name": "Action"}], ["Action"], []),
        ([{"groupName": "other", "name": "Multiplayer"}], [], ["Multiplayer"]),
        ([{"groupName": "genre", "name": "RPG"}, {
         "groupName": "other", "name": "Online"}], ["RPG"], ["Online"]),
        ([], [], [])
    ]
)
def test_get_genre_tags(tags, expected_genres, expected_other_tags):
    genres, other_tags = get_genre_tags(tags)
    assert genres == expected_genres


@pytest.mark.parametrize(
    "tags, expected_genres, expected_other_tags",
    [
        ([{"groupName": "genre", "name": "Action"}], ["Action"], []),
        ([{"groupName": "other", "name": "Multiplayer"}], [], ["Multiplayer"]),
        ([{"groupName": "genre", "name": "RPG"}, {
         "groupName": "other", "name": "Online"}], ["RPG"], ["Online"]),
        ([], [], [])
    ]
)
def test_get_other_tags(tags, expected_genres, expected_other_tags):
    genres, other_tags = get_genre_tags(tags)
    assert other_tags == expected_other_tags


@pytest.mark.parametrize(
    "game_data, expected_age",
    [
        ({"catalogNs": {"ageGatings": [
         {"ratingSystem": "PEGI", "ageControl": "16+"}]}}, "16+"),
        ({"catalogNs": {"ageGatings": [
         {"ratingSystem": "ESRB", "ageControl": "Teen"}]}}, None),
        ({"catalogNs": {"ageGatings": []}}, None),
        ({}, None)
    ]
)
def test_get_pegi_age_control(game_data, expected_age):
    assert get_pegi_age_control(game_data) == expected_age


@pytest.fixture
def mock_game_data():
    return [
        {
            "title": "Mock Game",
            "catalogNs": {
                "mappings": [{"sandboxId": "mock-sandbox", "pageSlug": "PlayStreamRulez-54c31"}],
                "ageGatings": [{"ratingSystem": "PEGI", "ageControl": "12+"}]
            },
            "tags": [{"groupName": "genre", "name": "Action"}, {"groupName": "tag", "name": "TEST_MMO"}],
            "publisherDisplayName": "Mock Publisher",
            "developerDisplayName": "Mock Developer",
            "price": {"totalPrice": {"originalPrice": 59.99, "discountPercentage": 80}},
            "releaseDate": "2023-12-01",
            "keyImages": [{"url": "https://example.com/image.jpg"}]
        }
    ]


@patch("epic_extract.get_platform_score")
def test_format_data_returns_list(mock_get_platform_score, mock_game_data):
    mock_get_platform_score.return_value = '5.0'
    data = format_data(mock_game_data)
    assert isinstance(data, list)


@patch("epic_extract.get_platform_score")
def test_format_data_has_length(mock_get_platform_score, mock_game_data):
    mock_get_platform_score.return_value = '5.0'
    data = format_data(mock_game_data)
    assert len(data) > 0


@patch("epic_extract.get_platform_score")
@pytest.mark.parametrize(
    "attribute, expected_value",
    [
        ('title', 'Mock Game'),
        ('genres', ['Action']),
        ('publisher', ['Mock Publisher']),
        ('developer', ['Mock Developer']),
        ('tag', ['TEST_MMO']),
        ('genres', ['Action']),
        ('platform_score', '5.0'),
        ('platform_price', 59.99),
        ('platform_discount', 80),
        ('release_date', "2023-12-01"),
        ('game_image', "https://example.com/image.jpg"),
        ('age_rating', '12+')
    ]
)
def test_format_data_has_correct_attributes(mock_get_platform_score, mock_game_data, attribute, expected_value):
    mock_get_platform_score.return_value = '5.0'
    data = format_data(mock_game_data)
    assert data[0][attribute] == expected_value
