import asyncio
import aiohttp
import logging
import random


previous_skins = set()
current_skins = set()



async def getdata():
    global previous_skins
    global current_skins
    try:
        new_skins = set()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://csgofloat.com/api/v1/listings?limit=50&sort_by=most_recent", timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data:
                        name = str(obj["item"]["market_hash_name"])
                        price = str(float(obj["price"])/100)
                        link = "https://csgofloat.com/item/"+obj["id"]
                        new_skins.add((name, price, link, "CSGOfloat"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/csgofloat.txt", "w", encoding="utf-8") as f:
                for skin in updated_skins:
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
            await asyncio.sleep(random.randrange(50, 90))



asyncio.run(main())