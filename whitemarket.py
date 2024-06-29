import asyncio
import aiohttp
import logging

previous_skins = set()
current_skins = set()
lock = asyncio.Lock()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

async def getdata():
    global previous_skins
    global current_skins
    try:  
        payload = {
    "query": """
    query MarketList($search: MarketProductSearchInput, $forwardPagination: ForwardPaginationInput) {
      market_list(search: $search, forwardPagination: $forwardPagination) {
        totalCount
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          node {
            id
            price {
              value
              currency
            }
            slug
            similarQty
            storeSimilarQty
            store {
              slug
              storeName
              avatar
              isStoreNamePublic
              isTopSeller
              steamAvatar
              customAvatar
            }
            item {
              ... on CSGOInventoryItem {
                link
                paintSeed
                paintIndex
                phase
                float
                stickerTitles
              }
              isAdditionalDataMissed
              appId
              id
              description {
                steamPrice {
                  value
                  currency
                }
                description
                icon(width: 90, height: 90)
                iconLarge(width: 400, height: 300)
                name
                nameHash
                isTradeable
                ... on CSGOSteamItem {
                  isStatTrak
                  isSouvenir
                  stickerImages
                  short
                  skin
                  collection {
                    key
                    value
                  }
                  categoryEnum
                  categoryTitle
                  subcategoryEnum
                  subcategoryTitle
                  rarity {
                    value
                    key
                  }
                  exterior {
                    value
                    key
                  }
                }
              }
            }
          }
        }
      }
    }
    """,
    "variables": {
        "search": {
            "name": "",
            "sort": {
                "field": "CREATED",
                "type": "DESC"
            },
            "csgoStatTrak": None,
            "csgoSouvenir": None,
            "csgoRarityEnum": [],
            "csgoExteriorEnum": [],
            "priceFrom": {"value": "0", "currency": "USD"},
            "priceTo": {"value": "1000000", "currency": "USD"},
            "csgoStickerNames": [],
            "csgoStickerNamesOperand": "OR",
            "csgoItemSkin": None,
            "distinctValues": True,
            "csgoStickerTeam": None,
            "csgoStickerPlayer": None,
            "csgoStickerTournament": None,
            "csgoStickerFilm": None,
            "csgoStickers": None,
            "nameStrict": False,
            "csgoFloatFrom": None,
            "csgoFloatTo": None
        },
        "forwardPagination": {
            "after": None,
            "first": 75
        }
    },
    "operationName": "MarketList"
}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.white.market/graphql/api", json=payload, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    new_skins = set()
                    for obj in data["data"]["market_list"]["edges"]:
                        node = obj["node"]
                        name = str(node["item"]["description"]["nameHash"])
                        price = str(float(node["price"]["value"]))
                        link = f"https://white.market/item/{node['slug']}"
                        image = node["item"]["description"]["icon"]
                        new_skins.add((name, price, link, image, "WhiteMarket"))

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                return
            else:
                with open("textFiles/whitemarket.txt", "w", encoding="utf-8") as f:
                    for skin in updated_skins:
                        f.write(skin[0] + ";" + skin[1] + ";" + skin[2]+ ";" + skin[3] + ";" + skin[4] + "\n")
                        await asyncio.sleep(0.06)
    except Exception as e:
        logging.error("Error occurred during getting data: %s", e)


async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            logging.error("Error occurred during scraping: %s", e)
        finally:
            await asyncio.sleep(15)


asyncio.run(main())
