import asyncio
import aiohttp
import random
import json
import tools.module as tl
from forex_python.converter import CurrencyRates
from datetime import datetime

cfg = json.load(open("configs/config.json"))
cookies = {'session': '1-eQ9kEbT6tHYyYUcdQTRqZg4KShd6B9n2Klyo7jlw1WSY2030480540'}

#database
pool = None

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
        db_connection = await tl.get_db_conn(pool)
        cursor = await db_connection.cursor()
        url = "https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num=" + str(x + 1)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10,cookies=cookies) as response:
                    items = await response.json()
                    code = str(items['code']).lower()
                    if response.status == 200 and  code == "ok":
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
                            await tl.db_manipulate_data(sql, cursor, db_connection, item_id, market_hash_name, price_in_usd, buy_max_price, buy_num, sell_num, update_time)
                        print("New buff skins were successfully commited to the database! Page: "+str(x))                   
        except Exception as e:
            tl.exceptions(e)
            return
        finally:
            await tl.release_db_conn(cursor,db_connection,pool)
            print("Response status: "+str(response.status)+"\nCode message: "+code)
            await asyncio.sleep(random.randrange(6, 20))
     

async def main():
    global pool
    pool = await tl.set_db_conn()
    while True:
        try:
          await scrape()
        except Exception as e:
          tl.exceptions(e)
          return 

asyncio.run(main())
