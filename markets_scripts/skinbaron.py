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
            async with session.get("https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&sort=NF&language=enr", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["aggregatedMetaOffers"]:
                        if "singleOffer" in obj and "exteriorClassName" in obj["singleOffer"]:
                            wear = " ("+obj["singleOffer"]["exteriorClassName"]+")"
                            price = str(float(obj["singleOffer"]["itemPrice"])*1.1)
                            new_skins.add(((str(obj["singleOffer"]["localizedName"]) + wear),price,"https://skinbaron.de/en"+obj["offerLink"],"SkinBaron"))
                        elif "lowestPrice" in obj:
                            price = str(float(obj["lowestPrice"]*1.1))
                            new_skins.add((str(obj["extendedProductInformation"]["localizedName"]),price,"https://skinbaron.de/en"+obj["offerLink"],"SkinBaron"))    

        updated_skins = new_skins - previous_skins
        previous_skins = new_skins

        if not updated_skins:
            return
        else:
            with open("textFiles/skinbaron.txt", "w", encoding="utf-8") as f:
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