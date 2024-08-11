import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser")
        if data:
            for obj in data["objects"]:
                name = str(obj["title"])
                price = str(float(obj["price"]["USD"])/100)
                link = "https://dmarket.com/ingame-items/item-list/csgo-skins?ref=y9l2rUxEFC&userOfferId="+obj["extra"]["linkId"]
                new_skins.add((name, price, link, "Dmarket"))


            with open("textFiles/dmarket.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(6)



asyncio.run(main())