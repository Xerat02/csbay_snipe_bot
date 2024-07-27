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
            async with session.get("https://api.buff.market/api/market/goods?game=csgo&page_num=1&page_size=50", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["data"]["items"]:
                        name = str(obj["market_hash_name"])
                        price = str(float(obj["sell_min_price"]))
                        link = "https://buff.market/market/goods/"+str(obj["id"])
                        new_skins.add((name, price, link, "BUFFMarket"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/buffmarket.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(random.randrange(30, 50))



asyncio.run(main())