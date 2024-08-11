import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://tradeit.gg/api/v2/inventory/data?gameId=730&offset=0&limit=500&sortType=Release+Date&searchValue=&minFloat=0&maxFloat=1&showTradeLock=true&onlyTradeLock=true&colors=&showUserListing=true&stickerName=&tradeLockDays[]=8&fresh=true&isForStore=1")
        if data:
            for obj in data["items"]:
                name = str(obj["name"])
                price = str(float(obj["storePrice"])/100)
                link = "https://tradeit.gg/csgo/store?search="+name
                new_skins.add((name, price, link, "TradeIt"))

            with open("textFiles/tradeit.txt", "w", encoding="utf-8") as f:
                for skin in new_skins:
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
            await asyncio.sleep(12)



asyncio.run(main())