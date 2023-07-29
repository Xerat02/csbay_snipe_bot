from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import logging



previous_skins = set()
current_skins = set()



logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')



async def create_driver():
    try:
        logging.info("Creating driver...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-cache")
        driver = webdriver.Firefox(options=options)
        return driver
    except Exception as e:
        logging.error("Error occurred during driver setup: %s", e)
        return None



async def close_driver(driver):
    try:
        logging.info("Closing driver...")
        if driver:
            driver.quit()
    except Exception as e:
        logging.error("Error occurred during driver cleanup: %s", e)



async def set_up():
    driver = None  
    try:
        driver = await create_driver()
        if driver:
            logging.info("Trying to start driver...")
            driver.set_page_load_timeout(20)
            driver.get('https://skinport.com/market?sort=date&order=desc')
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "CatalogPage-item")))
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'LiveBtn')))
            button.click()
    except Exception as e:
        logging.error("Error occurred during driver setup: %s", e)
        if driver is not None:
            await close_driver(driver)  
        driver = None  
    return driver
    


async def extract_price_skinport(text):
    try:
        start_index = text.find("€")
        if "−" in text:
            end_index = text.find("−")
        else:
            end_index = text.find(" ")
        if start_index == -1 or end_index == -1:
            return None
        if "," not in text:
            result = text[start_index + 1:end_index]
            result = (float(str(result).strip()))*1.09
            return result
        else:
            return None
    except Exception as e:
        logging.error("Error occurred during extracting price: %s", e)
        return None



async def extract_wear_skinport(wear):
    try:
        first_word = wear.partition(" ")[0]
        replacements = {
            "factory": "(Factory New)",
            "field": "(Field-Tested)",
            "minimal": "(Minimal Wear)",
            "well": "(Well-Worn)",
            "battle": "(Battle-Scarred)"
        }
        return replacements.get(str(first_word).lower(), "")
    except Exception as e:
        logging.error("Error occurred during extracting wear: %s", e)
        return None
    


async def get_latest_offers_skinport(driver):
    global previous_skins
    global current_skins

    try:
        logging.info("Getting a new data from skinport...")
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'ItemPreview-itemName')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        current_skins = set()

        for item in soup.find_all('div', {'class': 'ItemPreview-content'}):
            skin_type = item.find('div', {'class': 'ItemPreview-itemTitle'}).text.strip()
            name = item.find('div', {'class': 'ItemPreview-itemName'}).text.strip()
            if str(skin_type).lower() != "container":
                skin_name = skin_type + ' ' + name
            else:
                skin_name = name 
            wear = item.find('div', {'class': 'ItemPreview-itemText'}).text.strip()
            price = item.find('div', {'class': 'ItemPreview-priceValue'}).text.strip()+" "
            link = "https://skinport.com"+item.find('a')['href']
            img = item.find('img')['src']
            extracted_price = await extract_price_skinport(price)
            if extracted_price is not None:
                current_skins.add((skin_name, await extract_wear_skinport(wear), extracted_price, link, img, "Skinport"))
            else:
                return

        new_skins = current_skins - previous_skins
        previous_skins = current_skins
        
        if not new_skins:
            return
        else:
            with open("skinport.txt", "w", encoding="utf-8") as f:
                for skin in new_skins:
                    f.write(skin[0] + ";" + skin[1] + ";" + str(skin[2]) + ";" + skin[3] + ";" + skin[4] + ";" + skin[5] + "\n")
                    await asyncio.sleep(0.06) 
    except Exception as e:
        logging.error("Error occurred during getting skinport data: %s", e)  
  


async def main():
    driver = None
    cycles = 1

    while True:
        try:
            if not driver:
                driver = await set_up()
            else:
                await get_latest_offers_skinport(driver)
        except Exception as e:
            logging.error("Error occurred during get_latest_offers_skinport or set_up : %s", e)
        finally:
            if driver:
                if cycles > 20000:
                    await close_driver(driver)
                    driver = None
                    cycles = 1
                    logging.info("Restarting driver....")
                else:
                    logging.info("Cycle n.: " + str(cycles))
                    cycles += 1
            await asyncio.sleep(1)



asyncio.run(main())