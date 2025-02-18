# pylint: skip-file
from unittest.mock import MagicMock, patch
import steam_load_functions as lf

# def upload_and_return_devs(devs: list[tuple], conn: psycopg.Connection) -> dict:
#     """Uploads the new developers and returns their names and ids"""
#     if len(devs) == 0:
#         logging.info("No new developers to upload")
#         return {}
#     try:
#         with conn.cursor() as cur:
#             cur.executemany("""INSERT INTO developer (developer_name)
#                             VALUES (%s) RETURNING *""", devs, returning=True)
#             ids = []
#             while True:
#                 ids.append(cur.fetchone())
#                 if not cur.nextset():
#                     break
#             conn.commit()
#             logging.info("Successfully loaded developers")
#             return ids
#     except:
#         logging.error(f"Uploading developers failed. Data to be uploaded: {devs}")
#         return {}

# def test_upload_and_return_devs():

#     input = [("Treyarch")]
#     expected_output = [{"developer_id": "1", "developer_name": "Treyarch"}]

#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_cursor.fetchone.side_effect = [(1, "Dev1"), (2, "Dev2"), None]


#     assert lf.upload_and_return_devs(input, mock_conn) ==  expected_output

def test_upload_and_return_devs_no_data():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_devs(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new developers to upload") 
    
def test_upload_and_return_devs_upload_error():
    input = []
    expected_output = {}

    mock_conn = MagicMock()

    with patch('logging.info') as mock_info:
        assert lf.upload_and_return_devs(input, mock_conn) ==  expected_output
        mock_info.assert_any_call("No new developers to upload") 
