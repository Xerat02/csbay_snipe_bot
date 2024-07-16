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
            async with session.get("https://tradeit.gg/api/v2/inventory/data?gameId=730&offset=0&limit=120&sortType=Release+Date&searchValue=&minFloat=0&maxFloat=1&showTradeLock=true&onlyTradeLock=false&colors=&showUserListing=true&stickerName=&fresh=true&isForStore=1", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["items"]:
                        name = str(obj["name"])
                        price = str(float(obj["price"])/100)
                        link = "https://tradeit.gg/csgo/store?search="+name
                        new_skins.add((name, price, link, "TradeIt"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/tradeit.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(20)



asyncio.run(main())