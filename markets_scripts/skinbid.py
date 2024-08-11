import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://api.skinbid.com/api/search/auctions?take=120&skip=0&sellType=all&sort=created%23desc&goodDeals=false&popular=false&currency=USD")
        if data:
            for obj in data["items"]:
                name = str(obj["items"][0]["item"]["fullName"])
                price = str(obj["nextMinimumBid"])
                link = "https://skinbid.com/listings?search="+name
                new_skins.add((name, price, link, "SkinBid"))

            with open("textFiles/skinbid.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(12)



asyncio.run(main())