import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://mannco.store/items/get?quality=&class=&killstreak=&wear=&search=&price=DESC&deals=&page=0&i=22023&game=730&effect=&warpaints=&type=&parts=&spell=&festivized=&age=DESC&sold=&range=&stock=&skip=0", proxy=False)
        if data:
            for obj in data:
                name = str(obj["name"])
                price = str(float(obj["price"])/100)
                link = "https://mannco.store/item/"+str(obj["url"])
                new_skins.add((name, price, link, "Mannco"))

            with open("textFiles/mannco.txt", "w", encoding="utf-8") as f:
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