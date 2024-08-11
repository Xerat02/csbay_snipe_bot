import asyncio
import aiohttp
import logging
import tools.module as tl



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    await convert_currency()
    try:
        new_skins = set()
        data = await tl.fetch("https://api.gamerpay.gg/feed?page=1&market=steam")
        if data:
            for obj in data["items"]:
                name = str(obj["marketHashName"])
                price = str((float(obj["price"])*cur_rate)/100)
                link = "https://gamerpay.gg/item/"+str(obj["id"])+"&ref=63c4f5a485"
                new_skins.add((name, price, link, "Gamerpay"))

            with open("textFiles/gamerpay.txt", "w", encoding="utf-8") as f:
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