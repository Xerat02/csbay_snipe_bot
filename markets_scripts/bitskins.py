import asyncio
import websockets
import json
import logging



# 1. Nastavení logování na úroveň DEBUG pro všechny moduly
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')



apikey = "271a162d28431d0dcab7ee5496982ded9e0e46726df2e55f3e3a793baac7b7f1"
skins = []



async def connect():
    try:
        async with websockets.connect("wss://ws.bitskins.com") as socket:
            await socket.send(json.dumps(["WS_AUTH_APIKEY", apikey]))
            await socket.send(json.dumps(["WS_SUB", "listed"]))

            async for message in socket:
                action, data = json.loads(message)
                print("Message from server", {"action": action, "data": data})
                if action == "listed":
                    name = str(data["name"])
                    price = str(float(data["price"])/100)
                    link = "https://bitskins.com/item/csgo/"+data["id"]
                    skins.append(name + ";" + price + ";" + link + ";" + "Bitskins") 
    except Exception as e:
        logging.error("Error occurred during running script: %s", e)



async def write_to_file():
    while True:
        try:
            if skins:
                data_to_write = "\n".join(skins)
                with open("textFiles/bitskins.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_write + "\n")
                skins.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(2)
        except Exception as e:
            logging.error("Error occurred during writing data: %s", e)



async def main():
    while True:
        try:
            await asyncio.gather(connect(), write_to_file())
        except Exception as e:
            logging.error("Error occurred during starting script: %s", e)



asyncio.run(main())
