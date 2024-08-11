import asyncio
import aiohttp
import logging
import tools.module as tl



async def getdata():
    try:
        new_skins = set()
        data = await tl.fetch("https://loot.farm/botsInventory_730.json")
        wears = {
            "FN": "(Factory New)",
            "MW": "(Minimal Wear)",
            "FT": "(Field-Tested)",
            "WW": "(Well-Worn)",
            "BS": "(Battle-Scarred)"
        }
        if data:
            for key, obj in data["result"].items():
                if "p" in obj:
                    name = obj["n"]
                    if "e" in obj and obj["e"] in wears:
                        name += " " + wears[obj["e"]]
                    price = str(float(obj["p"]) / 100)
                    link = "https://loot.farm/#skin=730_" + name
                    new_skins.add((name, price, link, "Lootfarm"))


            with open("textFiles/lootfarm.txt", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(60)



asyncio.run(main())