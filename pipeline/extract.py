import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998%2C10&supportedlang=english&ndl=1"
API_URL = "https://store.steampowered.com/api/appdetails?appids="


def get_ids() -> list[str]:
    """Fetches the links from the Steam search page and extracts game IDs."""
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(
            f"Failed to fetch {BASE_URL}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    game_ids = []

    for link in soup.find_all('a', href=True):
        match = re.match(
            r'https://store\.steampowered\.com/app/(\d+)', link['href'])
        if match:
            game_id = match.group(1)
            game_ids.append(game_id)

    return game_ids


def fetch_game_details(game_ids: list[str]) -> list:
    """Fetch game details for each ID from the Steam API."""
    names = []

    for game_id in game_ids:
        url = API_URL + game_id
        response = requests.get(url)
        data = response.json()
        game = data.get(game_id)
        game_data = game.get("data")
        names.append(game_data.get("name"))
    return names


if __name__ == "__main__":
    ids = get_ids()
    game_details = fetch_game_details(ids)
    print(game_details)
