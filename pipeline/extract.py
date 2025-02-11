import re
import requests
from bs4 import BeautifulSoup

# Extract
def scrape_newest(url: str) -> list[dict]:
    """Fetches the links from the Steam search page and extracts game IDs."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    page_data_list = []
    for link in soup.find_all('a', href=True):
        if re.match(
                r'https://store\.steampowered\.com/app/\d+', link["href"]):
            page_data_list.append(get_data(link))

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

    # Find all <a> tags with href attributes
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
    """gets the price listed on the platform in pennies"""
    find_price = soup.find(class_="game_purchase_price")
    price = find_price.get('data-price-final')
    
    if not price:
        match = re.search(r'(Free To Play)',soup.find(class_="game_purchase_price").text)
        price = match.group(1)
    if not price:
        price = re.sub(
            r'[^0-9]', '', soup.find(class_="discount_original_price").text)
    return price

def fetch_platform_discount(soup: BeautifulSoup) -> str:
    """Gets the discounted price in percentage"""

    discount_percent = soup.find(class_="discount_pct")
    if discount_percent:
        match = re.search(r"(\d+)%", discount_percent.text)
        if match:
            return match.group(1)

def fetch_release_date(soup: BeautifulSoup) -> str:
    """Gets the release date from the soup"""
    release_date = soup.find(class_="release_date")
    match = re.search(r'(\d+ \w+, \d+)',release_date.text)
    return match.group(1)

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
    data['release_data'] = fetch_release_date(soup)
    data['game_image'] = fetch_game_image(soup)
    data['age_rating'] = fetch_age_rating(soup)
    return data

if __name__ == "__main__":
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998%2C10&supportedlang=english&ndl=1"
    api = "https://store.steampowered.com/api/appdetails?appids="

    # data = scrape_newest(url)
    data = get_data(
        "https://store.steampowered.com/app/730/CounterStrike_2/")

    print(data)