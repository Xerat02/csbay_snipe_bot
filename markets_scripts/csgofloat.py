import asyncio
import aiohttp
import logging
import tools.module as tl



cookies = {"session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGVhbV9pZCI6Ijc2NTYxMTk5MjM5Mzc0OTU2Iiwibm9uY2UiOjAsImltcGVyc29uYXRlZCI6ZmFsc2UsImlzcyI6ImNzdGVjaCIsImV4cCI6MTcyMzQxMzE1M30.hk5VivEg48V4sVBnDSdyCfj7UasmuPCXqu-4oXRYoGE"}



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://csgofloat.com/api/v1/listings?limit=50&sort_by=most_recent", cookies=cookies)
        if data:
            for obj in data:
                name = str(obj["item"]["market_hash_name"])
                price = str(float(obj["price"])/100)
                link = "https://csgofloat.com/item/"+obj["id"]
                new_skins.add((name, price, link, "CSGOfloat"))

            with open("textFiles/csgofloat.txt", "w", encoding="utf-8") as f:
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