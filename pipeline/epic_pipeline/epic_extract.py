"""Extracts script that pulls game data from undocumented GraphQL API"""

import requests
import logging


def load_query(filename: str) -> str:
    """Loads GraphQL query from a file."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def extract_games(url: str):
    """Queries a GraphQL API using a query from a file and returns raw game data."""
    query = load_query("query_all.gql")

    response = requests.post(url=url, json={"query": query})
    if response.status_code != 200:
        logging.error(f"Failed to fetch data: {response.status_code}")
        return []

    data = response.json()
    games = data.get("data", {}).get("Catalog", {}).get(
        "searchStore", {}).get("elements", [])

    return games


def get_platform_score(sandbox_id: str) -> str:
    """Queries the graphQL API with a games sandbox id to get rating"""
    query = load_query('get_rating.gql')

    query = query.replace("QUERY", sandbox_id)

    response = requests.post(
        url='https://graphql.epicgames.com/graphql', json={"query": query})
    if response.status_code != 200:
        logging.error(f"Failed to fetch data: {response.status_code}")
        return []

    data = response.json()
    try:
        platform_score = data.get("data", {}).get("RatingsPolls", {}).get(
            "getProductResult", {}).get("averageRating")
        return platform_score
    except:
        return None


def get_genre_tags(tags: list[str]) -> tuple[list[str], list[str]]:
    """Organizes the genres from the tags and returns them"""
    genres = []
    other_tags = []

    for tag in tags:
        if tag.get("groupName") == "genre":
            genres.append(tag.get("name"))
        else:
            other_tags.append(tag.get("name"))

    return genres, other_tags


def get_pegi_age_control(game):
    """Extracts the ageControl value where ratingSystem is 'PEGI'."""
    age_gatings = game.get("catalogNs", {}).get("ageGatings", [])

    if not isinstance(age_gatings, list):
        return None

    for age_data in age_gatings:
        if age_data.get("ratingSystem") == "PEGI":
            return age_data.get("ageControl")

    return None


def format_data(games: "json") -> list[dict]:
    """Formats raw game data into a standardized list of dictionaries."""
    game_list = []
    for game in games:
        mappings = game.get("catalogNs", {}).get("mappings")
        sandbox_id = mappings[0]["sandboxId"] if mappings else None
        genres, tags = get_genre_tags(game.get("tags", []))
        game_data = {
            "title": game.get("title"),
            "genres": genres if genres else None,
            "publisher": [game.get("publisherDisplayName")] if game.get("publisherDisplayName") else None,
            "developer": [game.get("developerDisplayName")] if game.get("developerDisplayName") else None,
            "tag": tags if tags else None,
            "platform_score": get_platform_score(sandbox_id) if sandbox_id else None,
            "platform_price": game.get("price", {}).get("totalPrice", {}).get("originalPrice"),
            "platform_discount": game.get("price", {}).get("totalPrice", {}).get("discount"),
            "release_date": game.get("releaseDate"),
            "game_image": game.get("keyImages", [{}])[0].get("url"),
            "age_rating": get_pegi_age_control(game)
        }
        print(game_data.get('age_rating'))
        game_list.append(game_data)

    return game_list


if __name__ == "__main__":
    raw_games = extract_games(
        "https://graphql.epicgames.com/graphql")
    games = format_data(raw_games)

    for game in games:
        print(game)

    print(len(games))
