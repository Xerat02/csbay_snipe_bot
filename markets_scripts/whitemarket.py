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



import asyncio
import aiohttp
import logging



previous_skins = set()
current_skins = set()



async def getdata():
    global previous_skins
    global current_skins
    try:
        new_skins = set()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.white.market/graphql/api", json=payload, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["data"]["market_list"]["edges"]:
                        node = obj["node"]
                        name = str(node["item"]["description"]["nameHash"]).strip()
                        price = str(float(node["price"]["value"]))
                        link = f"https://white.market/item/{node['slug']}"
                        new_skins.add((name, price, link, "WhiteMarket"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/whitemarket.txt", "w", encoding="utf-8") as f:
                for skin in updated_skins:
                    f.write(skin[0] + ";" + skin[1] + ";" + skin[2]+ ";" + skin[3] + "\n")
                    await asyncio.sleep(0.06)
    except Exception as e:
        print(e)
 


async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(10)



asyncio.run(main())