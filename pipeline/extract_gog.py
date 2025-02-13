"""The extraction script for GOG"""
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_soup(url: str) -> BeautifulSoup:
    """Fetches the page content using Selenium and returns a BeautifulSoup object"""

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    sleep(3)

    page_source = driver.page_source
    driver.quit()

    return BeautifulSoup(page_source, "html.parser")

def scrape_newest(url: str) -> list[dict]:
    """
    Scrapes all the newest games from GOG games
    """

    response = requests.get(url)
    soup = get_soup(url)
    game_links = [link['href'] for link in soup.find_all('a', href=True)
                  if re.match(r'https://www\.gog\.com/en/game/', link["href"])]


    page_data_list = []
    for link in game_links:
        game_data = get_data(link)
        page_data_list.append(game_data)
    return page_data_list

def fetch_title(soup: BeautifulSoup):
    """Gets the title of the page"""
    title_tag = soup.find(class_='productcard-basics__title')
    return title_tag.text.strip()

def fetch_genres(soup: BeautifulSoup):
    """Gets the genres of the page"""
    genres_div = soup.find("div", class_="details__content table__row-content")
    genres = [a.text.strip() for a in genres_div.find_all("a")]
    return genres


def fetch_publisher(soup: BeautifulSoup):
    """Extracts the publisher"""
    links = soup.find_all("a", href=True)
    publishers = [link.text.strip() for link in links if re.search(r'publisher',link.get("href", ""))]
    return publishers


def fetch_developer(soup: BeautifulSoup):
    """Extracts the developer"""
    links = soup.find_all("a", href=True)
    developers = [link.text.strip() for link in links if re.search(
        r'developer', link.get("href", ""))]
    return developers


def fetch_tags(soup: BeautifulSoup):
    """Extracts the tags"""
    tags = soup.find_all(class_='details__link details__link--tag')
    return [tag.text for tag in tags]


def fetch_platform_score(soup: BeautifulSoup):
    """Gets the review score of the game"""
    # TODO
    return None


def fetch_platform_price(soup: BeautifulSoup):
    """Gets the price of the game on the platform"""
    return soup.find(class_='product-actions-price__base-amount').text


def fetch_platform_discount(soup: BeautifulSoup):
    """Extracts the discount percentage from the product price section."""
    discounted_price = soup.find(
        "span", class_="product-actions-price__final-amount").text
    return discounted_price


def fetch_release_date(soup: BeautifulSoup):
    """Extracts the release date from the product details section."""
    release_date_span = soup.find(
        "div", class_="details__content table__row-content")
    print(release_date_span)

def fetch_game_image(soup: BeautifulSoup):
    pass


def get_data(link: str) -> dict:
    """Gets the needed data from GOG website"""
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}
    data['title'] = fetch_title(soup)
    data['genres'] = fetch_genres(soup)
    data['publisher'] = fetch_publisher(soup)
    data['developer'] = fetch_developer(soup)
    data['tag'] = fetch_tags(soup)
    data['platform_score'] = fetch_platform_score(soup)
    data['platform_price'] = fetch_platform_price(soup)
    data['platform_discount'] = fetch_platform_discount(soup)
    data['release_date'] = fetch_release_date(soup)



if __name__ == "__main__":
    # scrape_newest(
    #     'https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2025,2025')

    get_data("https://www.gog.com/en/game/primal_hearts")
