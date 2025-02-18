# pylint: skip-file
from unittest.mock import MagicMock, patch
import psycopg
import steam_load_functions as lf
import pytest

# Get IDs

# Make ID mapping
data = [
    ("genre", [{"genre_name": "solo", "genre_id": 1}], {"solo": 1}),
    ("tag", [{"tag_id": 1, "tag_name": "rpg"}], {"rpg": 1}),
    ("genre", [], {}),
    ("genre", [{"genre_name": "solo", "genre_id": 1},
               {"genre_name": "wilderness", "genre_id": 2},
               {"genre_name": "adventure", "genre_id": 3}],
               {"solo": 1, "wilderness": 2, "adventure": 3})
    ]

@pytest.mark.parametrize("item, input, expected", data)
def test_make_id_mapping(item, input, expected):
    assert lf.make_id_mapping(input, item) == expected




# Upload and return devs

def test_upload_and_return_devs():
    input_data = [("Treyarch,")]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_and_return_devs(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded developers")


def test_upload_and_return_devs_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_devs(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new developers to upload") 


def test_upload_and_return_devs_upload_error():
    input = [("Dev1",), ("Dev2",)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_and_return_devs(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading developers failed: DB Error. Data to be uploaded: [('Dev1',), ('Dev2',)]")


# Upload and return games

def test_upload_and_return_games():
    input_data = [("Rocket league,")]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_and_return_games(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded games")


def test_upload_and_return_games_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_games(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new games to upload") 


def test_upload_and_return_games_upload_error():
    input = [("Game1",), ("Game2",)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_and_return_games(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading games failed: DB Error. Data to be uploaded: [('Game1',), ('Game2',)]")


# Upload and return genres

def test_upload_and_return_genres():
    input_data = [("Fantasy,")]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_and_return_genres(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded genres")


def test_upload_and_return_genres_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_genres(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new genres to upload") 


def test_upload_and_return_genres_upload_error():
    input = [("Genre1",), ("Genre2",)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_and_return_genres(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading genres failed: DB Error. Data to be uploaded: [('Genre1',), ('Genre2',)]")


# Upload and return publishers

def test_upload_and_return_publishers():
    input_data = [("ubisoft,")]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_and_return_pubs(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded publishers")


def test_upload_and_return_publishers_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_pubs(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new publishers to upload") 


def test_upload_and_return_publishers_upload_error():
    input = [("Pub1",), ("Pub2",)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_and_return_pubs(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading publishers failed: DB Error. Data to be uploaded: [('Pub1',), ('Pub2',)]")


# Upload and return tags

def test_upload_and_return_tags():
    input_data = [("ubisoft,")]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_and_return_tags(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded tags")


def test_upload_and_return_tags_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_tags(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new tags to upload") 


def test_upload_and_return_tags_upload_error():
    input = [("Pub1",), ("Pub2",)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_and_return_tags(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading tags failed: DB Error. Data to be uploaded: [('Pub1',), ('Pub2',)]")

