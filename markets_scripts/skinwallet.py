import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://www.skinwallet.com/en/market/get-offers?appId=730&page=1&sortBy=Newest")
        if data:
            for obj in data["offerThumbnails"]["thumbnails"]:
                skin_data = {
                    "name": str(obj["marketHashName"]),
                    "price": str(float(obj["price"]["amount"])/100),
                    "link": "https://www.skinwallet.com/market/offer/"+obj["inventoryItemId"],
                    "source": "Skinwallet"
                }
                new_skins.append(skin_data)

            with open("textFiles/skinwallet.json", "w", encoding="utf-8") as f:
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