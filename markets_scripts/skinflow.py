import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://api.skinflow.gg/bots/items/trade?sort_by=date_received")
        if data:
            for obj in data["results"]:
                skin_data = {
                    "name": str(obj["market_hash_name"]),
                    "price": str(float(obj["offered"])/100),
                    "link": "https://skinflow.gg/buy?referral=CSBAY&search=" + str(obj["market_hash_name"]),
                    "source": "SkinBid"
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