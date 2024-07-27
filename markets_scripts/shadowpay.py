import asyncio
import json
import websockets
import logging
import tools.module as tl



items = []
cur_rate = 0



async def start():
    async with websockets.connect('wss://ws.shadowpay.com/connection/websocket?token=fcc02e347f409e8f9a3314c358009108') as websocket:
        auth_message = json.dumps({
            "params": {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI3NjU2MTE5ODI1MDQzMTg0MiIsImNoYW5uZWxzIjpbIm9mZmVycyM3NjU2MTE5ODI1MDQzMTg0MiIsIm9mZmVycyJdfQ.Zg40ca0R_kSmizJ0-nW62F062ldxcBBNGpf0K_7we88"},
            "id": 1
        })
        await websocket.send(auth_message)
        
        while True:
            try:
                response = await websocket.recv()
                
                responses = response.split('\n')
                for resp in responses:
                    if resp.strip():
                        try:
                            parsed_data = json.loads(resp)

                            if ("result" in parsed_data and
                                "data" in parsed_data["result"] and
                                "data" in parsed_data["result"]["data"] and
                                "offers" in parsed_data["result"]["data"]["data"]):

                                offers = parsed_data["result"]["data"]["data"]["offers"]
                                for obj in offers:
                                    name = str(obj["steam_market_hash_name"])
                                    price = str(float(obj["price"]) * 1.05157)
                                    link = f"https://shadowpay.com/item/{obj['id']}"
                                    items.append(f"{name};{price};{link};Shadowpay")
                        except json.JSONDecodeError as e:
                            logging.error(f"JSON decode error: {e}")
            except websockets.exceptions.ConnectionClosed as e:
                tl.exceptions(e)
                break
            except Exception as e:
                logging.error(f"An error occurred: {e}")



async def write_to_file():
    while True:
        try:
            if items:
                data_to_write = "\n".join(items)
                with open("textFiles/shadowpay.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_write + "\n")
                items.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(1)
        except Exception as e:
            logging.error("Error occurred during writing data: %s", e)



async def main():
    while True:
        try:
            await asyncio.gather(start(), write_to_file())
        except Exception as e:
            logging.error("Error occurred during starting script: %s", e)


asyncio.run(main())
