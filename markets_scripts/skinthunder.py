import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://skinthunder.com/api/inventory/list", method="post", json_format={"page":1,"sort":"ageASC","perPage":40})
        if data:
            for obj in data["items"]:
                skin_data = {
                    "name": str(obj["market_hash_name"]),
                    "price": str(obj["webApiInfo"]["market_price"]),
                    "link": "https://skinthunder.com/product/"+obj["id"],
                    "source": "Skinthunder"
                }
                new_skins.append(skin_data)

            with open("textFiles/skinflow.json", "w", encoding="utf-8") as f:
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