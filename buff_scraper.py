import requests
import time
from forex_python.converter import CurrencyRates

cookies = {'session': '1-_u3BKl-VGFj6uh3iPrlzAhAK2L7G1JkxSIczyvv99igo2030480540'}


f = open("demo.txt", "w", encoding="utf-8")

def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    converted_amount = c.convert(from_currency, to_currency, amount)
    return converted_amount

for x in range(261):
    url = "https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num=" + str(x+1)
    r = requests.get(url,cookies=cookies)

    items = r.json()
    itemsData = items['data']
    for item in itemsData['items']:
        try:
            f.write(str(item['id']) + ";" + str(item['market_hash_name']).replace("|", "").replace("  ", " ") + ";" + str(convert_currency(float(item['sell_min_price']), "CNY", "USD")) + "\n")
        except Exception as e:    
            print(e)
    time.sleep(5)

f.close()