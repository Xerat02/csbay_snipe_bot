import asyncio
import aiohttp
import logging
import random

previous_skins = set()
current_skins = set()
lock = asyncio.Lock()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

async def getdata():
    global previous_skins
    global current_skins
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://csgofloat.com/api/v1/listings?limit=50&sort_by=most_recent", timeout=30) as response:
                print(response.status) 
                if response.status == 200:
                    data = await response.json()
                    new_skins = set()
                    for obj in data:
                        name = str(obj["item"]["market_hash_name"]).replace("|","").replace("  "," ")
                        price = str(float(obj["price"])/100)
                        image = "https://community.cloudflare.steamstatic.com/economy/image/"+obj["item"]["icon_url"]
                        link = "https://csgofloat.com/item/"+obj["id"]
                        new_skins.add((name,price,link,image,"CSGOfloat"))

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                return
            else:
                with open("textFiles/csgofloat.txt", "w", encoding="utf-8") as f:
                    for skin in updated_skins:
                        f.write(skin[0] + ";" + skin[1] + ";" + skin[2]+ ";" + skin[3] + ";" + skin[4] + "\n")
                        await asyncio.sleep(0.06)
    except asyncio.TimeoutError as e:
        logging.error("Timeout occurred during getting data: %s", e)
    except Exception as e:
        logging.error("Error occurred during getting data: %s", e)


async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            logging.error("Error occurred during scraping: %s", e)
        finally:
            await asyncio.sleep(random.randrange(50, 90))


asyncio.run(main())