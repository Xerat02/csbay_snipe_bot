from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio



previous_skins = set()
current_skins = set()



def set_up():
    try:
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-software-rasterizer")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-cache")
        driver = webdriver.Firefox(options=opt)
        driver.get('https://skinport.com/market?sort=date&order=desc')
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ItemPreview-itemName")))
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'LiveBtn')))
        button.click()
        return driver
    except Exception as e:
        print("Error occurred during driver setup.", e)
        driver.quit()
        return None
    


async def extract_price_skinport(text):
    try:
        start_index = text.find("€")
        if "−" in text:
            end_index = text.find("−")
        else:
            end_index = text.find(" ")
        if start_index == -1 or end_index == -1:
            return None
        result = text[start_index + 1:end_index]
        result = (float(str(result).strip()))*1.09
        return result
    except:
        return None



async def extract_wear_skinport(wear):
    try:
        first_word = wear.partition(" ")[0] # assuming you're extracting the first word from a sentence
        replacements = {
            "factory": "(Factory New)",
            "field": "(Field-Tested)",
            "minimal": "(Minimal Wear)",
            "well": "(Well-Worn)",
            "battle": "(Battle-Scarred)"
        }
        return replacements.get(str(first_word).lower(), "")
    except Exception as e:
        print("extract_wear_skinport: ",e)
        return None
    


async def get_latest_offers_skinport(driver):
    global previous_skins
    global current_skins

    try:
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
            current_skins.add((skin_name, await extract_wear_skinport(wear), await extract_price_skinport(price), link, img, "Skinport"))

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
        print("get_latest_offers_skinport: ",e)   
  


async def main():
    driver = set_up()
    cycles = 1

    while True:
         try:
             if driver is None:
                driver = set_up()
             else:    
                await get_latest_offers_skinport(driver)
         except Exception as e:
             print("Error occurred during scraping.",e)
         finally:                  
             if driver is not None:
                if cycles > 1000:
                   driver.quit()
                   driver = None   
                   cycles = 1 
                   print("Restarting driver....")
                else:    
                   print("Cycle n.: "+str(cycles))
                   cycles += 1     
             await asyncio.sleep(3)    



asyncio.run(main())
        
