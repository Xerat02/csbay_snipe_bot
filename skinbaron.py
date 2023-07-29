import asyncio
import requests
import json
import time

previous_skins = set()
current_skins = set()
lock = asyncio.Lock()

async def getdata():
    global previous_skins
    global current_skins

    try:
        response = requests.get("https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&sort=NF&language=enr")
        if response.status_code == 200:
            data = json.loads(response.text)
            new_skins = set()

            for obj in data["aggregatedMetaOffers"]:
                if "singleOffer" in obj and "exteriorClassName" in obj["singleOffer"]:
                    wear = "("+obj["singleOffer"]["exteriorClassName"]+")"
                    new_skins.add((str(obj["singleOffer"]["localizedName"]).replace("|","").replace("★","").replace("  "," "),wear,str(obj["singleOffer"]["itemPrice"]),"https://skinbaron.de/en/"+obj["offerLink"],obj["singleOffer"]["imageUrl"],"SkinBaron"))
                elif "lowestPrice" in obj:
                    wear = ""
                    new_skins.add((str(obj["extendedProductInformation"]["localizedName"]).replace("|","").replace("★","").replace("  "," "),wear,str(obj["lowestPrice"]),"https://skinbaron.de/en/"+obj["offerLink"],obj["variant"]["imageUrl"],"SkinBaron"))    

            async with lock:
                current_skins.update(new_skins)

            updated_skins = current_skins - previous_skins
            previous_skins = current_skins.copy()

            if not updated_skins:
                print("No new skins.")
                return
            else:
                with open("skinbaron.txt", "w", encoding="utf-8") as f:
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
            time.sleep(15)


asyncio.run(main())
