import asyncio
import json
import aiohttp
import websockets
import logging 

items = []

async def ping_server(websocket):
    while True:
        
        try:
            await websocket.send('ping')
        except websockets.exceptions.ConnectionClosed:
            break
        finally:
            await asyncio.sleep(20)

async def start():
    async with websockets.connect('wss://wsn.dota2.net/wsn/') as websocket:
        await websocket.send("newitems_go")
        asyncio.create_task(ping_server(websocket))
        while True:
            try:
                response = await websocket.recv()
                if response != "pong":
                    parsed_data = json.loads(response)
                    inner_data = json.loads(parsed_data['data'])

                    name = str(inner_data['i_market_hash_name']).replace("|","").replace("  "," ")
                    price = inner_data["ui_price"]
                    link = "https://market.csgo.com/en/Agent/"+inner_data['i_market_hash_name']+"?id="+inner_data['ui_id']
                    image = "https://cdn2.csgo.com/item/image/width=458/"+inner_data['i_market_hash_name']+".webp"
                    items.append(f"{name};{price};{link};{image};Marketcsgo")
            except websockets.exceptions.ConnectionClosed:
                print("Connection with server closed")
                break

async def write_to_file():
    while True:
        try:
            if items:
                data_to_write = "\n".join(items)
                with open("marketcsgo.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_write + "\n")
                items.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(2)
        except Exception as e:
            logging.error("Error occurred during writing data: %s", e)

async def main():
    while True:
        try:
            await asyncio.gather(start(),write_to_file())
        except Exception as e:
            logging.error("Error occurred during starting script: %s", e)

asyncio.run(main())
