import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser")
        if data:
            for obj in data["objects"]:
                skin_data = {
                    "name": str(obj["title"]),
                    "price": str(float(obj["price"]["USD"]) / 100),
                    "link": "https://dmarket.com/ingame-items/item-list/csgo-skins?ref=y9l2rUxEFC&userOfferId=" + obj["extra"]["linkId"],
                    "source": "Dmarket"
                }
                extra = obj.get("extra")
                if "stickers" in extra:
                    sticker_names = [sticker["name"] for sticker in extra["stickers"]]
                    skin_data["stickers"] = sticker_names
                new_skins.append(skin_data)

            with open("textFiles/dmarket.json", "w", encoding="utf-8") as f:
                json.dump(new_skins, f, indent=4, ensure_ascii=False)
    except Exception as e:
        tl.exceptions(e)


async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(3)



asyncio.run(main())