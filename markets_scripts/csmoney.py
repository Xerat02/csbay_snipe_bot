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
            async with session.get("https://cs.money/1.0/market/sell-orders?limit=60&offset=0&order=desc&sort=insertDate", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["items"]:
                        name = str(obj["asset"]["names"]["full"])
                        price = str(float(obj["pricing"]["default"]))
                        link = "https://cs.money/market/buy?sort=price&order=asc&search="+name
                        new_skins.add((name, price, link, "CSMoney"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/csmoney.txt", "w", encoding="utf-8") as f:
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