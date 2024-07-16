import asyncio
import aiohttp
import logging



previous_skins = set()
current_skins = set()



async def getdata():
    global previous_skins
    global current_skins
    try:
        new_skins = set()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.skinbid.com/api/search/auctions?take=120&skip=0&sellType=all&sort=created%23desc&goodDeals=false&popular=false&currency=USD", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["items"]:
                        name = str(obj["items"][0]["item"]["fullName"])
                        price = str(obj["nextMinimumBid"])
                        link = "https://skinbid.com/listings?search="+name
                        new_skins.add((name, price, link, "SkinBid"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/skinbid.txt", "w", encoding="utf-8") as f:
                for skin in updated_skins:
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
            await asyncio.sleep(10)



asyncio.run(main())