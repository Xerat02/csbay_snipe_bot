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
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.skinwallet.com/en/market/get-offers?appId=730&page=1&sortBy=Newest", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    new_skins = set()
                    for obj in data["offerThumbnails"]["thumbnails"]:
                        name = str(obj["marketHashName"]).replace("|","").replace("  "," ")
                        price = str(float(obj["price"]["amount"])/100)
                        link = "https://www.skinwallet.com/market/offer/"+obj["inventoryItemId"]
                        image = "https://steamcommunity-a.akamaihd.net/economy/image/"+obj["imageUrl"]
                        new_skins.add((name, price, link, image,"Skinwallet"))

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                return
            else:
                with open("textFiles/skinwallet.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(12)


asyncio.run(main())
