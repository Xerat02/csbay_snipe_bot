import asyncio
import aiohttp
import logging
import tools.module as tl



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    await convert_currency()
    try:
        new_skins = set()
        data = await tl.fetch("https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&sort=NF&language=en")
        if data:
            for obj in data["aggregatedMetaOffers"]:
                if "singleOffer" in obj and "exteriorClassName" in obj["singleOffer"]:
                    offer = obj["singleOffer"]
                    name = str(offer["localizedName"])
                    wear = f" ({offer['exteriorClassName']})"
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

            with open("textFiles/skinbaron.txt", "w", encoding="utf-8") as f:
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