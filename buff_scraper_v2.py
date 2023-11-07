import asyncio
import aiohttp
import random
import json
import tools.module as tl
from datetime import datetime

cfg = json.load(open("configs/config.json"))
cookies = {'session': '1-awmXwXzw6fGl5MJpP5M6Nt4d6XfjFmPEllVvUBXH6TTM2030480540'}
pool = None
cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("CNY", 1)
    await asyncio.sleep(360) 



async def scrape():
    for x in range(270):
        db_connection = await tl.get_db_conn(pool)
        cursor = await db_connection.cursor()
        url = "https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num=" + str(x + 1)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10, cookies=cookies) as response:
                    items = await response.json()
                    code = str(items['code']).lower()
                    if response.status == 200 and code == "ok":
                        itemsData = items['data']
                        for item in itemsData['items']:
                            item_id = item['id']
                            market_hash_name = str(item['market_hash_name']).replace("|", "").replace("  ", " ")
                            price_in_usd = float(item['sell_min_price']) * cur_rate
                            buy_max_price = float(item['buy_max_price']) * cur_rate
                            buy_num = int(item["buy_num"])
                            sell_num = int(item["sell_num"])
                            update_time = datetime.now()
                            sql = "INSERT INTO buff_skins (id, market_hash_name, price_in_usd, buy_max_price, buy_num, sell_num, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s) " \
                                  "ON DUPLICATE KEY UPDATE market_hash_name = VALUES(market_hash_name), " \
                                  "price_in_usd = VALUES(price_in_usd), "\
                                  "buy_max_price = VALUES(buy_max_price), "\
                                  "buy_num = VALUES(buy_num), "\
                                  "sell_num = VALUES(sell_num), "\
                                  "update_time = VALUES(update_time)"
                            await tl.db_manipulate_data(sql, cursor, db_connection, True, item_id, market_hash_name, price_in_usd, buy_max_price, buy_num, sell_num, update_time)
                        print("New buff skins were successfully commited to the database! Page: "+str(x))                   
        except Exception as e:
            tl.exceptions(e)
            return
        finally:
            await tl.release_db_conn(cursor,db_connection,pool)
            print("Response status: "+str(response.status)+"\nCode message: "+code)
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