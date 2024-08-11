import asyncio
import aiohttp
import logging
import tools.module as tl



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("CNY", 1)



async def getdata():
    await convert_currency()
    try:
        new_skins = set()
        data = await tl.fetch("https://api.youpin898.com/api/v2/commodity/template/GetCsGoNewOnShelf?Count=100")
        if data:
            for obj in data["Data"]:
                name = str(obj["CommodityHashName"])
                price = str(float(obj["Price"]) * cur_rate)
                link = "https://www.youpin898.com/goodInfo?id="+str(obj["Id"])
                new_skins.add((name, price, link, "Youpin"))

            with open("textFiles/youpin.txt", "w", encoding="utf-8") as f:
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