from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import asyncio

# Vytvořit headless prohlížeč    
opt = Options()
opt.add_argument('-headless')
driver = webdriver.Firefox(options=opt)
previous_skins = []
current_skins = []
# Načíst stránku
driver.get('https://dmarket.com/ingame-items/item-list/csgo-skins')
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
wait.until(EC.presence_of_all_elements_located((By.XPATH, "//img")))
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ItemPreview-itemName")))
# Najdeme element drop menu
menu = driver.find_element_by_id('menu')
select = Select(menu)
select.select_by_visible_text('položka1')

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
    try:
        wear = str(wear)
        wear = wear.lower()
        if wear.startswith("factory"):
            wear = "(Factory New)"
        elif wear.startswith("field"):
            wear = "(Field-Tested)"
        elif wear.startswith("minimal"):
            wear = "(Minimal Wear)"    
        elif wear.startswith("well"):
            wear = "(Well-Worn)"
        elif wear.startswith("battle"):
            wear = "(Battle-Scarred)"
        else:
            wear = ""
        return wear    
    except:
        return "err"
    
async def get_latest_offers_skinport():
    global previous_skins
    global current_skins
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ItemPreview-itemName')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        current_skins = []
       
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
                current_skins.append({'skin_name': skin_name,'wear': await extract_wear_skinport(wear), 'price': await extract_price_skinport(price), 'link': link, 'img': img, 'market' : "Skinport"})

        new_skins = []
        for skin in current_skins:
            if skin not in previous_skins:
                new_skins.append(skin)
        
        previous_skins = current_skins
        if len(new_skins) == 0:
            return 0
        else:    
            with open("skinport.txt", "w", encoding="utf-8") as f:
                for skins in new_skins:
                    f.write(skins["skin_name"]+";"+skins["wear"]+";"+str(skins["price"])+";"+skins["link"]+";"+skins["img"]+";"+skins["market"]+"\n")
    except:
        return 0
    
async def main():
    while True:
        await asyncio.gather(get_latest_offers_skinport())

asyncio.run(main())
        
