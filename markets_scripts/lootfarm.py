import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
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
                    link = "https://loot.farm/#skin=730_" + name.replace(" ", "%20")
                    skin_data = {
                        "name": name,
                        "price": price,
                        "link": link,
                        "source": "Lootfarm"
                    }
                    new_skins.append(skin_data)

            with open("textFiles/lootfarm.json", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(60)



asyncio.run(main())