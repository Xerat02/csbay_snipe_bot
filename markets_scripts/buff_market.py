import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://api.buff.market/api/market/goods?game=csgo&page_num=1&page_size=50")
        if data:
            for obj in data["data"]["items"]:
                skin_data = {
                    "name": str(obj["market_hash_name"]),
                    "price": str(float(obj["sell_min_price"])),
                    "link": "https://buff.market/market/goods/" + str(obj["id"]),
                    "source": "BUFFMarket"
                }
                new_skins.append(skin_data)

            with open("textFiles/buffmarket.json", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(20)



asyncio.run(main())