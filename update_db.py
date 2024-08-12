import asyncio
import json
import re
import unicodedata
from pymongo import MongoClient, UpdateOne, DeleteOne
import markets_scripts.tools.module as tl



cfg = json.load(open("configs/config.json"))
mongo_client = MongoClient(cfg["mongoDB"]["uri"])
db = mongo_client["csbay"]
collection = db["buff_items"]



async def update_search_names():
    operations = []
    cursor = collection.find({})

    for document in cursor:
        item_id = document.get("_id")
        market_hash_name = document.get("market_hash_name")

        if market_hash_name:
            search_name = tl.preprocess_string(market_hash_name)
            operations.append(
                UpdateOne(
                    {"_id": item_id},
                    {
                        "$set": {
                            "search_name": search_name
                        },
                        "$unset": {
                            "steam_update_time": ""
                        }
                    }
                )
            )
        else:
            operations.append(
                DeleteOne({"_id": item_id})
            )

    if operations:
        # Perform the bulk write operation asynchronously
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: collection.bulk_write(operations))
        print(f"Updated {len(operations)} items.")






async def main():
    try:
        await update_search_names()
    except Exception as e:
        print(f"An error occurred: {e}")



asyncio.run(main())
