
import asyncio
import aiohttp
import random
import json
import tools.module as tl
from datetime import datetime
from pymongo import MongoClient, UpdateOne

cfg = json.load(open("configs/config.json"))
cookies = {'session': '1-73N9nnxv100xcZlM6_j7b2vc4KrGof-DlWpOGepIQXCL2030480540'}
pool = None
cur_rate = 0

mongo_client = MongoClient(cfg["mongoDB"]["uri"])
db = mongo_client["csbay"]
collection = db["buff_items"]
  


async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("CNY", 1)
    await asyncio.sleep(360) 



async def scrape():
    for x in range(270):
        url = f"https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num={x + 1}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10, cookies=cookies) as response:
                    items = await response.json()
                    code = str(items['code']).lower()
                    if response.status == 200 and code == "ok":
                        items_data = items['data']['items']
                        operations = []

                        for item in items_data:
                            item_id = item['id']
                            market_hash_name = str(item['market_hash_name'])
                            price_in_usd = float(item['sell_min_price']) * cur_rate
                            buy_max_price = float(item['buy_max_price']) * cur_rate
                            buy_num = int(item["buy_num"])
                            sell_num = int(item["sell_num"])
                            item_image = str(item["goods_info"]["icon_url"])
                            update_time = datetime.now()

                            operations.append(
                                UpdateOne(
                                    {'_id': item_id},
                                    {
                                        '$set': {
                                            'market_hash_name': market_hash_name,
                                            'price_in_usd': price_in_usd,
                                            'buy_max_price': buy_max_price,
                                            'buy_num': buy_num,
                                            'sell_num': sell_num,
                                            'item_image': item_image,
                                            'update_time': update_time
                                        }
                                    },
                                    upsert=True
                                )
                            )
                        
                        if operations:
                            result = collection.bulk_write(operations)
                            print(f"Page {x+1}: {result.upserted_count} items upserted, {result.modified_count} items modified.")
        
        except Exception as e:
            tl.exceptions(e)
            return
        finally:
            print(f"Response status: {response.status}\nCode message: {code}")
            await asyncio.sleep(random.randrange(14, 28))
     

async def main():
    global pool
    pool = await tl.set_db_conn()
    while True:
        try:
          await asyncio.gather(scrape(), convert_currency())
        except Exception as e:
          tl.exceptions(e)
          return 



asyncio.run(main())