import asyncio
import aiohttp
import random
import json
import aiomysql
from forex_python.converter import CurrencyRates
from datetime import datetime

cfg = json.load(open("configs/config.json"))
cookies = {'session': '1-ykvoh7Qo-7vNI1FL07XOpqBTBhgFUD-v08dEmFQ3IlQ_2030480540'}

async def get_db_connection():
    return await pool.acquire()

async def close_pool():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()

def convert_currency():
    try:
        c = CurrencyRates()
        converted_amount = c.convert("USD", "CNY", 1)
        return float(converted_amount)
    except Exception as e:
        print(e)
        return



async def scrape():
    conversion = convert_currency()
    for x in range(270):
        db_connection = await get_db_connection()
        cursor = await db_connection.cursor()
        url = "https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num=" + str(x + 1)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10,cookies=cookies) as response:
                    if response.status == 200:
                        items = await response.json()
                        itemsData = items['data']
                        for item in itemsData['items']:
                            item_id = item['id']
                            market_hash_name = str(item['market_hash_name']).replace("|", "").replace("  ", " ")
                            price_in_usd = float(item['sell_min_price']) / conversion
                            buy_max_price = float(item['buy_max_price']) / conversion
                            buy_num = int(item["buy_num"])
                            sell_num = int(item["sell_num"])
                            update_time = datetime.now()  # Aktuální datum a čas aktualizace ceny
                            # Insert or update data in the MySQL table
                            sql = "INSERT INTO buff_skins (id, market_hash_name, price_in_usd, buy_max_price, buy_num, sell_num, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s) " \
                                  "ON DUPLICATE KEY UPDATE market_hash_name = VALUES(market_hash_name), " \
                                  "price_in_usd = VALUES(price_in_usd), "\
                                  "buy_max_price = VALUES(buy_max_price), "\
                                  "buy_num = VALUES(buy_num), "\
                                  "sell_num = VALUES(sell_num), "\
                                  "update_time = VALUES(update_time)"
                            await cursor.execute(sql, (item_id, market_hash_name, price_in_usd, buy_max_price, buy_num, sell_num, update_time))
                            await db_connection.commit()
        except Exception as e:
            print(e)
            await close_pool()
            return
        finally:
            if cursor:
                await cursor.close()
            if db_connection:
                pool.release(db_connection)

            print("New buff skins were successfully commited to the database! Page: "+str(x))
            await asyncio.sleep(random.randrange(6, 14))
     

async def main():
  global pool
  pool = await aiomysql.create_pool(
       host = cfg["database"]["host"],
       port = cfg["database"]["port"],
       user = cfg["database"]["user"],
       password = cfg["database"]["password"],
       db = cfg["database"]["db"],
       minsize = cfg["database"]["minsize"],
       maxsize = cfg["database"]["maxsize"]
   )  
  while True:
      try:
        await scrape()
      except Exception as e:
        print(e)
        return 

asyncio.run(main())
