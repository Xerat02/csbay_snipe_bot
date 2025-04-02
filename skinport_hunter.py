from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import logging

# Suppress logging from Selenium
logging.getLogger('selenium').setLevel(logging.CRITICAL)

class SkinHunter:
    def __init__(self, max_price, min_price, market, risk_factor, discount, sell_number):
        self.max_price = max_price
        self.min_price = min_price
        self.market = market
        self.risk_factor = risk_factor
        self.discount = discount
        self.sell_number = sell_number
        self.driver = None

    def get_data_from_api(self):
        response = requests.get("https://api.csbay.org/snipes?buff_discount=0", headers={'Cache-Control': 'no-cache'})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch links from API. Status code: {response.status_code}")
            return []

    def get_right_item_from_data(self, data):
        best_item = None
        highest_discount = 0

        for item in data:
            if item["market_price"] <= self.max_price and item["market_price"] >= self.min_price and item["market_name"].lower() == self.market.lower() and item["market_risk_factor"] <= self.risk_factor and item["buff_discount"] >= self.discount and item["buff_item_sell_num"] >= self.sell_number:
                if item["buff_discount"] > highest_discount:
                    highest_discount = item["buff_discount"]
                    best_item = item

        if best_item:
            print("--------------------------------------------------------------------------------")
            print("Found item with highest discount:")
            print(f"Name: {best_item.get('item_name')}")
            print(f"Market Name: {best_item.get('market_name')}")
            print(f"Buff Price: {best_item.get('buff_price')}")
            print(f"Market Price: {best_item.get('market_price')}")
            print(f"Buff Discount: {best_item.get('buff_discount')}")
            print(f"Market Risk Factor: {best_item.get('market_risk_factor')}")
            print(f"Profit: {best_item.get('profit')}%")
            print(f"Buff Item Sell Number: {best_item.get('buff_item_sell_num')}")
            print(f"Buff Data Update Time: {best_item.get('buff_data_update_time')}")
            print(f"Inserted Time: {best_item.get('inserted_time')}")
            print("--------------------------------------------------------------------------------")
            print("https://skinport.com/market?currency=USD&sort=date&order=desc&search="+"".join(best_item.get('item_name').split()))
            print("--------------------------------------------------------------------------------")
            return best_item.get("market_link")
        return None

    def open_page(self):
        # Set up Chrome options
        chrome_options = Options()

        # Set up the Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)

        # Open the web page
        self.driver.get(self.link)
        print(f"Opened page: {self.link}")

        input("Press anything to end it...")
        self.driver.quit()

    def run(self):
        while True:
            self.link = self.get_right_item_from_data(self.get_data_from_api())
            if self.link:
                self.open_page()
                break
            else:
                time.sleep(1)
                print("No items found, retrying...")

if __name__ == "__main__":
    hunter = SkinHunter(100, 10, "dmarket", 3, 11, 50)
    hunter.run()
