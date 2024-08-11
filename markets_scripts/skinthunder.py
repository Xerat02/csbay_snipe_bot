import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://skinthunder.com/api/inventory/list", method="post", json_format={"page":1,"sort":"ageASC","perPage":40})
        if data:
            for obj in data["items"]:
                name = str(obj["market_hash_name"])
                price = str(obj["webApiInfo"]["market_price"])
                link = "https://skinthunder.com/product/"+obj["id"]
                new_skins.add((name, price, link, "Skinthunder"))


            with open("textFiles/skinthunder.txt", "w", encoding="utf-8") as f:
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