import discord
import mysql.connector
import asyncio
from collections import deque


#que
message_queue = asyncio.Queue()
processed_messages = deque(maxlen=200)

#discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def string_comp(name, wear, price):
    try:
        name = str(name).lower()
        wear = str(wear).lower()

        db_connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='user',
            password='Buldozer4563',
            database='csbay'
        )
        if wear:
            comp_name = (name + " " + wear).strip()
        else:
            comp_name = name
        
        query = "SELECT id, market_hash_name, price_in_usd FROM buff_skins WHERE market_hash_name = %s LIMIT 1;"
        cursor = db_connection.cursor()
        cursor.execute(query, (comp_name,))
        data = cursor.fetchall()
        cursor.close()
        db_connection.close()

        for row in data:
            buff_id = row[0]
            buff_name = str(row[1]).lower().strip()
            buff_price = row[2]

            

            if comp_name == buff_name:
                num = float(buff_price)
                price = float(price)

                #print("comp_name: "+comp_name)
                #print("buff_name: "+buff_name)
                 

                if price < num:
                    #print("comp_price: "+str(price)) 
                    #print("buff_price: "+str(num))

                    discount = (((num) - price) / price) * 100
                    profit = ((num * 0.975) - price)
                    if discount > 1 and profit > 0.1:
                        buff_link = "https://buff.163.com/goods/" + str(buff_id)
                        return [round(discount, 1), round(num, 2), round(profit, 2), buff_link]
                    else:
                        return None
    except Exception as e:
        print("Error:", e)
        return None


async def send_latest_offers():
    await client.wait_until_ready()
    while not client.is_closed():
        try: 

            #skinport
            with open("skinport.txt", "r", encoding="utf-8") as skinport:
                for skinport_row in skinport.read().split('\n'):
                    skinport_row = str(skinport_row).split(";")
                    if len(skinport_row) > 2:
                        info = skinport_row
                        if info[3] not in processed_messages:
                            if float(skinport_row[2]) > 0.3:
                                discount = await string_comp(skinport_row[0], skinport_row[1], skinport_row[2])
                                if discount is not None and discount[0] != None:
                                        await message_queue.put((info, discount))
                                        processed_messages.append(info[3])  
                                        print(info)

            await asyncio.sleep(0.1)
            
            #dmarket
            with open("dmarket.txt", "r", encoding="utf-8") as dmarket:
                for dmarket_row in dmarket.read().split('\n'):
                    dmarket_row = str(dmarket_row).split(";")
                    if len(dmarket_row) > 2:
                        info = dmarket_row
                        if info[3] not in processed_messages:
                            if float(dmarket_row[2]) > 0.3:
                                discount = await string_comp(dmarket_row[0],dmarket_row[1],dmarket_row[2])
                                if discount is not None and discount[0] != None:                           
                                        await message_queue.put((info, discount))  
                                        processed_messages.append(info[3])
                                        print(info)                    
    
            await asyncio.sleep(0.1)

            #skinbaron
            with open("skinbaron.txt", "r", encoding="utf-8") as skinbaron:
                for skinbaron_row in skinbaron.read().split('\n'):
                    skinbaron_row = str(skinbaron_row).split(";")
                    if len(skinbaron_row) > 2:
                        info = skinbaron_row
                        if info[3] not in processed_messages:
                            if float(skinbaron_row[2]) > 0.3:
                                discount = await string_comp(skinbaron_row[0],skinbaron_row[1],skinbaron_row[2])
                                if discount is not None and discount[0] != None:                            
                                        await message_queue.put((info, discount))  
                                        processed_messages.append(info[3])
                                        print(info)  
                      
        except Exception as e:
            print("send_latest_offers: ",e)



async def send_message_worker():
    while True:
        if not message_queue.empty():
                row = await message_queue.get()
                info = row[0]
                discount = row[1]
                try:
                    await send_message(info, discount)
                except Exception as e:
                    print("send_message_worker: ", e)
                finally:
                    message_queue.task_done()
        await asyncio.sleep(0.4)



async def send_message(info,discount):
    try:
        if not info or not discount:
            return
        
        channel = [client.get_channel(1104867182871056455),client.get_channel(1104867279512023190),client.get_channel(1104867324730818570)]
        desc = "**Wear: **"+info[1]+"\n"+"**Market price: **$"+str(round(float(info[2]),2))+"\n**Buff price: **$"+str(discount[1])+"**\nPotencial profit: **$"+str(discount[2])+" (Buff fee included)**\nDiscount: **"+str(discount[0])+"%"       
        embed = discord.Embed(title=info[0], description=desc, url=info[3])
        embed.set_thumbnail(url=info[4])

        if info[5] == "Skinport":
            icon_url = "https://i.imgur.com/NH7KSXK.png"
        elif info[5] == "Dmarket":
            icon_url = "https://i.imgur.com/fs5rPrI.png"
        elif info[5] == "SkinBaron":
            icon_url = "https://i.imgur.com/iYBDKfj.png"

        embed.set_footer(text=info[5],icon_url= icon_url)

        market_button = discord.ui.Button(label="Check it",style=discord.ButtonStyle.url,url=info[3])
        buff_button = discord.ui.Button(label="Buff price",style=discord.ButtonStyle.url,url=discount[3])
        view = discord.ui.View()
        view.add_item(market_button)
        view.add_item(buff_button)

        if float(info[2]) <= 10:
            embed.colour = discord.Colour(65482)
            await channel[0].send(embed=embed, view=view)
        elif float(info[2]) < 100 :
            embed.colour = discord.Colour(376795)
            await channel[1].send(embed=embed, view=view)
        else:     
            embed.colour = discord.Colour(6047388)
            await channel[2].send(embed=embed, view=view)
    except Exception as e:
        print("send_message: ",e)
        return




@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    client.loop.create_task(send_latest_offers())
    asyncio.create_task(send_message_worker())



client.run('MTEwNDg3MTkxNjk0MDA1MDU0Mg.Gxl-Dj.pzbOzxaVKWQkmR6-oTYvinsa0T3bT7xpMdsyDo')