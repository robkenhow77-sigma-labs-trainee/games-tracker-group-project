"""Test extract file for GOG"""
# pylint: skip-file

import pytest
from bs4 import BeautifulSoup
from gog_extract import get_soup, fetch_title, fetch_genres, fetch_publisher, fetch_developer, fetch_tags, \
    fetch_platform_score, fetch_platform_price, fetch_platform_discount, fetch_release_date, fetch_game_image, \
    fetch_age_rating, get_data
from unittest.mock import MagicMock


@pytest.fixture
def false_soup():
    """Provides a BeautifulSoup object with the basic html requirement for testing."""
    html = """
    <html>
        <head><title>FAKE-SOUP</title></head>
        <body>
            <div class="productcard-basics__title">Skyrim</div>
            <div class="details__content table__row-content">
                <a href="#">Action</a>
                <a href="#">Adventure</a>
            </div>
            <a class="details__link ng-scope" href="TEST/TEST?publishers=microsoft">Microsoft</a>
            <a class="details__link ng-scope" href="TEST/TEST?developers=bethesda">Bethesda</a>
            <div class="details__link details__link--tag">wilderness</div>
            <div class="details__link details__link--tag">mod</div>
            <div class="details__link details__link--tag">monster</div>
            <span class="average-item__value">5.0</span>
            <span class="product-actions-price__base-amount">£10.00</span>
            <span class="product-actions-price__discount ng-binding" selenium-id="ProductPriceDiscount" ng-bind="'-'+cardProduct.product.price.discountPercentage+'%'">-50%</span>
            <img class="productcard-player__logo" srcset="test_image.png" />
            <div class="age-restrictions">TEST TEST PEGI Rating: 16+ TEST</div>
        </body>
    </html>
    """
    return BeautifulSoup(html, "html.parser")



def test_fetch_title(false_soup: BeautifulSoup):
    """Tests fetching the title"""
    assert fetch_title(false_soup) == "Skyrim"

def test_fetch_genres(false_soup: BeautifulSoup):
    """Tests fetching the genre"""
    assert fetch_genres(false_soup) == ['Action', 'Adventure']

def test_fetch_publisher(false_soup: BeautifulSoup):
    """Tests fetching the publisher"""
    assert fetch_publisher(false_soup) == ['Microsoft']

def test_fetch_developer(false_soup: BeautifulSoup):
    """Tests fetching the developer"""
    assert fetch_developer(false_soup) == ['Bethesda']

def test_fetch_tags(false_soup: BeautifulSoup):
    """Tests fetching the tags"""
    assert fetch_tags(false_soup) == ['wilderness', 'mod', 'monster']

def test_fetch_platform_score(false_soup: BeautifulSoup):
    """Tests fetching the platform score"""
    assert fetch_platform_score(false_soup) == '5.0'

def test_fetch_platform_price(false_soup: BeautifulSoup):
    """Tests fetching the platform price"""
    assert fetch_platform_price(false_soup) == '£10.00'

def test_fetch_platform_discount(false_soup: BeautifulSoup):
    """Tests fetching the platform discount"""
    assert fetch_platform_discount(false_soup) == '50'

def test_fetch_game_image(false_soup: BeautifulSoup):
    """Tests fetching the game image"""
    assert fetch_game_image(false_soup) == 'test_image.png'

def test_fetch_age_rating(false_soup: BeautifulSoup):
    """Tests fetching the age rating"""
    assert fetch_age_rating(false_soup) == '16'
