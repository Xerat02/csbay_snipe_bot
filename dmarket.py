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
            async with session.get("https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    new_skins = set()
                    for obj in data["objects"]:
                        name = str(obj["title"])
                        price = str(float(obj["price"]["USD"])/100)
                        link = "https://dmarket.com/ingame-items/item-list/csgo-skins?ref=y9l2rUxEFC&userOfferId="+obj["extra"]["linkId"]
                        image = obj["image"]
                        new_skins.add((name, price, link, image,"Dmarket"))

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                return
            else:
                with open("textFiles/dmarket.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(9)


asyncio.run(main())
