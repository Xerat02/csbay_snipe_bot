####################################
#
#
# This snipe bot is created by Xerat
#
#
####################################

import discord
import aiomysql
import aiohttp
import asyncio
import shutil
import os
import re
import tools.module as tl
from datetime import datetime, timedelta
from collections import deque
from pymongo import MongoClient, UpdateOne



cfg = tl.cfg_load("config")

# que
message_queue = asyncio.Queue()
processed_messages = deque(maxlen=1000)

# discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#database
pool = None

#mongoDB
mongo_client = MongoClient(cfg["mongoDB"]["uri"])
db = mongo_client["csbay"]


async def process_data(market_array):
    try:
        collection = db["buff_items"]

        for market_row in market_array:
            market_row = market_row.split(";")
            
            if len(market_row) > 1:
                market_risk_factor = ""
                market_skin_name = str(market_row[0])
                market_price = float(market_row[1])
                market_item_link = market_row[2].replace(" ", "%20")
                market_name = market_row[3]

                if market_item_link in processed_messages:
                    continue
                
                search_value = "".join(market_skin_name.split()).lower()
                buff_row = collection.find_one({"search_name": search_value})

                
                if buff_row:
                    buff_id = buff_row["_id"]
                    buff_skin_name = str(buff_row["market_hash_name"]).strip()
                    buff_sell_price = round(buff_row["price_in_usd"], 2)
                    buff_buy_price = round(buff_row["buy_max_price"], 2)
                    buff_item_buy_num = buff_row["buy_num"]
                    buff_item_sell_num = buff_row["sell_num"]
                    buff_item_image = buff_row["item_image"]
                    buff_data_update_time = int(buff_row["update_time"].timestamp())

                    if buff_buy_price <= 0 or buff_sell_price <= 0 or market_price <= 0:
                        continue
                    else:
                        buff_price = buff_sell_price if buff_sell_price != 0 else buff_buy_price

                        if buff_sell_price != 0 and buff_buy_price != 0:
                            price_diff = abs(buff_sell_price - buff_buy_price) / min(buff_sell_price, buff_buy_price)

                            if price_diff > 0.10:
                                buff_price = min(buff_sell_price, buff_buy_price)

                        market_risk_factor = abs((((buff_sell_price - buff_price) / buff_price) * 100))

                    market_price = round(market_price, 2)
                    if market_price < buff_price and buff_price > 0.5:
                        buff_discount = round(((buff_price / market_price) - 1) * 100, 2)
                        profit = [round(buff_price - market_price, 2),round((buff_price * 0.975) - market_price, 2)]

                        if buff_discount > 4 or profit[0] > 2:
                            buff_item_link = f"https://buff.163.com/goods/{buff_id}"
                            processed_item = [
                                buff_id, buff_skin_name, market_skin_name, market_name, buff_price, market_price,
                                buff_discount, market_risk_factor, profit, buff_item_buy_num, buff_item_sell_num,
                                buff_item_link, market_item_link, buff_item_image, buff_data_update_time
                            ]
                            await message_queue.put(processed_item)
                            processed_messages.append(processed_item[12])
                            print(processed_item)
                else:
                    print("Not found!")
                    print("-------------")
                    print(buff_row)
                    print(market_skin_name)  
                    print(search_value)
                    print(market_name)  
                    print("-------------")              
    except Exception as e:
        tl.exceptions(e)



async def process_file(filename):
    temp_folder = cfg["main"]["temp_files_location"]
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    base_name = os.path.basename(filename)
    temp_filename = os.path.join(temp_folder, "temp_"+base_name)
    shutil.copy(filename, temp_filename)
    try:
        with open(temp_filename, "r", encoding="utf-8") as file:
            item_array = file.read().split("\n")
            if len(item_array) > 0:
                if item_array[0] != "":
                    await process_data(item_array) #send array to process_data function        
    except Exception as e:
        tl.exceptions(e)  
    finally:               
        with open(filename,"w") as file:
            pass        
        os.remove(temp_filename)                    



async def send_latest_offers():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            tasks = [process_file("textFiles/"+filename) for filename in cfg["main"]["files"]]            
            await asyncio.gather(*tasks)            
            await asyncio.sleep(cfg["main"]["offers_check_delay"])            
        except Exception as e:
            tl.exceptions(e)



async def send_message_worker():
    while True:
        if not message_queue.empty():
            try:
                await send_message(await message_queue.get())
            except Exception as e:
                tl.exceptions(e)
            finally:
                message_queue.task_done()
        await asyncio.sleep(cfg["main"]["message_send_delay"])



async def update_statistics(market_name, discount, profit, message_url):
    collection = db["snipe_statistic"]
    new_count = None  
    new_average = None  
    new_max_profit = None
    
    try:
        data = collection.find_one({"_id": market_name})

        #general snipe data
        if data:
            old_count = data.get("count", 1) 
            old_average = data.get("average", 0)   
            old_potencial_profit = data.get("potencial_profit")

            new_count = old_count + 1
            new_average = float(((old_average * old_count) + discount) / new_count)
            new_average = round(new_average, 2)
            new_message_url = data.get("message_url")

            if old_potencial_profit == None:
                new_max_profit = profit[0]
            else:
                if profit[0] > old_potencial_profit:
                    new_max_profit = profit[0]
                    new_message_url = message_url
                else:
                    new_max_profit = old_potencial_profit


            collection.update_one(
                {"_id": market_name},
                {
                    "$set": {
                                "count": new_count,
                                "average": new_average,
                                "max_profit": new_max_profit,
                                "message_url": new_message_url,
                                "update_time": datetime.now(),
                            }
                },
                upsert=True
            )

            last_hour_count = data.get("last_hour_count", data.get("count"))
            last_hour_update_time = data.get("last_hour_update_time")

            if abs(datetime.now() - last_hour_update_time) > timedelta(hours=1):
                collection.update_one(
                    {"_id": symbol},
                    {
                        "$set": {
                                    "last_hour_count": data.get("count") - last_hour_count,
                                    "last_hour_update_time": datetime.now()
                                }
                    },
                    upsert=True
                )    
        else:
            new_count = 1
            new_average = float(discount)
            new_max_profit = profit[0]  

            collection.update_one(
                {"_id": market_name},
                {
                    "$set": {
                                "count": new_count,
                                "last_hour_count": new_count,
                                "average": new_average,
                                "max_profit": new_max_profit,
                                "message_url": message_url,
                                "update_time": datetime.now(),
                                "last_hour_update_time": datetime.now()
                            }
                },
                upsert=True
            )



        #time snipe data (1 min, 10min, 1h, 1d, 1w)
        for x in cfg["main"]["stats_time_frames"]:
            time = datetime.now()
            time_frame_data = collection.find_one({"_id": x})
            
            x = int(x)

            if time_frame_data:
                time_diff = time - time_frame_data.get("update_time")
                if time_diff.total_seconds() > x*60:
                    collection.update_one(
                        {"_id": x},
                        {
                            "$set": {
                                        "market": market_name,
                                        "potencial_profit": profit[0],
                                        "message_url": message_url,
                                        "discount": discount,
                                        "update_time": time,
                                    }
                        },
                        upsert=True
                    )

                    await asyncio.sleep(0.07)

                if time_frame_data.get("potencial_profit", 0) < profit[0]:
                    collection.update_one(
                        {"_id": x},
                        {
                            "$set": {
                                        "market": market_name,
                                        "potencial_profit": profit[0],
                                        "message_url": message_url,
                                        "discount": discount,
                                    }
                        },
                        upsert=True
                    )
            else:
                collection.update_one(
                        {"_id": x},
                        {
                            "$set": {
                                        "market": market_name,
                                        "potencial_profit": profit[0],
                                        "message_url": message_url,
                                        "discount": discount,
                                        "update_time": time,
                                    }
                        },
                        upsert=True
                )   
    except Exception as e:
        tl.exceptions(e)



async def find_existing_message(channel, target_title):
    try:
        async for message in channel.history(limit=100):
            for embed in message.embeds:
                if embed.title == target_title:
                    return message
        return None
    except Exception as e:
        tl.exceptions(e)




async def send_statistics_embed():
    stats_channel = client.get_channel(cfg["main"]["stat_channels_id"][0])
    stats_message = await find_existing_message(stats_channel, "Market Statistics")

    while not client.is_closed():
        db_connection = await tl.get_db_conn(pool)
        cursor = await db_connection.cursor()

        try:
            sql = """SELECT market_name, snipe_count, average_discount, max_profit, msg_link
                       FROM snipe_statistics
                       ORDER BY snipe_count DESC;"""
            data = await tl.db_get_data(sql, cursor, None)

            sql = """SELECT time_frame, market, potencial_profit, msg_link, discount
            FROM snipe_time_stats
            ORDER BY time_frame ASC;"""
            time_frame_data = await tl.db_get_data(sql, cursor, None)

            if data and time_frame_data:
                embed = discord.Embed(title="Market Statistics", description="Here are the latest stats:", color=discord.Color.blue())

                for row in data:
                    market_name, snipe_count, average_discount, max_profit, msg_link = row
                    embed.add_field(name=f"{market_name}", value=f"📚 Snipe Count: {snipe_count}\n🔖 Average Discount: {average_discount}%\n💵 Max recorded profit: ${max_profit} ([Jump]({msg_link}))", inline=False)

                embed.add_field(name="",value="")
                
                def remove_trailing_zeros(x):
                    if "." in x:
                        if x.endswith("0") or x.endswith("."):
                            return(remove_trailing_zeros(x[:-1]))
                    else:
                        return(x)
                       
                    
                for row in time_frame_data:
                    time_frame, market, potencial_profit, msg_link, discount = row

                    x = 0    
                    if time_frame < 60:
                        x = time_frame
                        time_frame = remove_trailing_zeros(str(x)) + " min"
                    elif time_frame / 60 < 24:
                        x = time_frame / 60
                        time_frame = remove_trailing_zeros(str(x)) + " h" 
                    elif time_frame / 1440 < 7:
                        x = time_frame / 1440
                        time_frame = remove_trailing_zeros(str(x)) + " d"
                    elif time_frame / 10080 < 5:
                        x = time_frame / 10080
                        time_frame = remove_trailing_zeros(str(x)) + " w"     
                    
                    embed.add_field(name=f"The best snipe in {time_frame}:", value=f"Market: {market}\nPotencial profit: ${potencial_profit} ([Jump]({msg_link}))\nDiscount: {discount}%", inline=False)

                embed.set_footer(text=f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

                if stats_message:  
                    await stats_message.edit(embed=embed)
                else:
                    stats_message = await stats_channel.send(embed=embed)  

        except Exception as e:
            tl.exceptions(e)

        finally:
            await tl.release_db_conn(cursor, db_connection, pool)

        await asyncio.sleep(cfg["main"]["statistic_message_update_delay"])



async def create_embed(data):
    header = data[1]
    risk = data[7]
    try:
        if risk < cfg["main"]["risk_ranges"][0]:
            risk = "Low"
        elif risk < cfg["main"]["risk_ranges"][0]:
            risk = "Medium"
        elif risk < cfg["main"]["risk_ranges"][0]:
            risk = "High"
        else:
            risk = "Very High"
        risk = risk + " (" + str(data[10]) + " on sale)"

        desc = f"**Risk:** `{risk}`\n**Market price:** ${data[5]}\n**Buff price:** ${data[4]}\n**Potencial profit:** ${data[8][0]} / ${data[8][1]} (With buff fees) \n**Discount:** {data[6]}% ({round(100-data[6], 2)}% Buff) \n\nBuff data was last updated <t:{data[14]}:R>"

        embed = discord.Embed(title=header, description=desc, url=data[12])
        embed.set_thumbnail(url=data[13])
        embed.timestamp = datetime.utcnow()
        footer_text = data[3]
        embed.set_footer(text=footer_text, icon_url=cfg["main"]["icons_urls"].get(data[3], ""))
        return embed
    except Exception as e:
        tl.exceptions(e)



async def save_snipe_to_dtb(buff_id, price, discount, risk_factor, market_name, offer_link):
    try:
        release_datetime = datetime.now()
        db_connection = await tl.get_db_conn(pool) 
        cursor = await db_connection.cursor()
        sql = """INSERT INTO snipes (buff_id, price, discount, risk_factor, market_name, offer_link, release_datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        await tl.db_manipulate_data(sql, cursor, db_connection, True, buff_id, price, discount, risk_factor, market_name, offer_link, release_datetime)
    except Exception as e:
        tl.exceptions(e)
    finally:
        await tl.release_db_conn(cursor, db_connection, pool)   



async def send_message(data):
    message = None
    message_url = None
    try:
        if not data:
            return
        
        channel = [client.get_channel(cfg["main"]["snipe_channels_id"][0]),client.get_channel(cfg["main"]["snipe_channels_id"][1]),client.get_channel(cfg["main"]["snipe_channels_id"][2]),client.get_channel(cfg["main"]["snipe_channels_id"][3])]
        embed = await create_embed(data)

        market_button = discord.ui.Button(label="Check it",style=discord.ButtonStyle.url,url=data[12])
        buff_button = discord.ui.Button(label="Buff price",style=discord.ButtonStyle.url,url=data[11])
        view = discord.ui.View()
        view.add_item(market_button)
        view.add_item(buff_button)

        price = data[5]

        if price <= cfg["main"]["price_ranges"][0]:
            embed.colour = discord.Colour(cfg["main"]["message_colors"][0])
            message = await channel[0].send(embed=embed, view=view)
        elif price < cfg["main"]["price_ranges"][1]:
            embed.colour = discord.Colour(cfg["main"]["message_colors"][1])
            message = await channel[1].send(embed=embed, view=view)
        else:     
            embed.colour = discord.Colour(cfg["main"]["message_colors"][2])
            message = await channel[2].send(embed=embed, view=view)

        message_url = message.jump_url

        if price > cfg["main"]["price_ranges"][2] and data[7] < 7 and data[6] >= 10 or data[8][1] > 5 :
            embed.colour = discord.Colour(cfg["main"]["message_colors"][3])
            message = await channel[3].send(embed=embed, view=view)
       
    except Exception as e:
        tl.exceptions(e)
        return
    finally:
        await update_statistics(data[3], data[6], data[8], message_url)
        await save_snipe_to_dtb(data[0], data[5], data[6], data[7], data[3], data[12])




#functions that will get latest currency rates
async def currency_updater():
    while not client.is_closed():
        collection = db["currency"]

        token = cfg["main"]["currency_updater_token"]
        symbols = ["CNY", "RUB", "USD"]
        url = f"http://data.fixer.io/api/latest?access_key={token}&symbols="
        update = False
        try:
            for i in range(0, len(symbols)):
                if i == (len(symbols) - 1):
                    url += symbols[i]
                else:
                    url += symbols[i] + ", "

            for symbol in symbols:
                update_time = collection.find_one({"_id": symbol}).get("update_time")
                if update_time == None or abs(datetime.now() - update_time) > timedelta(days=1):
                   update = True

            if update:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=30) as response:
                        response_data = await response.json()
                        if response.status == 200 and response_data["success"]:
                            for symbol in symbols:
                                currency_value = response_data["rates"][symbol]
                                if currency_value != None:
                                    collection.update_one(
                                        {"_id": symbol},
                                        {
                                            "$set": {
                                                "value": currency_value,
                                                "update_time": datetime.now()
                                            }
                                        },
                                        upsert=True
                                    )

        except Exception as e:
            tl.exceptions(e)  
        finally:
             await asyncio.sleep(cfg["main"]["currency_updater_delay"])   



#main discord run function
@client.event
async def on_ready():
    global pool
    pool = await tl.set_db_conn()
    print(f"Logged on as {client.user}!")
    await asyncio.gather(send_latest_offers(), send_message_worker(), send_statistics_embed(), currency_updater())



@client.event
async def on_close():
    await tl.close_db_conn(pool)



client.run(cfg["main"]["discord_client_token"])