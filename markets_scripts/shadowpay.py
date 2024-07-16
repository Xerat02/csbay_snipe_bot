import asyncio
import json
import websockets
import logging
import tools.module as tl



items = []
cur_rate = 0



async def start():
    async with websockets.connect('wss://ws.shadowpay.com/connection/websocket?token=fcc02e347f409e8f9a3314c358009108') as websocket:
        auth_message = json.dumps({"params": {"token": "fcc02e347f409e8f9a3314c358009108"}, "id": 1})
        await websocket.send(auth_message)
        while True:
            try:
                response = await websocket.recv()
                #if response != "pong":
                #    parsed_data = json.loads(response)
                #    inner_data = json.loads(parsed_data['data'])
#
                #    name = str(inner_data['i_market_hash_name'])
                #    price = str(round(((float(inner_data["ui_price"]))*cur_rate),3))
                #    market_hash_name = str(inner_data["i_market_hash_name"]).replace(" ","%20")
                #    link = "https://market.csgo.com/en/Agent/"+market_hash_name+"?id="+inner_data['ui_id']
                #    items.append(f"{name};{price};{link};Marketcsgo")
            except websockets.exceptions.ConnectionClosed as e:
                print("Connection with server closed", e)
                break



async def write_to_file():
    while True:
        try:
            if items:
                data_to_write = "\n".join(items)
                with open("textFiles/marketcsgo.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_write + "\n")
                items.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(1)
        except Exception as e:
            logging.error("Error occurred during writing data: %s", e)



async def main():
    while True:
        try:
            await asyncio.gather(start())
        except Exception as e:
            logging.error("Error occurred during starting script: %s", e)

asyncio.run(main())
