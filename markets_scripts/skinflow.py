import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://api.skinflow.gg/bots/items/trade?sort_by=date_received")
        if data:
            for obj in data["results"]:
                name = str(obj["market_hash_name"])
                price = str(float(obj["offered"])/100)
                link = "https://skinflow.gg/buy?search="+name
                new_skins.add((name, price, link, "Skinflow"))


            with open("textFiles/skinflow.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(6)



asyncio.run(main())