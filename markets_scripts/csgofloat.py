import asyncio
import aiohttp
import logging
import json
import tools.module as tl



cookies = {"session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGVhbV9pZCI6Ijc2NTYxMTk5MjM5Mzc0OTU2Iiwibm9uY2UiOjAsImltcGVyc29uYXRlZCI6ZmFsc2UsImlzcyI6ImNzdGVjaCIsImV4cCI6MTcyNjY5ODYwM30.zBblKvzXiwHskgj0HcwSuyo0LzLSShvhMicGqObLA3c"}



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://csgofloat.com/api/v1/listings?limit=50&sort_by=most_recent", cookies=cookies)
        if data:
            for obj in data:
                skin_data = {
                    "name": str(obj["item"]["market_hash_name"]),
                    "price": str(float(obj["price"]) / 100),
                    "link": "https://csgofloat.com/item/" + obj["id"],
                    "source": "CSGOfloat"
                }
                if "stickers" in obj["item"]:
                    sticker_names = [sticker["name"] for sticker in obj["item"]["stickers"]]
                    skin_data["stickers"] = sticker_names
                new_skins.append(skin_data)

            with open("textFiles/csgofloat.json", "w", encoding="utf-8") as f:
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