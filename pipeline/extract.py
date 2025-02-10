import re
import requests
from bs4 import BeautifulSoup

# Extract
def get_ids(url: str) -> list[str]:
    """Fetches the links from the Steam search page and extracts game IDs."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
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


def fetch_game_details(api: str, game_ids: list[str]) -> list:
    """Fetch game details for each ID from the Steam API."""
    game_data = []

    for game_id in game_ids:
        url = api + game_id
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            game_data.append(data.get(game_id))
    return game_data


if __name__ == "__main__":
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998%2C10&supportedlang=english&ndl=1"
    api = "https://store.steampowered.com/api/appdetails?appids="

    ids = get_ids(url)
    game_details = fetch_game_details(api, ids)
    print(game_details[0]["data"]["name"])
       