import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://tradeit.gg/api/v2/inventory/data?gameId=730&offset=0&limit=500&sortType=Release+Date&searchValue=&minFloat=0&maxFloat=1&showTradeLock=true&onlyTradeLock=true&colors=&showUserListing=true&stickerName=&tradeLockDays[]=8&fresh=true&isForStore=1")
        if data:
            for obj in data["items"]:
                skin_data = {
                    "name": str(obj["name"]),
                    "price": str(float(obj["storePrice"])/100),
                    "link": "https://tradeit.gg/csgo/store?search="+str(obj["name"]),
                    "source": "TradeIt"
                }
                new_skins.append(skin_data)

            with open("textFiles/tradeit.json", "w", encoding="utf-8") as f:
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