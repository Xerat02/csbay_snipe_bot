import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://cdn.cs.trade:8443/api/getInventoryCmp?order_by=price_desc&bot=all&_=1722866759008")
        if data:
            for obj in data["inventory"]:
                skin_data = {
                    "name": str(obj["n"]),
                    "price": str(obj["p"]),
                    "link": "https://cs.trade/store/" + str(obj["id"]),
                    "source": "CSTrade"
                }
                new_skins.append(skin_data)

            with open("textFiles/cstrade.json", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(30)



asyncio.run(main())