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
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://api.white.market/graphql/api", json_format=payload)
        if data:
            for obj in data["data"]["market_list"]["edges"]:
                node = obj["node"]
                skin_data = {
                    "name": str(node["item"]["description"]["nameHash"]).strip(),
                    "price": str(float(node["price"]["value"])),
                    "link": f"https://white.market/item/{node['slug']}",
                    "source": "WhiteMarket"
                }
                new_skins.append(skin_data)

            with open("textFiles/whitemarket.json", "w", encoding="utf-8") as f:
                json.dump(new_skins, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)



async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(12)



asyncio.run(main())