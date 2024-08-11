import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://csgoempire.com/api/v2/trading/items?per_page=160&page=1&price_max_above=15&sort=desc&order=deposit_id")
        print(data)
        #if data:
        #    for obj in data["items"]:
        #        name = str(obj["asset"]["names"]["full"])
        #        price = str(float(obj["pricing"]["default"]))
        #        link = "https://cs.money/market/buy?sort=price&order=asc&search="+name
        #        new_skins.add((name, price, link, "CSMoney"))
#
        #    with open("textFiles/csmoney.txt", "w", encoding="utf-8") as f:
        #        for skin in new_skins:
        #            f.write(skin[0] + ";" + skin[1] + ";" + skin[2]+ ";" + skin[3] + "\n")
        #            await asyncio.sleep(0.06)
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