import requests


def extract_games(url: str):
    """Queries a graphQL API """
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
}"""

    response = requests.post(url=url, json={"query": q})
    print("Response status code:", response.status_code)

    if response.status_code == 200:
        return response.json()

    return None


if __name__ == "__main__":
    
    data = extract_games("https://graphql.epicgames.com/graphql")
    
    ## How to extract elements from data!
    if data:
        games = data["data"]["Catalog"]["searchStore"]["elements"]
        for game in games:
            print(f"Title: {game['title']}")
            print(f"Release Date: {game['releaseDate']}")
            print(f"Developer: {game['developerDisplayName']}")
            print(f"Publisher: {game['publisherDisplayName']}")
            print(f"Seller: {game['seller']['name']}")
            print(f'Current Price: {game['currentPrice']}')

            print("\nPrice Details:")
            price_info = game.get("price", {}).get("totalPrice", {})
            print(
                f"  - Original Price: {price_info.get('originalPrice', 'N/A')}")
            print(
                f"  - Discount Price: {price_info.get('discountPrice', 'N/A')}")
            print(
                f"  - Voucher Discount: {price_info.get('voucherDiscount', 'N/A')}")
            print(f"  - Discount: {price_info.get('discount', 'N/A')}")
            print(
                f"  - Currency Code: {price_info.get('currencyCode', 'N/A')}")

            currency_info = price_info.get("currencyInfo", {})
            print(
                f"  - Currency Decimals: {currency_info.get('decimals', 'N/A')}")

            fmt_price = price_info.get("fmtPrice")
            if fmt_price:
                print(
                    f"  - Formatted Original Price: {fmt_price.get('originalPrice', 'N/A')}")
                print(
                    f"  - Formatted Discount Price: {fmt_price.get('discountPrice', 'N/A')}")
                print(
                    f"  - Formatted Intermediate Price: {fmt_price.get('intermediatePrice', 'N/A')}")
            else:
                print("  - Formatted price details not available")

            print("\nImages:")
            for image in game["keyImages"]:
                print(
                    f"  - {image['type']}: {image['url']} ({image['alt']})\n")

            print("\nTags:")
            for tag in game["tags"]:
                print(
                    f"  - {tag['name']} ({tag.get('groupName', 'No group')})")

            print("\n" + "-" * 40 + "\n")
