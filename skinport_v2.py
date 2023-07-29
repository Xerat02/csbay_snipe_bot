import socketio
import asyncio



sio = socketio.AsyncClient(ssl_verify=False)
skins = []



@sio.on('saleFeed')
async def on_sale_feed(result):
    name = result["sales"][0]["title"] + " " + result["sales"][0]["name"]
    if "Container" in name:
        name = result["sales"][0]["name"]
    name = str(name).replace("|", "").replace("  ", " ")
    wear = result["sales"][0]["exterior"]
    if wear is None:
        wear = ""
    else:
        wear = "(" + wear + ")"
    price = str(result["sales"][0]["salePrice"] / 100)
    link = "https://skinport.com/item/" + result["sales"][0]["url"] + "/" + str(result["sales"][0]["saleId"])
    image = "https://community.cloudflare.steamstatic.com/economy/image/" + str(result["sales"][0]["image"])

    skins.append(name + ";" + wear + ";" + price + ";" + link + ";" + image + ";Skinport")
    #print(name + ";" + wear + ";" + price + ";" + link + ";" + image + ";Skinport")



async def write_to_file():
    while True:
        await asyncio.sleep(4)  
        if skins:
            data_to_write = "\n".join(skins)
            with open("skinport.txt", "w", encoding="utf-8") as file:
                file.write(data_to_write + "\n")
            skins.clear()



async def start():
    await sio.connect('https://skinport.com', transports=['websocket'])
    await sio.emit('auth', {'token': 'p5SLeHLC1EEIbdKgnVe/CISCdYVtlCvJTh8G+yphc5iXvOignneadkGkI6Oqf3OPu0zZW8tFvCh3sFen9JK9bA=='})
    await sio.emit('saleFeedJoin', {'currency': 'USD', 'locale': 'en', 'appid': 730})



async def main():
    await asyncio.gather(start(), write_to_file())



asyncio.run(main())
