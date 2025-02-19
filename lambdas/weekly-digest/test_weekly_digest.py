# pylint: skip-file

from unittest.mock import MagicMock
from weekly_digest import get_weekly_top_games
import pandas as pd


def test_get_weekly_top_games():
    mock_conn = MagicMock()

    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Game 1', '2025-02-10', 'http://TEST1.com', 'Steam', 100),
        (2, 'Game 2', '2025-02-11', 'http://TEST2.com', 'GOG', 2)
    ]

    result = get_weekly_top_games(mock_conn)

    expected_result = pd.DataFrame({
        'id': [1, 2],
        'title': ['Game 1', 'Game 2'],
        'release_date': ['2025-02-10', '2025-02-11'],
        'cover_image_url': ['http://TEST1.com', 'http://TEST2.com'],
        'platform_name': ['Steam', 'GOG'],
        'platform_score': [100, 2]
    })

    assert all(result ==
               expected_result)
    

