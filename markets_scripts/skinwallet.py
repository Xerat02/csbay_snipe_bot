import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://www.skinwallet.com/en/market/get-offers?appId=730&page=1&sortBy=Newest")
        if data:
            for obj in data["offerThumbnails"]["thumbnails"]:
                name = str(obj["marketHashName"])
                price = str(float(obj["price"]["amount"])/100)
                link = "https://www.skinwallet.com/market/offer/"+obj["inventoryItemId"]
                new_skins.add((name, price, link, "Skinwallet"))

            with open("textFiles/skinwallet.txt", "w", encoding="utf-8") as f:
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