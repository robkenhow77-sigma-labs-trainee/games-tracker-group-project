# pylint: skip-file
from unittest.mock import MagicMock, patch
from datetime import datetime

import psycopg
import epic_load_functions as lf
import pytest

NEW_GAMES_EXAMPLE = [{
        "game_name": "BO3",
        "developer": ["treyarch", 'epic', 'some other dev', "someone"],
        "tag": ["action"],
        "genre": ["mystic"],
        "publisher": ["sigma", "activision"],
        "release_date": datetime.date(datetime.now()),
        "game_image": "random",
        "is_nsfw": True,
        "age_rating": "PEGI 16",
        "platform": "Steam",
        "score": 90,
        "price": 20000,
        "discount": 99,
        "platform_url": "game_platform_url"
        },
        {
        "game_name": "rocket league",
        "developer": ["EA"],
        "tag": ["action", "racing"],
        "genre": ["mystic", "horror"],
        "publisher": ["sigma"],
        "release_date": datetime.date(datetime.now()),
        "game_image": "random",
        "is_nsfw": True,
        "age_rating": "PEGI 18",
        "platform": "GOG",
        "score": 10,
        "price": 20,
        "discount": 0,
        "platform_url": "game_platform_url"
        }]

GAME_ID_MAPPING = {"BO3": 1, "rocket league": 2}

PLATFORM_MAPPING = {"Steam":1, "GOG": 2, "Epic Games Store": 3}

AGE_RATING_MAPPING =  {"PEGI 3": 1,
             "PEGI 7": 2,
             "PEGI 12": 3,
             "PEGI 16": 4,
             "PEGI 18": 5,
             "Not Assigned": 6
             }

DEVELOPER_MAPPING = {"treyarch": 1, "epic": 2, "some other dev": 3, "someone": 4, "EA": 5}

PUBLISHER_MAPPING = {"sigma": 1, "activision": 2}

GAME_PLATFORM_ASSIGNMENT_MAPPING = {"(1, 1)": 1, "(2, 2)": 2}

GENRE_MAPPING = {"mystic": 1, "horror": 2}

TAG_MAPPING = {"action": 1, "racing": 2}

GAME_PLATFORM_ASSIGNMENT_MAPPING = {"(1, 1)": 1, "(2, 2)": 2}

# DELETE RANDO.PY

# Get IDs !!!!!

# Make ID mapping
DATA= [
    ("genre", [{"genre_name": "solo", "genre_id": 1}], {"solo": 1}),
    ("tag", [{"tag_id": 1, "tag_name": "rpg"}], {"rpg": 1}),
    ("genre", [], {}),
    ("genre", [{"genre_name": "solo", "genre_id": 1},
               {"genre_name": "wilderness", "genre_id": 2},
               {"genre_name": "adventure", "genre_id": 3}],
               {"solo": 1, "wilderness": 2, "adventure": 3})
    ]
@pytest.mark.parametrize("item, input, expected", DATA)
def test_make_id_mapping(item, input, expected):
    assert lf.make_id_mapping(input, item) == expected


# Get games for upload

DATA= [
    (NEW_GAMES_EXAMPLE,
     {"cod": 1},
     NEW_GAMES_EXAMPLE),
    (NEW_GAMES_EXAMPLE,
     {"BO3": 2},
     [NEW_GAMES_EXAMPLE[1]]),
    ([], {}, []),
    (NEW_GAMES_EXAMPLE,
     {},
     NEW_GAMES_EXAMPLE),
    (NEW_GAMES_EXAMPLE,
     {"BO3":1, "rocket league": 2}, [])
    ]
@pytest.mark.parametrize("new, current, expected", DATA)
def test_get_games_for_upload(new, current, expected):
    assert lf.get_games_for_upload(new, current) == expected


# Get items for upload
DATA= [
    ('tag', NEW_GAMES_EXAMPLE, {"solo":1}, [('racing',), ('action',)]),
    ('genre', NEW_GAMES_EXAMPLE, {"mystic":1, "horror": 2}, []),
    ('publisher', NEW_GAMES_EXAMPLE, {"activision":1,}, [('sigma',)]),
    ('developer', [], {}, [])
    ]
@pytest.mark.parametrize("table, new, current, expected", DATA)
def test_get_items_for_upload(table, new, current, expected):
    items = lf.get_items_for_upload(table, new, current)
    for item in items:
        assert item in expected


# Format games for upload

def test_format_games_for_upload():
    A = NEW_GAMES_EXAMPLE[0].copy()
    A["age_rating"] = 4
    B = NEW_GAMES_EXAMPLE[1].copy()
    B["age_rating"] = 5
    expected = [A, B]
    expected = [(
        game["game_name"],
        game["game_image"],
        game["age_rating"],
        game["is_nsfw"]) 
        for game in expected]
    assert lf.format_games_for_upload(NEW_GAMES_EXAMPLE, AGE_RATING_MAPPING) == expected


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


# make_current_dev_or_pub_game_assignment_tuples

def test_make_current_dev_or_pub_game_assignment_tuples():
    current_dev_assignments = [{"assignment_id": 1, "game_id": 1, "developer_id":2}]
    expected_dev_tuples = [(1,2)]

    current_pub_assignments = [{"assignment_id": 1, "game_id": 1, "publisher_id":2}]
    expected_pub_tuples = [(1,2)]
    assert lf.make_current_dev_or_pub_game_assignment_tuples(current_dev_assignments, 'developer_id') == expected_dev_tuples
    assert lf.make_current_dev_or_pub_game_assignment_tuples(current_pub_assignments, 'publisher_id') == expected_pub_tuples

    # DB query returns empty list if there is nothing in the table
    no_assignments = []
    expected = []
    assert lf.make_current_dev_or_pub_game_assignment_tuples(no_assignments, 'publisher_id') == expected


# Assign developers
DATA = [
    ([(1,1), (1,2)], [(1,3), (1,4), (2,5)]),
    ([], [(1,1), (1,2), (1,3), (1,4), (2,5)]),
    ([(1,1), (1,2), (1,3), (1,4), (2,5)], [])
    ]
@pytest.mark.parametrize("current, expected", DATA)
def test_assign_developers(current, expected):
    assert lf.assign_developers(NEW_GAMES_EXAMPLE, GAME_ID_MAPPING, DEVELOPER_MAPPING, current) == expected


# Assign publishers
DATA = [
    ([(1,1), (1,2)], [(2,1)]),
    ([], [(1,1), (1,2), (2,1)]),
    ([(1,1), (1,2), (2,1)], [])
    ]
@pytest.mark.parametrize("current, expected", DATA)
def test_assign_publishers(current, expected):
    assert lf.assign_publishers(NEW_GAMES_EXAMPLE, GAME_ID_MAPPING, PUBLISHER_MAPPING, current) == expected


# Upload developer_game assignments
def test_upload_developer_game_assignment():
    input_data = [(1,1), (1,2)]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_developer_game_assignment(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded developer_game_assignments")


def test_upload_developer_game_assignment_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_developer_game_assignment(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new developer_game_assignments to upload") 


def test_test_upload_developer_game_assignment_upload_error():
    input = [(1,1), (1,2)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_developer_game_assignment(input, mock_conn) == expected_output
        mock_error.assert_any_call('Uploading developer_game_assignments failed: DB Error. Data to be uploaded: [(1, 1), (1, 2)]')

# Upload publisher_game assignments
def test_upload_publisher_game_assignment():
    input_data = [(1,1), (1,2)]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_publisher_game_assignment(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded publisher_game_assignments")


def test_upload_publisher_game_assignment_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_publisher_game_assignment(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new publisher_game_assignments to upload") 


def test_test_upload_publisher_game_assignment_upload_error():
    input = [(1,1), (1,2)]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_publisher_game_assignment(input, mock_conn) == expected_output
        mock_error.assert_any_call('Uploading publisher_game_assignments failed: DB Error. Data to be uploaded: [(1, 1), (1, 2)]')


# Game platform assignments

def test_make_current_game_platform_assignment_tuples():
    current_assignments = [
    {"platform_assignment_id": 1, "game_id": 1, "platform_id": 1},
    {"platform_assignment_id": 2, "game_id": 1, "platform_id": 2},
    {"platform_assignment_id": 3, "game_id": 2, "platform_id": 3},
    {"platform_assignment_id": 4, "game_id": 3, "platform_id": 2},
    {"platform_assignment_id": 5, "game_id": 3, "platform_id": 3}
    ]
    expected_assignments = [(1, 1), (1, 2), (2, 3), (3, 2), (3, 3)]
    assert lf.make_current_game_platform_assignment_tuples(current_assignments) == expected_assignments
    assert lf.make_current_game_platform_assignment_tuples([]) == []


# Assign game platform
DATA = [
    ([(1,1)], [(2, 2, 10, 20, 0, datetime.date(datetime.now()), "game_platform_url")]),
    ([(2,2)], [(1, 1, 90, 20000, 99, datetime.date(datetime.now()), "game_platform_url")])
    ]
@pytest.mark.parametrize("current, expected", DATA)
def test_assign_game_platform(current, expected):
    assert lf.assign_game_platform(NEW_GAMES_EXAMPLE, GAME_ID_MAPPING, PLATFORM_MAPPING, current) == expected


# Upload and return game_platform_assignments
def test_upload_and_return_game_platform_assignments():
    input_data = [(2, 2, 10, 20, 0, datetime.date(datetime.now()))]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_and_return_game_platform_assignment(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded game_platform_assignments")


def test_upload_and_return_game_platform_assignments_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_game_platform_assignment(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new game_platform_assignments to upload") 


def test_upload_and_return_game_platform_assignments_upload_error():
    input_data = [(2, 2, 10, 20, 0, "date")]
    expected_output = {}
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_and_return_game_platform_assignment(input_data, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading game_platform_assignments failed: DB Error. Data to be uploaded: [(2, 2, 10, 20, 0, 'date')]")


# Assign genre game_platform

def test_assign_genre_game_platform():
    current_assignments = [(1, 1), (1,2)]
    assert lf.assign_genre_game_platform(NEW_GAMES_EXAMPLE, GAME_ID_MAPPING, PLATFORM_MAPPING, GENRE_MAPPING, GAME_PLATFORM_ASSIGNMENT_MAPPING, current_assignments) == [(2, 2)]


# Assign tag game_platform

def test_assign_genre_game_platform():
    current_assignments = [(1, 1), (2,2)]
    assert lf.assign_tag_game_platform(NEW_GAMES_EXAMPLE, GAME_ID_MAPPING, PLATFORM_MAPPING, TAG_MAPPING, GAME_PLATFORM_ASSIGNMENT_MAPPING,current_assignments) == [(1, 2)]


# Upload genre_game_platform_assignment

def test_upload_genre_game_platform_assignment():
    input_data = [(1, 2)]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_genre_game_platform_assignment(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded genre_game_platform_assignments")


def test_upload_genre_game_platform_assignment_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_genre_game_platform_assignment(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new genre_game_platform_assignments to upload") 


def test_upload_genre_game_platform_assignment_upload_error():
    input = [(1,2), (2,1)]
    expected_output = None
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_genre_game_platform_assignment(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading genre_game_platform_assignments failed: DB Error. Data to be uploaded: [(1, 2), (2, 1)]")


# Upload genre_game_platform_assignment

def test_upload_tag_game_platform_assignment():
    input_data = [(1, 2)]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.nextset.return_value = False

    with patch('logging.info') as mock_info:
        result = lf.upload_tag_game_platform_assignment(input_data, mock_conn)
        mock_info.assert_any_call("Successfully loaded tag_game_platform_assignments")


def test_upload_tag_game_platform_assignment_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_tag_game_platform_assignment(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new tag_game_platform_assignments to upload") 


def test_upload_tag_game_platform_assignment_upload_error():
    input = [(1,2), (2,1)]
    expected_output = None
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
   
    mock_cursor.executemany.side_effect = psycopg.Error("DB Error")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('logging.error') as mock_error:
        assert lf.upload_tag_game_platform_assignment(input, mock_conn) == expected_output
        mock_error.assert_any_call("Uploading tag_game_platform_assignments failed: DB Error. Data to be uploaded: [(1, 2), (2, 1)]")

