import asyncio
import aiohttp
import logging
import tools.module as tl



previous_skins = set()
current_skins = set()



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    global previous_skins
    global current_skins
    await convert_currency()
    try:
        new_skins = set()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&sort=NF&language=enr", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for obj in data["aggregatedMetaOffers"]:
                        if "singleOffer" in obj and "exteriorClassName" in obj["singleOffer"]:
                            offer = obj["singleOffer"]
                            name = str(offer["localizedName"])
                            wear = f"({offer['exteriorClassName']})"
                            price = str(float(offer["itemPrice"])*cur_rate)
                            souvenir = offer.get("souvenirString", "")
                            link = "https://skinbaron.de/en"+obj["offerLink"]
                            name = souvenir + name + wear
                            new_skins.add((name, price, link, "SkinBaron"))
                        elif "lowestPrice" in obj:
                            name = str(obj["extendedProductInformation"]["localizedName"])
                            price = str(float(obj["lowestPrice"]*cur_rate))
                            link = "https://skinbaron.de/en"+obj["offerLink"]
                            new_skins.add((name, price, link, "SkinBaron"))    

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