from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio

# create a headless browser  
opt = Options()
opt.add_argument('-headless')
driver = webdriver.Firefox(options=opt)
previous_skins = set()
current_skins = set()
# load the page
driver.get('https://skinport.com/market?sort=date&order=desc')
wait = WebDriverWait(driver, 40)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ItemPreview-itemName")))
button = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, 'LiveBtn')))
button.click()

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
        return "err"

async def extract_wear_skinport(wear):
    first_word = wear.partition(" ")[0] # assuming you're extracting the first word from a sentence
    replacements = {
        "factory": "(Factory New)",
        "field": "(Field-Tested)",
        "minimal": "(Minimal Wear)",
        "well": "(Well-Worn)",
        "battle": "(Battle-Scarred)"
    }
    return replacements.get(str(first_word).lower(), "")
    
async def get_latest_offers_skinport():
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
            pass
        else:
            with open("skinport.txt", "w", encoding="utf-8") as f:
                for skin in new_skins:
                    f.write(skin[0] + ";" + skin[1] + ";" + str(skin[2]) + ";" + skin[3] + ";" + skin[4] + ";" + skin[5] + "\n")
    except:
        pass
  
async def main():
    while True:
         await get_latest_offers_skinport()
         await asyncio.sleep(2)

asyncio.run(main())
        
