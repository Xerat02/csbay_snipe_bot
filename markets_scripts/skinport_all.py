import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://api.skinport.com/v1/items?currency=USD")
        if data:
            for obj in data:
                name = str(obj["market_hash_name"])
                price = str(obj["min_price"])
                link = "https://skinport.com/market?search="+name+"&sort=price&order=asc"
                new_skins.add((name, price, link, "Skinport"))


            with open("textFiles/skinport_all.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(60)



asyncio.run(main())