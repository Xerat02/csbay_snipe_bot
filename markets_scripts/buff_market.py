import asyncio
import aiohttp
import logging
import tools.module as tl


async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://api.buff.market/api/market/goods?game=csgo&page_num=1&page_size=50")
        if data:
            for obj in data["data"]["items"]:
                name = str(obj["market_hash_name"])
                price = str(float(obj["sell_min_price"]))
                link = "https://buff.market/market/goods/"+str(obj["id"])
                new_skins.add((name, price, link, "BUFFMarket"))

            with open("textFiles/buffmarket.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(20)



asyncio.run(main())