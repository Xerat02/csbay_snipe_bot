import asyncio
import aiohttp
import logging
import json
import tools.module as tl



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    await convert_currency()
    try:
        new_skins = []
        data = await tl.fetch("https://api.gamerpay.gg/feed?page=1&market=steam")
        if data:
            for obj in data["items"]:
                skin_data = {
                    "name": str(obj["marketHashName"]),
                    "price": str((float(obj["price"]) * cur_rate) / 100),
                    "link": "https://gamerpay.gg/item/" + str(obj["id"]) + "&ref=63c4f5a485",
                    "source": "Gamerpay"
                }
                new_skins.append(skin_data)

            with open("textFiles/gamerpay.json", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(12)



asyncio.run(main())