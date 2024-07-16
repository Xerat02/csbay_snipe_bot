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
            async with session.get("https://www.skinwallet.com/en/market/get-offers?appId=730&page=1&sortBy=Newest", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["offerThumbnails"]["thumbnails"]:
                        name = str(obj["marketHashName"])
                        price = str(float(obj["price"]["amount"])/100)
                        link = "https://www.skinwallet.com/market/offer/"+obj["inventoryItemId"]
                        new_skins.add((name, price, link, "Skinwallet"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/skinwallet.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(6)



asyncio.run(main())