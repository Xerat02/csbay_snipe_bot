import asyncio
import aiohttp
import logging

previous_skins = set()
current_skins = set()
lock = asyncio.Lock()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

async def getdata():
    global previous_skins
    global current_skins
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://mannco.store/items?a=&b=&c=&d=&e=&f=&g=&h=1&i=0&game=730&j=1&k=&l=&m=&n=&o=&s=DESC&t=&skip=0", headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    new_skins = set()
                    for obj in data:
                        name = str(obj["name"])
                        price = str(float(obj["price"])/100)
                        link = "https://mannco.store/item/"+obj["url"]
                        image = "https://steamcommunity-a.akamaihd.net/economy/image/"+obj["image"]
                        new_skins.add((name, price, link, image,"Mannco"))

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                return
            else:
                with open("textFiles/mannco.txt", "w", encoding="utf-8") as f:
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
