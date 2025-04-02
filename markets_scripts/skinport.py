import socketio
import asyncio
import json
import logging



logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s')
skins = []
sio = socketio.AsyncClient(ssl_verify=True)



@sio.on('saleFeed')
async def on_sale_feed(result):
    try:
        sale = result["sales"][0]
        name = str(sale["marketHashName"])
        price = round(sale["salePrice"] / 100, 2)
        link = f"https://skinport.com/item/{sale['url']}/{sale['saleId']}"
        
        skin_data = {
            "name": name,
            "price": price,
            "link": link,
            "source": "Skinport"
        }
        if "stickers" in sale:
            print("test")
            if len(sale["stickers"]) > 0:
                sticker_names = [sticker["name"] for sticker in sale["stickers"]]
                skin_data["stickers"] = sticker_names
        skins.append(skin_data)
    except Exception as e:
        logging.error("Error occurred during getting data: %s", e)
        await sio.disconnect()



async def write_to_file():
    while True:
        try:
            if skins:
                with open("textFiles/skinport.json", "w", encoding="utf-8") as file:
                    json.dump(skins, file, ensure_ascii=False, indent=4)
                skins.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(2)
        except Exception as e:
            logging.error("Error occurred during writing data: %s", e)



async def start():
    try:
        await sio.connect('https://skinport.com', transports=['websocket'], wait_timeout=10)
        await sio.emit('auth', {'token': 'tBCwBEr0lE98WhOwwKFtB+bho83MOseP9iicE9SygNkmrkfZWAImACCpnNmfmosV5icbVnPYs6T0Gwa0/WLjpg=='})  # Přidejte svůj token
        await sio.emit('saleFeedJoin', {'currency': 'USD', 'locale': 'en', 'appid': 730})
        await sio.wait()
    except Exception as e:
        logging.error("Error occurred during starting websocket: %s", e)



async def main():
    while True:
        try:
            await asyncio.gather(start(), write_to_file())
        except Exception as e:
            logging.error("Error occurred during starting script: %s", e)


       
asyncio.run(main())
