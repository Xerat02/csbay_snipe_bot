import asyncio
import aiohttp
import logging
import json
import tools.module as tl



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    await convert_currency()
    try:
        new_skins = []
        data = await tl.fetch("https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&sort=NF&language=en")
        if data:
            for obj in data["aggregatedMetaOffers"]:
                if "singleOffer" in obj and "exteriorClassName" in obj["singleOffer"]:
                    offer = obj["singleOffer"]
                    name = str(offer["localizedName"])
                    wear = f" ({offer['exteriorClassName']})"
                    price = str(float(offer["itemPrice"]) * cur_rate)
                    souvenir = offer.get("souvenirString", "")
                    link = "https://skinbaron.de/en" + obj["offerLink"]
                    name = souvenir + name + wear
                    new_skins.append({"name": name, "price": price, "link": link, "source": "SkinBaron"})
                elif "lowestPrice" in obj:
                    name = str(obj["extendedProductInformation"]["localizedName"])
                    price = str(float(obj["lowestPrice"] * cur_rate))
                    link = "https://skinbaron.de/en" + obj["offerLink"]
                    new_skins.append({"name": name, "price": price, "link": link, "source": "SkinBaron"})

            with open("textFiles/skinbaron.json", "w", encoding="utf-8") as f:
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
            await asyncio.sleep(12)



asyncio.run(main())