headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
  


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
            async with session.get("https://mannco.store/items?a=&b=&c=&d=&e=&f=&g=&h=1&i=0&game=730&j=1&k=&l=&m=&n=&o=&s=DESC&t=&skip=0", headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data:
                        name = str(obj["name"])
                        price = str(float(obj["price"])/100)
                        link = "https://mannco.store/item/"+str(obj["url"])
                        new_skins.add((name, price, link, "Mannco"))

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/mannco.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(10)



asyncio.run(main())