import discord
from datetime import datetime
import jellyfish
import os
import pandas as pd
import asyncio
import queue


#que
queue = asyncio.Queue()

#discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#modifikace souboru
last_modified_skinport = None
#last_modified_dmarket = os.stat("new_skins.txt").st_mtime
#last_modified_bitskins = os.stat("new_skins.txt").st_mtime

async def string_comp(name, wear, price):
    try:
        df = pd.read_csv('demo.csv', delimiter=';', header=None, names=['col1', 'col2', 'col3'], encoding='utf-8')

        buff_skin_name = df['col2'].str.strip().str.replace("|", "").str.replace("  ", " ").str.lower()
        if wear != "":
            comp_name = (str(name).strip().lower() + " " + str(wear).strip().lower())
        else:
            comp_name = (str(name).strip().lower())
        similarity = buff_skin_name.apply(lambda x: jellyfish.jaro_winkler_similarity(comp_name, x))
        idx = (similarity > 0.98).idxmax()

        if similarity[idx] > 0.98:
            num = float(df.loc[idx, 'col3'])
            buffprice = num / 6.91
            price = float(price)

            if price < num / 6.91:
                discount = (((num / 6.91) - price) / price) * 100
                return [round(discount), round(buffprice, 2)]
        else:
            return [-1, 0]

    except:
        print()
        return ["err", "err"]
    



async def send_latest_offers(last_modified_skinport):
    await client.wait_until_ready()
    while not client.is_closed():
        try: 

            #skinport
            current_modified_skinport = os.stat("skinport.txt").st_mtime
            if current_modified_skinport != last_modified_skinport:
                print(last_modified_skinport)
                print(current_modified_skinport)
                last_modified_skinport = current_modified_skinport
                with open("skinport.txt", "r", encoding="utf-8") as skinport:
                    for skinport_row in skinport:
                        skinport_row = skinport_row.split(";")
                        info = skinport_row
                        discount = await string_comp(skinport_row[0], skinport_row[1], skinport_row[2])
                        await queue.put((info, discount))
                        await asyncio.sleep(1.2)   
        except:
            pass 




async def send_message_worker():
    while True:
        row = await queue.get()
        info = row[0]
        discount = row[1]
        print(info)
        print(discount)
        try:
            await send_message(info, discount)
            await asyncio.sleep(2.2) 
        except Exception as e:
            pass
        finally:
            queue.task_done()



async def send_message(info,discount):
       channel = [client.get_channel(818598365490708521),client.get_channel(818598365490708522),client.get_channel(818598365490708523)]
       desc = "**Wear: **"+info[1]+"\n"+"**Market price: **$"+str(round(float(info[2]),2))+"\n**Buff price: **$"+str(discount[1])+"**\nDiscount: **"+str(discount[0])+"%"+"**\nMarket: **"+info[5]       
       embed = discord.Embed(title=info[0], description=desc, url=info[3])
       embed.set_thumbnail(url=info[4])
       if str(discount[0]) != "-1" and str(discount[0]) != "err":
        if float(info[2]) <= 10:
            await channel[0].send(embed=embed)
        elif float(info[2]) < 100 :
            await channel[1].send(embed=embed)
        else:     
            await channel[2].send(embed=embed)



@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    client.loop.create_task(send_latest_offers(last_modified_skinport))
    asyncio.create_task(send_message_worker())



client.run('ODI4MjMwMDEwMzEzNjM3ODg4.G-AnRQ.z_VCpQ1DRjNIMkYT8bClUKrI7qMY7BJkjVSHv8')