import asyncio
import aiohttp
import logging
import json
import tools.module as tl



async def getdata():
    try:
        new_skins = []
        data = await tl.fetch("https://api.skinbid.com/api/search/auctions?take=120&skip=0&sellType=all&sort=created%23desc&goodDeals=false&popular=false&currency=USD")
        if data:
            for obj in data["items"]:
                skin_data = {
                    "name": str(obj["items"][0]["item"]["fullName"]),
                    "price": str(obj["nextMinimumBid"]),
                    "link": "https://skinbid.com/market/" + str(obj["items"][0]["auctionHash"]),
                    "source": "SkinBid"
                }
                if "stickers" in obj["items"][0]["item"]:
                    if len(obj["items"][0]["item"]["stickers"]) > 0:
                        if "Sticker" not in skin_data["name"]:
                            sticker_names = [sticker["name"] for sticker in obj["items"][0]["item"]["stickers"]]
                            skin_data["stickers"] = sticker_names
                new_skins.append(skin_data)

            with open("textFiles/skinbid.json", "w", encoding="utf-8") as f:
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