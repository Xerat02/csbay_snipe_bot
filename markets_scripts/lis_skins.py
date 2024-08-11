from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
import random
import asyncio
import csv
import tools.module as tl



# List of user agents for random selection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]



# Randomly select a user agent
user_agent = random.choice(user_agents)



# Configure the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-logging")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--blink-settings=imagesEnabled=false")  
options.add_argument(f"user-agent={user_agent}")



cur_rate = 0



async def convert_currency():
    global cur_rate
    cur_rate = await tl.get_dollar("USD", 1)



async def getdata():
    await convert_currency()
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=options)

        # Enable stealth mode
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
               )

        driver.get("https://lis-skins.ru/market/csgo/?sort_by=date_desc")
        await asyncio.sleep(1)  

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        PRICE_LIST = []
        NAME_LIST = []
        LINK_LIST = []

        price_elements = soup.find_all(class_="price")
        for element in price_elements:
            price_text = element.get_text(strip=True)
            PRICE_LIST.append(str(float(price_text.replace("€","").replace(" ",""))*cur_rate))

        name_elements = soup.find_all('a', class_='name')
        for element in name_elements:
            name_inner = element.find(class_='name-inner').get_text(strip=True)
            name_exterior = element.find(class_='name-exterior')
            if name_exterior:
                name_inner += f" {name_exterior.get_text(strip=True)}"
            NAME_LIST.append(name_inner)

        link_elements = soup.find_all(class_="name", href=True)
        for element in link_elements:
            LINK_LIST.append(element["href"]+"?rf=1302230")

        new_skins = set(zip(NAME_LIST, PRICE_LIST, LINK_LIST))


        with open("textFiles/lis_skins.txt", "w", encoding="utf-8") as f:
            for name, price, link in new_skins:
                f.write(f"{name};{price};{link};Lis-skins\n")
                await asyncio.sleep(0.06)
    except Exception as e:
        print(e)
    finally:
        driver.quit()



async def main():
    while True:
        try:
            await getdata()
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(random.randrange(20, 50))



asyncio.run(main())