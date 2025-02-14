"""The extraction script for GOG"""
import re
from time import sleep
import json
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_soup(url: str) -> BeautifulSoup:
    """Fetches the page content using Selenium and returns a BeautifulSoup object"""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(url)
    sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Some resources only load when scrolling
    sleep(3)
    page_source = driver.page_source
    driver.quit()

    return BeautifulSoup(page_source, "html.parser")


def scrape_newest(url: str) -> list[dict]:
    """
    Scrapes all the newest games from GOG games
    """
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features='html.parser')
    game_links = [link['href'] for link in soup.find_all('a', href=True)
                  if re.match(r'https://www\.gog\.com/en/game/', link["href"])]


    page_data_list = []
    for link in game_links:
        game_data = get_data(link)
        page_data_list.append(game_data)
    return page_data_list


def fetch_title(soup: BeautifulSoup) -> str:
    """Gets the title of the game"""
    return soup.find(class_='productcard-basics__title').text.strip()


def fetch_genres(soup: BeautifulSoup) -> list[str]:
    """Gets the genres of the page"""
    genres_div = soup.find("div", class_="details__content table__row-content")
    genres = [a.text.strip() for a in genres_div.find_all("a")]
    return genres


def fetch_publisher(soup: BeautifulSoup) -> list[str]:
    """Extracts the publisher"""
    links = soup.find_all("a", href=True)
    publishers = [link.text.strip() for link in links if re.search(r'publisher',link.get("href", ""))]
    return publishers


def fetch_developer(soup: BeautifulSoup) -> list[str]:
    """Extracts the developer"""
    links = soup.find_all("a", href=True)
    developers = [link.text.strip() for link in links if re.search(
        r'developer', link.get("href", ""))]
    return developers


def fetch_tags(soup: BeautifulSoup) -> list[str]:
    """Extracts the tags"""
    tags = soup.find_all(class_='details__link details__link--tag')
    return [tag.text for tag in tags]


def fetch_platform_score(soup: BeautifulSoup) -> str:
    """Gets the review score of the game"""
    return soup.find(class_='average-item__value').text


def fetch_platform_price(soup: BeautifulSoup) -> str:
    """Gets the price of the game on the platform"""
    return soup.find(class_='product-actions-price__base-amount').text


def fetch_platform_discount(soup: BeautifulSoup) -> str:
    """fetches the platform discount"""
    discounted_price = soup.find(
        "span", class_="product-actions-price__discount")
    if discounted_price:
        match = re.search(r'(\d+)', discounted_price.text)
        if match:
            return match.group(1)
    return None


def fetch_release_date(soup: BeautifulSoup) -> str:
    """Extracts the release date from the product details section."""
    script_tag = soup.find("script", type="application/ld+json")
    if script_tag:
        data = json.loads(script_tag.string)
        release_date = data.get("releaseDate")
        return release_date if release_date else None


def fetch_game_image(soup: BeautifulSoup) -> str:
    """Gets the game images"""
    image = soup.find(class_='productcard-player__logo').get('srcset')
    if not image:
        logging.error("Couldn't find image")
    return image if image else None


def fetch_age_rating(soup: BeautifulSoup) -> str:
    """Gets the age rating from the age restriction class"""
    age_div = soup.find(class_='age-restrictions')

    if age_div:
        match = re.search(r'PEGI Rating:\s*(\d+)', age_div.text)
        if not match:
            logging.warning("Couldn't find age rating")
        return match.group(1) if match else None


def get_data(link: str) -> dict:
    """Gets the needed data from GOG website"""
    soup = get_soup(link)
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
    data['game_image'] = fetch_game_image(soup)
    data['age_rating'] = fetch_age_rating(soup)
    return data


if __name__ == "__main__":
    data = scrape_newest(
        'https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2025,2025')
