import socketio
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s')
items = []
sio = socketio.AsyncClient(ssl_verify=True)

@sio.on('add_item')
async def on_add_item(data):
    try:
        name = str(data['name'])
        link_name = name.lower().replace("★","").replace("™","").replace("(","").replace(")","").replace(" ","-")
        price = str(round((float(data['price'])/1000),2))
        if "★" in name:
            link_name = link_name[1:]
        link = "https://waxpeer.com/"+link_name+"/item/"+str(data['item_id'])
        image = data['image']
        items.append(f"{name};{price};{link};{image};Waxpeer")
    except Exception as e:
        logging.error("Error occurred during getting data: %s", e)
        await sio.disconnect()

async def write_to_file():
    while True:
        try:
            if items:
                data_to_write = "\n".join(items)
                with open("textFiles/waxpeer.txt", "w", encoding="utf-8") as file:
                    file.write(data_to_write + "\n")
                items.clear()
                logging.debug("Data successfully written to the file.")
            await asyncio.sleep(2)
        except Exception as e:
            logging.error("Error occurred during writing data: %s", e)

async def ping_server():
    while True:
        if sio.connected:
            await sio.emit('name','ping')
        await asyncio.sleep(20)

async def start(sub):
    try:
        await sio.connect(
            'https://waxpeer.com',
            transports=['websocket'],
            socketio_path='/socket.io/',
            headers={'authorization': 'b268a096e46fc9f21a072c01936e7e0c9b3686b82bf9292e4167d2c207204292'}
        )
        for sub in sub_events:
            await sio.emit('sub', {'name': sub, 'value': True})
        await sio.wait()
    except Exception as e:
        logging.error("Error occurred during starting websocket: %s", e)

async def main(sub_events):
    while True:
        try:
            await asyncio.gather(start(sub_events), write_to_file(), ping_server())
        except Exception as e:
            logging.error("Error occurred during starting script: %s", e)

sub_events = ["add_item"]
asyncio.run(main(sub_events))