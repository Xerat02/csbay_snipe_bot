import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://cs.money/1.0/market/sell-orders?limit=60&offset=0&order=desc&sort=insertDate")
        if data:
            for obj in data["items"]:
                skin_data = {
                    "name": str(obj["asset"]["names"]["full"]),
                    "price": str(float(obj["pricing"]["default"])),
                    "link": "https://cs.money/market/buy?sort=price&order=asc&search=" + obj["asset"]["names"]["full"],
                    "source": "CSMoney"
                }
                if "stickers" in obj:
                    if obj["stickers"]:
                        sticker_names = []
                        for sticker in obj["stickers"]:
                            if sticker:
                                sticker_names.append(sticker["name"])
                        skin_data["stickers"] = sticker_names
                new_skins.append(skin_data)
                new_skins.append(skin_data)

            with open("textFiles/csmoney.json", "w", encoding="utf-8") as f:
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