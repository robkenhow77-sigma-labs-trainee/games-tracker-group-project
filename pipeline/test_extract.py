import unittest
import pytest
from unittest.mock import patch, MagicMock
from extract import get_ids, fetch_game_details


@pytest.fixture
def api_response():
    return """
    <html>
        <body>
            <a href="https://store.steampowered.com/app/1/game_one"></a>
            <a href="https://store.steampowered.com/app/2/game_two"></a>
        </body>
    </html>
    """


@patch("requests.get")
def test_get_ids(mock_get, api_response):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = api_response

    mock_get.return_value = mock_response

    url = "https://store.steampowered.com/search"
    game_ids = get_ids(url)

    assert game_ids == ["1", "2"]

def test_fetch_game_details():
    api = "https://store.steampowered.com/api/appdetails?appids="
    ids = ["1", "2"]
    fetch_game_details(api, ids)


