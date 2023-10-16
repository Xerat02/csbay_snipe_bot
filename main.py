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
import tools.module as tl
from datetime import datetime
from collections import deque



cfg = tl.cfg_load("config")

# que
message_queue = asyncio.Queue()
processed_messages = deque(maxlen=200)

# discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#database
pool = None


async def string_comp(name, price):
    try:
        name = str(name).lower().strip()
        risk = ""

        db_connection = await tl.get_db_conn(pool)
        cursor = await db_connection.cursor()

        sql = "SELECT * FROM buff_skins WHERE market_hash_name = %s LIMIT 1;"
        data = await tl.db_get_data(sql, cursor, None, name)

        for row in data:
            buff_id = row[0]
            buff_name = str(row[1]).strip()
            sell_price = row[2]
            buff_price = row[3]
            buy_num = row[4]
            sell_num = row[5]
            buff_update_time = row[6]

            buff_update_time = int(buff_update_time.timestamp())

            if buff_price == 0:
                buff_price = sell_price
                risk = 9999
            else:    
                risk = abs((((sell_price) - buff_price) / buff_price) * 100)            

            if name == buff_name.lower():
                num = float(buff_price)
                num = round(num, 2)
                price = float(price)
                price = round(price, 2)

                if price < num:
                    discount = ((num / price)-1) * 100
                    profit = ((num * 0.975) - price)
                    if discount > 0.5 and profit > 0.01:
                        buff_link = "https://buff.163.com/goods/" + str(buff_id)
                        return [round(discount, 2), num, round(profit, 2), buff_link, risk, buff_name, buff_update_time, sell_num, buff_id]        
        return None
    except Exception as e:
        tl.exceptions(e)
        return None
    finally:
        await tl.release_db_conn(cursor,db_connection,pool)



async def process_file(filename):
    temp_folder = cfg["main"]["temp_files_location"]
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    base_name = os.path.basename(filename)
    temp_filename = os.path.join(temp_folder, "temp_"+base_name)
    shutil.copy(filename, temp_filename)
    try:
        with open(temp_filename, "r", encoding="utf-8") as file:
            for row in file.read().split('\n'):
                row = str(row).split(";")
                if len(row) > 2:
                    info = row
                    if info[3] not in processed_messages:
                        discount = await string_comp(row[0], row[1])
                        if discount and discount[0]:
                            await message_queue.put((info, discount))
                            processed_messages.append(info[3])
                            print(info)
    except Exception as e:
        tl.exceptions(e)  
    finally:                          
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
            row = await message_queue.get()
            info = row[0]
            discount = row[1]
            try:
                await send_message(info, discount)
            except Exception as e:
                tl.exceptions(e)
            finally:
                message_queue.task_done()
        await asyncio.sleep(cfg["main"]["message_send_delay"])



async def update_statistics(market_name, discount, profit, message_url):
    db_connection = await tl.get_db_conn(pool)
    cursor = await db_connection.cursor()
    new_count = None  
    new_average = None  
    new_max_profit = None
    
    try:
        await db_connection.begin()
        
        sql = """SELECT snipe_count, average_discount, max_profit, msg_link
                   FROM snipe_statistics 
                   WHERE market_name = %s 
                   FOR UPDATE;"""
        data = await tl.db_get_data(sql, cursor, 1, market_name)

        #general snipe data
        if data:
            new_count = data[0] + 1
            new_average = float(((data[1] * data[0]) + discount) / new_count)
            new_average = round(new_average, 2)
            new_message_url = data[3]

            if data[2] is None:
                new_max_profit = profit
            else:
                if profit > data[2]:
                    new_max_profit = profit
                    new_message_url = message_url
                else:
                    new_max_profit = data[2]
            
            sql = "UPDATE snipe_statistics SET snipe_count = %s, average_discount = %s, max_profit = %s, msg_link = %s WHERE market_name = %s;"
            await tl.db_manipulate_data(sql, cursor, db_connection, False, new_count, new_average, new_max_profit, new_message_url, market_name)
        else:
            new_count = 1
            new_average = float(discount)
            new_max_profit = profit  
            
            sql = """INSERT INTO snipe_statistics (market_name, snipe_count, average_discount, max_profit, msg_link)
                       VALUES (%s, %s, %s, %s, %s);"""
            await tl.db_manipulate_data(sql, cursor, db_connection, False, market_name, new_count, new_average, new_max_profit, message_url)

        #time snipe data (1 min, 10min, 1h, 1d, 1w)
        for x in cfg["main"]["stats_time_frames"]:
            time = datetime.now()
            sql = """SELECT time_frame, market, potencial_profit, msg_link, discount, update_time
                    FROM snipe_time_stats
                    WHERE time_frame = %s
                    FOR UPDATE;"""
            time_frame_data = await tl.db_get_data(sql, cursor, 1, x)
            
            x = int(x)

            if time_frame_data:
                time_diff = time - time_frame_data[5]
                if time_diff.total_seconds() > x*60:
                    sql = "UPDATE snipe_time_stats SET market = %s, potencial_profit = %s, msg_link = %s, discount = %s, update_time = %s WHERE time_frame = %s;"
                    await tl.db_manipulate_data(sql, cursor, db_connection, False, market_name, profit, message_url, discount, time, x)

                    await asyncio.sleep(0.07)

                if time_frame_data[2] < profit:
                    sql = "UPDATE snipe_time_stats SET market = %s, potencial_profit = %s, msg_link = %s, discount = %s WHERE time_frame = %s;"
                    await tl.db_manipulate_data(sql, cursor, db_connection, False, market_name, profit, message_url, discount, x)
            else:
                sql = """INSERT INTO snipe_time_stats (time_frame, market, potencial_profit, msg_link, discount, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s);"""
                await tl.db_manipulate_data(sql, cursor, db_connection, False, x, market_name, profit, message_url, discount, time)        
        await db_connection.commit()
    except Exception as e:
        tl.exceptions(e)
        await db_connection.rollback()
    finally:
        await tl.release_db_conn(cursor, db_connection, pool)



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

    if stats_message is None:
        async for message in stats_channel.history(limit=10):
            if message.author == client.user:
                stats_message = message
                break

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
                        if x.endswith('0') or x.endswith('.'):
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
                    
                    embed.add_field(name=f"The best snipes in {time_frame}:", value=f"Market: {market}\nPotencial profit: ${potencial_profit} ([Jump]({msg_link}))\nDiscount: {discount}%", inline=False)

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



async def create_embed(info, discount):
    header = discount[5]
    risk = discount[4]
    try:
        if risk < cfg["main"]["risk_ranges"][0]:
            risk = "Low"
        elif risk < cfg["main"]["risk_ranges"][0]:
            risk = "Medium"
        elif risk < cfg["main"]["risk_ranges"][0]:
            risk = "High"
        else:
            risk = "Very High"
        risk = risk + " (" + str(discount[7]) + " on sale)"

        desc = f"**Risk:** `{risk}`\n**Market price:** ${round(float(info[1]),2)}\n**Buff price:** ${discount[1]}\n**Potencial profit:** ${discount[2]} (Buff fee included)\n**Discount:** {discount[0]}%\n\nBuff data was last updated <t:{discount[6]}:R>"

        embed = discord.Embed(title=header, description=desc, url=info[2])
        embed.set_thumbnail(url=info[3])
        embed.timestamp = datetime.utcnow()
        footer_text = info[4]
        embed.set_footer(text=footer_text, icon_url=cfg["main"]["icons_urls"].get(info[4], ""))
        return embed
    except Exception as e:
        tl.exceptions(e)



async def save_snipe_to_dtb(buff_id, price, discount, risk_factor, market_name, offer_link, img_link):
    try:
        release_datetime = datetime.now()
        db_connection = await tl.get_db_conn(pool) 
        cursor = await db_connection.cursor()
        sql = """INSERT INTO snipes (buff_id, price, discount, risk_factor, market_name, offer_link, img_link, release_datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        await tl.db_manipulate_data(sql, cursor, db_connection, True, buff_id, price, discount, risk_factor, market_name, offer_link, img_link, release_datetime)
    except Exception as e:
        tl.exceptions(e)
    finally:
        await tl.release_db_conn(cursor, db_connection, pool)   



async def send_message(info, discount):
    message = None
    message_url = None
    try:
        if not info or not discount:
            return
        
        channel = [client.get_channel(cfg["main"]["snipe_channels_id"][0]),client.get_channel(cfg["main"]["snipe_channels_id"][1]),client.get_channel(cfg["main"]["snipe_channels_id"][2]),client.get_channel(cfg["main"]["snipe_channels_id"][3])]
        embed = await create_embed(info, discount)

        market_button = discord.ui.Button(label="Check it",style=discord.ButtonStyle.url,url=info[2])
        buff_button = discord.ui.Button(label="Buff price",style=discord.ButtonStyle.url,url=discount[3])
        view = discord.ui.View()
        view.add_item(market_button)
        view.add_item(buff_button)

        price = float(info[1])

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

        if price > cfg["main"]["price_ranges"][2] and float(discount[4]) < 7 and float(discount[0]) >= 10 or float(discount[2]) > 5 :
            embed.colour = discord.Colour(cfg["main"]["message_colors"][3])
            message = await channel[3].send(embed=embed, view=view)
       
    except Exception as e:
        tl.exceptions(e)
        return
    finally:
        pass
        await update_statistics(info[4], discount[0], discount[2], message_url)
        await save_snipe_to_dtb(discount[8], float(info[1]), discount[1], discount[4], info[4], info[2], info[3])

async def currency_updater():
    while not client.is_closed():
        db_connection = await tl.get_db_conn(pool)
        cursor = await db_connection.cursor()
        token = cfg["main"]["currency_updater_token"]
        symbols = ["CNY", "RUB", "USD"]
        url = f"http://data.fixer.io/api/latest?access_key={token}&symbols="
        try:
            for i in range(0, len(symbols)):
                if i == (len(symbols) - 1):
                    url += symbols[i]
                else:
                    url += symbols[i] + ", "

            sql_select = "SELECT * FROM currency WHERE currency_name = %s;"
            sql_insert = """INSERT INTO currency (currency_name, value) VALUES (%s, %s);"""
            sql_update = """UPDATE currency SET value = %s WHERE currency_name = %s;"""

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    response_data = await response.json()
                    if response.status == 200 and response_data["success"]:
                        for symbol in symbols:
                            currency_value = response_data["rates"][symbol]
                            if currency_value is not None:
                                existing_currency = await tl.db_get_data(sql_select, cursor, 1, symbol)

                                if existing_currency:
                                    await tl.db_manipulate_data(sql_update, cursor, db_connection, True, currency_value, symbol)
                                else:
                                    await tl.db_manipulate_data(sql_insert, cursor, db_connection, True, symbol, currency_value)
        except Exception as e:
            tl.exceptions(e)  
        finally:
             await asyncio.sleep(cfg["main"]["currency_updater_delay"])   


@client.event
async def on_ready():
    global pool
    pool = await tl.set_db_conn()
    print(f'Logged on as {client.user}!')
    asyncio.gather(send_latest_offers(), send_message_worker(), send_statistics_embed())



@client.event
async def on_close():
    await tl.close_db_conn(pool)



client.run(cfg["main"]["discord_client_token"])