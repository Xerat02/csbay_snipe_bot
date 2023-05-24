import asyncio
import requests
import json

previous_skins = set()
current_skins = set()
lock = asyncio.Lock()

async def getdata():
    global previous_skins
    global current_skins

    try:
        response = requests.get("https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&cursor=&limit=50&currency=USD&platform=browser")
        if response.status_code == 200:
            data = json.loads(response.text)
            new_skins = set()

            for obj in data["objects"]:
                if "exterior" in obj["extra"]:
                    wear = "("+obj["extra"]["exterior"]+")"
                else:
                    wear = ""    
                new_skins.add((str(obj["extra"]["name"]).replace("|","").replace("★","").replace("  "," "),wear,str(float(obj["price"]["USD"])/100),"https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId="+obj["extra"]["linkId"],obj["image"],"Dmarket"))

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                print("No new skins.")
                return
            else:
                with open("dmarket.txt", "w", encoding="utf-8") as f:
                    for skin in updated_skins:
                        f.write(skin[0] + ";" + skin[1] + ";" + str(skin[2]) + ";" + skin[3] + ";" + skin[4] + ";" + skin[5] + "\n")
                        await asyncio.sleep(0.06)
    except Exception as e:
        print("Error occurred during getting data:", e)


async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            print("Error occurred during scraping:", e)
        finally:
            await asyncio.sleep(15)


asyncio.run(main())
