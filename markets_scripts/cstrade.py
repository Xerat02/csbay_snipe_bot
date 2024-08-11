import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://cdn.cs.trade:8443/api/getInventoryCmp?order_by=price_desc&bot=all&_=1722866759008")
        if data:
            for obj in data["inventory"]:
                name = str(obj["n"])
                price = str(obj["p"])
                link = "https://cs.trade/store/"+str(obj["id"])
                new_skins.add((name, price, link, "CSTrade"))

            with open("textFiles/cstrade.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(30)



asyncio.run(main())