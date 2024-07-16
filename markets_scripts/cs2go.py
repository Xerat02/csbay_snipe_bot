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
            async with session.get("https://g-api.cs2go.com/api/market/item/filter/rank?order_by=1&app_id=730&page=1&size=100", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["items"]:
                        name = str(obj["market_hash_name"])
                        price = str(float(obj["dqf_price"]))
                        link = "https://www.cs2go.com/spu/730/"+obj["read_name"]
                        new_skins.add((name, price, link, "CS2GO"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/cs2go.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(30)



asyncio.run(main())