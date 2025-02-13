"""Test extract for steam"""
# pylint: skip-file

import unittest
import pytest
from unittest.mock import patch, MagicMock
from extract_steam import find_target_date, setup_logging, parse_args, init_driver, fetch_age_rating, fetch_developer, fetch_game_image, fetch_platform_discount, fetch_genres, fetch_platform_price, fetch_platform_score, fetch_publisher, fetch_release_date, fetch_tags
from bs4 import BeautifulSoup

class TestParseArgs(unittest.TestCase):
    
    @patch('sys.argv', ['script_name'])  # Test no arguments
    def test_default_values(self):
        args = parse_args()
        self.assertEqual(args.scroll_to_date, None)
        self.assertEqual(args.log_output, 'console')

    @patch('sys.argv', ['script_name', '--log_output', 'file'])
    def test_log_output_file(self):
        args = parse_args()
        self.assertEqual(args.log_output, 'file')

    @patch('sys.argv', ['script_name', '--log_output', 'console'])
    def test_log_output_console(self):
        args = parse_args()
        self.assertEqual(args.log_output, 'console')

    @patch('sys.argv', ['script_name', '--scroll_to_date', '10 Feb, 2025'])
    def test_scroll_to_date(self):
        args = parse_args()
        self.assertEqual(args.scroll_to_date, '10 Feb, 2025')

    @patch('sys.argv', ['script_name', '--log_output', 'invalid_option'])
    def test_invalid_log_output(self):
        with self.assertRaises(SystemExit):  # argparse will exit on invalid argument
            parse_args()

    @patch('sys.argv', ['script_name', '--scroll_to_date', '10 Feb, 2025', '--log_output', 'file'])
    def test_both_arguments(self):
        args = parse_args()
        self.assertEqual(args.scroll_to_date, '10 Feb, 2025')
        self.assertEqual(args.log_output, 'file')


class TestInitDriver(unittest.TestCase):

    @patch('extract_steam.webdriver.Chrome')  # Mock webdriver.Chrome
    @patch('extract_steam.ChromeDriverManager')  # Mock ChromeDriverManager
    @patch('extract_steam.Service')  # Mock Service
    @patch('extract_steam.webdriver.ChromeOptions')  # Mock ChromeOptions
    def test_driver_init(self, MockChromeOptions, MockService, MockChromeDriverManager, MockChrome):
        """Tests the driver initialises with correct options."""

        mock_manager = MagicMock()
        MockChromeDriverManager.return_value = mock_manager
        mock_manager.install.return_value = '/not/real/path'

        mock_service = MagicMock()
        MockService.return_value = mock_service

        mock_options = MagicMock()
        MockChromeOptions.return_value = mock_options

        mock_driver = MagicMock()
        MockChrome.return_value = mock_driver

        driver = init_driver()

        MockChromeDriverManager.assert_called_once()

        MockChrome.assert_called_once_with(service=mock_service, options=mock_options)

        self.assertEqual(driver, mock_driver)

    @patch('extract_steam.webdriver.Chrome')  # Mock webdriver.Chrome
    @patch('extract_steam.ChromeDriverManager')  # Mock ChromeDriverManager
    @patch('extract_steam.webdriver.chrome.service.Service')  # Mock Service
    @patch('extract_steam.webdriver.ChromeOptions')  # Mock ChromeOptions
    def test_headless_option(self, MockChromeOptions, MockService, MockChromeDriverManager, MockChrome):
        """tests drive initialises with headless."""

        mock_manager = MagicMock()
        MockChromeDriverManager.return_value = mock_manager
        mock_manager.install.return_value = '/not/real/path'

        mock_service = MagicMock()
        MockService.return_value = mock_service

        mock_options = MagicMock()
        MockChromeOptions.return_value = mock_options

        mock_driver = MagicMock()
        MockChrome.return_value = mock_driver

        init_driver()

        mock_options.add_argument.assert_called_with('--headless')


class TestSetupLogging(unittest.TestCase):

    @patch('logging.basicConfig')
    @patch('logging.info')
    def test_setup_logging_to_file(self, mock_info, mock_basic_config):

        output = "file"
        filename = "custom_log.log"
        level = 30  # ERROR level

        setup_logging(output, filename, level)

        mock_basic_config.assert_called_once_with(
            filename=filename,
            encoding="utf-8",
            filemode="a",
            level=level,
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )
        
        mock_info.assert_called_once_with("Logging to file: %s", filename)

    @patch('logging.basicConfig')
    @patch('logging.info')
    def test_setup_logging_to_console(self, mock_info, mock_basic_config):
        output = "console"
        filename = "game_track.log"
        level = 20  # INFO level

        setup_logging(output, filename, level)

        mock_basic_config.assert_called_once_with(
            level=level,
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )
        
        mock_info.assert_called_once_with("Logging to console.")

    @patch('logging.basicConfig')
    @patch('logging.info')
    def test_default_logging(self, mock_info, mock_basic_config):
        output = "console"
        level = 20  # INFO level

        # Call the setup_logging function
        setup_logging(output)

        # Check that logging.basicConfig was called with the expected arguments
        mock_basic_config.assert_called_once_with(
            level=level,
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )
        
        # Verify that logging.info was called with the correct message
        mock_info.assert_called_once_with("Logging to console.")

    @patch('logging.basicConfig')
    @patch('logging.info')
    def test_logging_with_different_level(self, mock_info, mock_basic_config):
        # Test setup_logging with a custom logging level (DEBUG)
        output = "file"
        filename = "test.log"
        level = 10  # DEBUG level

        # Call the setup_logging function
        setup_logging(output, filename, level)

        mock_basic_config.assert_called_once_with(
            filename=filename,
            encoding="utf-8",
            filemode="a",
            level=level,
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )

        mock_info.assert_called_once_with("Logging to file: %s", filename)


class TestFindTargetDate(unittest.TestCase):

    @patch('extract_steam.ChromeDriverManager')
    @patch('extract_steam.BeautifulSoup')
    def test_target_date_found(self, mock_bs, MockDriver):

        mock_driver = MockDriver.return_value
        mock_driver.page_source = "<html><div class='col search_released responsive_secondrow'>2025-02-14</div></html>"

        target_date = "2025-02-13"

        mock_soup = MagicMock()
        mock_soup.find_all.return_value = [MagicMock(text="2025-02-13")]
        mock_bs.return_value = mock_soup

        find_target_date(mock_driver, target_date)

        mock_driver.find_element.assert_not_called()  # No need to scroll
        mock_driver.page_source = "<html><div class='col search_released responsive_secondrow'></div></html>"

    @patch('extract_steam.ChromeDriverManager')
    @patch('extract_steam.BeautifulSoup')
    def test_target_date_found_after_one_scroll(self, mock_bs, MockDriver):

        mock_driver = MockDriver.return_value
        mock_driver.page_source = "<html><div class='col search_released responsive_secondrow'></div></html>"

        target_date = "2025-02-13"

        mock_soup = MagicMock()
        mock_soup.find_all.return_value = [MagicMock(text="2025-02-14")]
        mock_bs.return_value = mock_soup

        # Find after one scroll.
        mock_soup.find_all.return_value = [MagicMock(text="2025-02-13")]

        # Mock scrolling
        mock_driver.find_element.return_value.send_keys = MagicMock()

        find_target_date(mock_driver, target_date)

        mock_driver.find_element.assert_not_called()


    @patch('extract_steam.ChromeDriverManager')
    @patch('extract_steam.BeautifulSoup')
    @patch('extract_steam.logging.error')
    def test_target_date_not_found_after_100_scrolls(self, mock_log_error, mock_bs, MockDriver):

        mock_driver = MockDriver.return_value
        mock_driver.page_source = "<html><div class='col search_released responsive_secondrow'></div></html>"

        target_date = "2025-02-13"

        mock_soup = MagicMock()
        mock_soup.find_all.return_value = [MagicMock(text="2025-02-14")]
        mock_bs.return_value = mock_soup

        mock_driver.find_element.return_value.send_keys = MagicMock()

        with self.assertRaises(ValueError):
            find_target_date(mock_driver, target_date)

        mock_log_error.assert_called_once_with('Date not found after %s scrolls.', 100)

        self.assertEqual(mock_driver.find_element.call_count, 100)


@pytest.fixture
def tag_page_response():
    """html response that has the tags as expected by fetch tag function"""
    return """            
    <a href="https://store.steampowered.com/tags/en/eye"></a>
    <a href="https://store.steampowered.com/tags/en/gift"></a>
    <a href="https://store.steampowered.com/tags/en/cyclopse"></a>"""


def test_fetch_tags(tag_page_response: str):
    """Test fetch tags gets the tags correctly"""
    mock_soup = MagicMock()
    mock_soup.find.return_value = BeautifulSoup(
        tag_page_response, "html.parser")
    assert fetch_tags(mock_soup) == ['eye', 'gift', 'cyclopse']


@pytest.fixture
def genre_page_response():
    """page response of genres"""
    return """
    <a href="https://store.steampowered.com/genre/action"></a>
"""

def test_fetch_genre(genre_page_response: str):
    """tests the fetch genres function gets the genre from the page response."""
    soup = BeautifulSoup(
        genre_page_response, "html.parser"
    )
    assert fetch_genres(soup) == ['action']

@pytest.fixture
def publisher_page_response():
    """Page response for publishers"""
    return """
    <a href="https://store.steampowered.com/search/?publisher=bethesda"></a>
"""


def test_fetch_publisher(publisher_page_response):
    """Tests the fetch publisher function gets the publisher from a html"""
    soup = BeautifulSoup(
        publisher_page_response, "html.parser")
    assert fetch_publisher(soup) == ['bethesda']


@pytest.fixture
def developer_page_response():
    """Page response for list of developers"""
    return """
    <div id="developers_list">
        <a href="https://store.steampowered.com/search/?developer=bethesda"></a>
    </div>
    """


def test_fetch_developer(developer_page_response):
    """Tests the fetch developer function to get the dev."""
    # Use real BeautifulSoup object
    soup = BeautifulSoup(developer_page_response, "html.parser")
    assert fetch_developer(soup) == ['bethesda']

@pytest.fixture
def platform_score_page_response():
    """Page response for platform score"""
    return """
    <div class="user_reviews_summary_row" data-tooltip-html="TEST TEST 69% TEST TEST.">
"""

def test_fetch_plaform_score(platform_score_page_response):
    """Tests the fetch platform score function actually extracts the score from the html"""
    soup = BeautifulSoup(platform_score_page_response, "html.parser")
    assert fetch_platform_score(soup) == '69'

@pytest.fixture
def platform_price_page_response():
    """Page response for platform price"""
    return """
    <div class="game_purchase_price" data-price-final="1000">
"""

def test_fetch_platform_price(platform_price_page_response):
    """Tests the fetch platform price function extracts the value from the html"""
    soup = BeautifulSoup(platform_price_page_response, "html.parser")
    assert fetch_platform_price(soup) == '1000'

@pytest.fixture
def platform_price_discount_page_response():
    """Page response for page discount"""
    return """
    <div class="discount_pct">50%</div>
"""

def test_fetch_platform_discount(platform_price_discount_page_response):
    """Tests the fetch platform discount"""
    soup = BeautifulSoup(platform_price_discount_page_response, "html.parser")
    assert fetch_platform_discount(soup) == '50'

@pytest.fixture
def release_date_page_response():
    """Release date page response"""
    return """
    <div class="release_date">TEST</div>    
"""
def test_fetch_release_date(release_date_page_response):
    soup = BeautifulSoup(release_date_page_response, "html.parser")
    assert fetch_release_date(soup) == 'TEST'

@pytest.fixture
def age_rating_page_response():
    return """
    <div class="game_rating_icon">
        <a href="TEST">
            <img src="https://store.cloudflare.steamstatic.com/public/shared/images/game_ratings/PEGI/69">
        </a>
    </div>
"""

def test_fetch_rating(age_rating_page_response):
    soup = BeautifulSoup(age_rating_page_response, "html.parser")
    assert fetch_age_rating(soup)
