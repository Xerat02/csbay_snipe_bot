import requests
import time
import mysql.connector
from forex_python.converter import CurrencyRates
from datetime import datetime

cookies = {'session': '1-k5osPhRqYNtCGcMYRmDmlUU8nktJ0WaiHMD4s0w8aPAu2030480540'}

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='user',
    password='Buldozer4563',
    database='csbay'
)

cursor = conn.cursor()

def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    converted_amount = c.convert(from_currency, to_currency, amount)
    return converted_amount

for x in range(270):
    url = "https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num=" + str(x + 1)
    r = requests.get(url, cookies=cookies)

    items = r.json()
    itemsData = items['data']
    for item in itemsData['items']:
        try:
            item_id = item['id']
            market_hash_name = str(item['market_hash_name']).replace("|", "").replace("  ", " ")
            price_in_usd = convert_currency(float(item['sell_min_price']), "CNY", "USD")
            buy_max_price = convert_currency(float(item['buy_max_price']), "CNY", "USD")
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
            val = (item_id, market_hash_name, price_in_usd, buy_max_price, buy_num, sell_num, update_time)
            cursor.execute(sql, val)

        except Exception as e:
            print(e)

    conn.commit()
    time.sleep(5)

conn.close()
