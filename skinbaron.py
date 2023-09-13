import asyncio
import aiohttp
import logging


previous_skins = set()
current_skins = set()
lock = asyncio.Lock()


async def getdata():
    global previous_skins
    global current_skins

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&sort=NF&language=enr", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    new_skins = set()
                    for obj in data["aggregatedMetaOffers"]:
                        if "singleOffer" in obj and "exteriorClassName" in obj["singleOffer"]:
                            wear = " ("+obj["singleOffer"]["exteriorClassName"]+")"
                            price = str(float(obj["singleOffer"]["itemPrice"])*1.1)
                            new_skins.add(((str(obj["singleOffer"]["localizedName"]).replace("|","").replace("  "," ") + wear),price,"https://skinbaron.de/en"+obj["offerLink"],obj["singleOffer"]["imageUrl"],"SkinBaron"))
                        elif "lowestPrice" in obj:
                            price = str(float(obj["lowestPrice"]*1.1))
                            new_skins.add((str(obj["extendedProductInformation"]["localizedName"]).replace("|","").replace("  "," "),price,"https://skinbaron.de/en"+obj["offerLink"],obj["variant"]["imageUrl"],"SkinBaron"))    

                    async with lock:
                        current_skins.update(new_skins)

                    updated_skins = current_skins - previous_skins
                    previous_skins = current_skins.copy()

                    if not updated_skins:
                        return
                    else:
                        with open("textFiles/skinbaron.txt", "w", encoding="utf-8") as f:
                            for skin in updated_skins:
                                f.write(skin[0] + ";" + skin[1] + ";" + str(skin[2]) + ";" + skin[3] + ";" + skin[4] + "\n")
                                await asyncio.sleep(0.06)
    except asyncio.TimeoutError as e:
        logging.error("Timeout occurred during getting data: %s", e)
    except Exception as e:
        logging.error("Error occurred during getting data: %s", e)


async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            logging.error("Error occurred during scraping: %s", e)
        finally:
            await asyncio.sleep(10)


asyncio.run(main())
