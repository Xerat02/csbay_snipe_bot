import asyncio
import aiohttp
import logging
import tools.module as tl


previous_skins = set()
current_skins = set()
cur_rate = 0


async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    global previous_skins
    global current_skins
    await convert_currency()
    try:
        new_skins = set()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.gamerpay.gg/feed?page=1&market=steam", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["items"]:
                        name = str(obj["marketHashName"])
                        price = str((float(obj["price"])*cur_rate)/100)
                        link = "https://gamerpay.gg/item/"+str(obj["id"])
                        new_skins.add((name, price, link, "Gamerpay"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/gamerpay.txt", "w", encoding="utf-8") as f:
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