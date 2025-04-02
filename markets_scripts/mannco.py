import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://mannco.store/items/get?quality=&class=&killstreak=&wear=&search=&price=DESC&deals=&page=0&i=22023&game=730&effect=&warpaints=&type=&parts=&spell=&festivized=&age=DESC&sold=&range=&stock=&skip=0", proxy=False)
        if data:
            for obj in data:
                name = str(obj["name"])
                price = str(float(obj["price"]) / 100)
                link = "https://mannco.store/item/" + str(obj["url"])
                skin_data = {
                    "name": name,
                    "price": price,
                    "link": link,
                    "source": "Mannco"
                }
                new_skins.append(skin_data)

            with open("textFiles/mannco.json", "w", encoding="utf-8") as f:
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