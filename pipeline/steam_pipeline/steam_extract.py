"""Extract script by webscraping steam store page"""
import re
from os import environ as ENV
from tempfile import mkdtemp
from datetime import datetime, timedelta

import logging
import requests
from bs4 import BeautifulSoup
from rich.progress import Progress
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


def init_driver():
    """Sets up the selenium driver with proper service and options."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(options=chrome_options, service=service)

    return driver


def get_current_games(conn: psycopg.Connection):
    """Gets the current games in the database."""
    sql = "SELECT game_name FROM game;"
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def setup_logging(output: str=None, filename="game_track.log", level=logging.INFO):
    """Setup the basicConfig."""
    log_format = "{asctime} - {levelname} - {message}"
    log_datefmt = "%Y-%m-%d %H:%M"
    if output == "file":
        logging.basicConfig(
            filename=filename,
            encoding="utf-8",
            filemode="a",
            level=level,
            format=log_format,
            style="{",
            datefmt=log_datefmt
        )
        logging.info("Logging to file: %s", filename)
    else:
        logging.basicConfig(
            level=level,
            format=log_format,
            style="{",
            datefmt=log_datefmt
        )
        logging.info("Logging to console.")


def find_target_date(driver: ChromeDriverManager, target_date: str) -> None:
    """Scrolls through the page until target date is found"""
    found_target_date = False
    scroll_attempts = 0

    while not found_target_date:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        release_dates = soup.find_all(
            'div', class_='col search_released responsive_secondrow')

        for release_date in release_dates:
            if release_date.text.strip() == target_date:
                found_target_date = True
                break #is this necessary?

        if not found_target_date:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.END)
            scroll_attempts += 1

        if scroll_attempts == 100: # Change 100 to change how many max scrolls you want.
            logging.error('Date not found after %s scrolls.', scroll_attempts)
            raise ValueError(f'Date not found after {scroll_attempts} scrolls.')


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
        if not match:
            logging.error("Couldn't find review score")
        return match.group(1) if match else None


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
            price = "0"

    if not price:
        discount_price = soup.find(class_="discount_original_price")
        if discount_price:
            price = re.sub(r'[^0-9]', '', discount_price.text)
    if not price:
        logging.warning("Couldn't find price")
    return price if price else None


def fetch_platform_discount(soup: BeautifulSoup) -> str:
    """Gets the discounted price in percentage"""
    discount_percent = soup.find(class_="discount_pct")
    if discount_percent:
        match = re.search(r"(\d+)%", discount_percent.text)
        if not match:
            logging.info("Couldn't find platform discount")
        return match.group(1) if match else None


def fetch_release_date(soup: BeautifulSoup) -> str:
    """Gets the release date from the soup"""
    release_date = soup.find(class_="release_date")
    if release_date:
        release_text = release_date.text.strip().replace("Release Date:", "").strip()
        return release_text
    logging.error("Couldn't find release date")
    return None


def fetch_game_image(soup: BeautifulSoup) -> str:
    """gets the url for the game image"""
    image = soup.find(class_="game_header_image_full").get("src")
    if not image:
        logging.error("Couldn't find image")
    return image if image else None


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
        if not match:
            logging.warning("Couldn't find age rating")
        return match.group(1) if match else None


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
    data['link'] = link
    return data


def scrape_newest(url: str, target_date: str, local: bool, conn: psycopg.Connection) -> list[dict]:
    """
    Scrolls until it finds a game with the target release date, 
    then scrapes all loaded game links.
    """
    current_games = get_current_games(conn)
    current_games = [game["game_name"] for game in current_games]

    # Configure to run local or run in cloud
    if local:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
    else:
        driver = init_driver()

    driver.get(url)
    page_data_list = []

    with Progress() as progress:
        task = progress.add_task("[cyan]Processing Steam games...", total=None)

        find_target_date(driver, target_date)

        game_links = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        game_links = [link['href'] for link in soup.find_all('a', href=True)
                      if re.match(r'https://store\.steampowered\.com/app/\d+', link["href"])]

        progress.update(task, total=len(game_links))

        driver.quit()
        for link in game_links:
            game_data = get_data(link)
            if game_data.get('title') in current_games:
                break
            logging.info('Processed %s', game_data.get('title'))
            page_data_list.append(game_data)
            progress.update(task, advance=1)


    return page_data_list


if __name__ == "__main__":
    setup_logging()
    load_dotenv()
    user = ENV['DB_USERNAME']
    password = ENV["DB_PASSWORD"]
    host = ENV["DB_HOST"]
    port = ENV["DB_PORT"]
    name = ENV["DB_NAME"]
    CONN_STRING = f"""postgresql://{user}:{password}@{host}:{port}/{name}"""
    db_connection = psycopg.connect(CONN_STRING, row_factory=dict_row)

    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&supportedlang=english&ndl=1"
    targeted_date = datetime.now() - timedelta(days=2)
    targeted_date = targeted_date.strftime('%d %b, %Y')
    local = True
    scraped_data = scrape_newest(url, targeted_date, local, db_connection)
    print(scraped_data)
