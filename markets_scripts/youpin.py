import asyncio
import aiohttp
import logging
import json
import tools.module as tl



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("CNY", 1)



async def getdata():
    await convert_currency()
    try:
        new_skins = []
        data = await tl.fetch("https://api.youpin898.com/api/v2/commodity/template/GetCsGoNewOnShelf?Count=100")
        if data:
            for obj in data["Data"]:
                skin_data = {
                    "name": str(obj["CommodityHashName"]),
                    "price": str(float(obj["Price"]) * cur_rate),
                    "link": "https://www.youpin898.com/goodInfo?id="+str(obj["Id"]),
                    "source": "Youpin"
                }
                new_skins.append(skin_data)

            with open("textFiles/youpin.json", "w", encoding="utf-8") as f:
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