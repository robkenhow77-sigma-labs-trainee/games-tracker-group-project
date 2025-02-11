from rich.progress import Progress
import re
import requests
import argparse
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Scrape Steam search page for games released on a specific date.")
    parser.add_argument(
        '--scroll_to_date',
        type=str,
        required=False,
        help="The release date to stop scrolling at, in the format 'DD MMM, YYYY' (e.g., '10 Feb, 2025')"
    )
    return parser.parse_args()

def init_driver():
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    return driver


def scrape_newest(url: str, target_date: str) -> list[dict]:
    """Fetches the links from the Steam search page and extracts game IDs by scrolling and waiting for content to load."""
    driver = init_driver()
    driver.get(url)
    page_data_list = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Scraping Steam Games...", total=None)
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")

            for link in soup.find_all('a', href=True):
                if re.match(r'https://store\.steampowered\.com/app/\d+', link["href"]):
                    game_data = get_data(link["href"])
                    page_data_list.append(game_data)
                    print(f'Processing {game_data.get('title')} released {game_data.get('release_date')}')
                    progress.update(task, advance=1)
                    if game_data.get("release_date") == target_date:
                        driver.quit()
                        return page_data_list


        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)

def fetch_genres(soup: BeautifulSoup) -> list[str]:
    """Gets the genres out of a soup"""
    genres = []
    for link in soup.find_all('a', href=True):
        match = re.search(
            r'https://store\.steampowered\.com/genre/([^/?]+)', link["href"])
        if match:
            genres.append(match.group(1))
    return genres


def fetch_publisher(soup: BeautifulSoup) -> list:
    """Gets the publisher from the soup"""
    publishers = []

    for link in soup.find_all('a', href=True):
        match = re.search(
            r'https://store.steampowered.com/search/\?publisher=([^&]+)', link['href'])
        if match:
            if match.group(1) not in publishers:
                publishers.append(match.group(1))
    return publishers



def fetch_developer(soup: BeautifulSoup) -> list:
    """Gets the developers from the soup"""
    developers = []

    developer_div = soup.find(id="developers_list")
    if developer_div:
        for link in developer_div.find_all('a', href=True):
            match = re.search(
                r'https://store.steampowered.com/search/\?developer=([^=/?&]+)', link['href'])
            if match:
                developers.append(match.group(1))
    return developers

def fetch_tags(soup: BeautifulSoup) -> list[str]:
    """gets the tags from the soup"""
    tags_tag = soup.find(class_="glance_tags popular_tags")
    tag_links = tags_tag.find_all('a', href=True)
    pattern = r'https://store.steampowered.com/tags/en/([^/?]+)'
    return [re.search(pattern, a['href']).group(
        1) for a in tag_links if re.search(pattern, a['href'])]


def fetch_platform_score(soup: BeautifulSoup) -> str:
    """Extracts the percentage of positive reviews from the user review summary."""
    review_tag = soup.find(class_="user_reviews_summary_row")

    if review_tag:
        tooltip_text = review_tag.get("data-tooltip-html", "")
        match = re.search(r"(\d+)%", tooltip_text)
        if match:
            return match.group(1)


def fetch_platform_price(soup: BeautifulSoup) -> str:
    """Gets the price listed on the platform in pennies"""
    find_price = soup.find(class_="game_purchase_price")

    if find_price:
        price = find_price.get('data-price-final')
    else:
        price = None

    if not price:
        game_purchase_price = soup.find(class_="game_purchase_price")
        if game_purchase_price and "Free To Play" in game_purchase_price.text:
            price = "Free To Play"

    if not price:
        discount_price = soup.find(class_="discount_original_price")
        if discount_price:
            price = re.sub(r'[^0-9]', '', discount_price.text)

    return price if price else None

def fetch_platform_discount(soup: BeautifulSoup) -> str:
    """Gets the discounted price in percentage"""

    discount_percent = soup.find(class_="discount_pct")
    if discount_percent:
        match = re.search(r"(\d+)%", discount_percent.text)
        if match:
            return match.group(1) if match else None


def fetch_release_date(soup: BeautifulSoup) -> str:
    """Gets the release date from the soup"""
    release_date = soup.find(class_="release_date")
    if release_date:
        release_text = release_date.text.strip().replace("Release Date:", "").strip()
        return release_text
    return None

def fetch_game_image(soup: BeautifulSoup) -> str:
    """gets the url for the game image"""
    image = soup.find(class_="game_header_image_full").get("src")
    return image

def fetch_age_rating(soup: BeautifulSoup) -> str:
    """Gets age rating if it exists"""
    try:
        age_rating_tag = soup.find(class_="game_rating_icon").find('img')
    except:
        return None
    if age_rating_tag:
        age_rating = age_rating_tag['src']
        match = re.match(
            r'https://store.cloudflare.steamstatic.com/public/shared/images/game_ratings/PEGI/(\d+)', age_rating)
        return match.group(1)

def get_data(link: str) -> dict:
    """Scrapes page for this data.
    
    Output:
    {
        "title": x,
        "genres": [x, y, z],
        "publisher": x,
        "developer": x,
        "tag": [x,y,z],
        "platform_score": x,
        "platform_price": x,
        "platform_discount": x,
        "release_date": x,
        "game_image": x,
        "age_rating": x,
    }
    """
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    title_tag = soup.find(class_="apphub_AppName")
    data["title"] = title_tag.text.strip()

    data["genres"] = fetch_genres(soup)
    data["publisher"] = fetch_publisher(soup)
    data["developer"] = fetch_developer(soup)
    data['tag'] = fetch_tags(soup)
    data['platform_score'] = fetch_platform_score(soup)
    data['platform_price'] = fetch_platform_price(soup)
    data['platform_discount'] = fetch_platform_discount(soup)
    data['release_date'] = fetch_release_date(soup)
    data['game_image'] = fetch_game_image(soup)
    data['age_rating'] = fetch_age_rating(soup)
    return data

def steam_handler(event, context):
    args = parse_args()
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998%2C10&supportedlang=english&ndl=1"
    if args.scroll_to_date:
        try:
            scroll_to_date = datetime.strptime(
                args.scroll_to_date, "%d %b, %Y").strftime("%d %b, %Y")
        except ValueError:
            print(
                "Error: The date format should like '10 Feb, 2025'.")
            return
    else:
        scroll_to_date = (datetime.now() - timedelta(1)).strftime("%d %b, %Y")
    data = scrape_newest(url, scroll_to_date)
    return f"Completed {len(data)} entries"

steam_handler(None, None)