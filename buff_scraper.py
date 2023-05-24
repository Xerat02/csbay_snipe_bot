import requests
import time

cookies = {'session': '1-daSaAoELg2mqXCKK2yC4WbH60Ys5hC3GCEcvuJG-CONw2030480540'}


f = open("demo.txt", "w", encoding="utf-8")

for x in range(261):
    url = "https://buff.163.com/api/market/goods/all?game=csgo&page_size=80&page_num=" + str(x+1)
    r = requests.get(url,cookies=cookies)

    items = r.json()
    itemsData = items['data']
    for item in itemsData['items']:
        f.write(str(item['id']) + ";" + item['market_hash_name'] + ";" + item['sell_min_price'] + "\n")

    time.sleep(5)

f.close()