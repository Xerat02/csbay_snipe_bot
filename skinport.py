import socketio
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s')
skins = []
sio = socketio.AsyncClient(ssl_verify=True)


@sio.on('saleFeed')
async def on_sale_feed(result):
    try:
        name = str(result["sales"][0]["marketHashName"])
        price = str(result["sales"][0]["salePrice"] / 100)
        link = "https://skinport.com/item/" + result["sales"][0]["url"] + "/" + str(result["sales"][0]["saleId"])
        image = "https://community.cloudflare.steamstatic.com/economy/image/" + str(result["sales"][0]["image"])
        skins.append(name + ";" + price + ";" + link + ";" + image + ";Skinport")
    except Exception as e:
        logging.error("Error occurred during getting data: %s", e)
        await sio.disconnect()

async def write_to_file():
    while True:
        try:
            if skins:
                data_to_write = "\n".join(skins)
                with open("textFiles/skinport.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_write + "\n")
                skins.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(1)
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
