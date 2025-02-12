import requests


def get_response(url):
    """Queries the GraphQL API"""
    q = """{
  Catalog {
    searchStore(
      allowCountries: "GB"
      category: "games/edition/base"
      comingSoon: false
      count: 50
      country: "GB"
      locale: "en-US"
      sortBy: "releaseDate"
      sortDir: "DESC"
    ) {
      elements {
        id
        title
        description
        currentPrice
        releaseDate
        developerDisplayName
        publisherDisplayName
				

        seller {
          id
          name
        }

        keyImages {
          type
          url
					alt
        }

        items {
          id
          namespace
        }

        tags {
          id
          name
					groupName
        }
				
				price(country: "GB") {
					totalPrice {
						discountPrice
						originalPrice
						voucherDiscount
						discount
						currencyCode
						currencyInfo {
							decimals
						}
						fmtPrice {
							originalPrice
							discountPrice
							intermediatePrice
						}
					}
				}
      }
    }
	}
}
"""

    response = requests.post(url=url, json={"query": q})
    print("Response status code:", response.status_code)

    if response.status_code == 200:
        return response.json()

    return None


if __name__ == "__main__":
    data = get_response("https://graphql.epicgames.com/graphql")

    if data:
        games = data["data"]["Catalog"]["searchStore"]["elements"]
        for game in games:
            print(f"Title: {game['title']}")
            print(f"Price: {game['currentPrice']}")
            print(f"Release Date: {game['releaseDate']}")
            print(f"Developer: {game['developerDisplayName']}")
            print(f"Publisher: {game['publisherDisplayName']}")
            print(f"Seller: {game['seller']['name']}")

            print("\nImages:")
            for image in game["keyImages"]:
                print(f"  - {image['type']}: {image['url']} ({image['alt']})\n")

            print("\nTags:")
            for tag in game["tags"]:
                print(
                    f"  - {tag['name']} ({tag.get('groupName', 'No group')})")

            print("\n" + "----------------------------------------" + "\n")
