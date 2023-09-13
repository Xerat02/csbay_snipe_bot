import discord
import aiomysql
import asyncio
import shutil
import os
import json
from datetime import datetime
from collections import deque


cfg = json.load(open("configs/config.json"))

# que
message_queue = asyncio.Queue()
processed_messages = deque(maxlen=200)

# discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#database
pool = None


async def get_db_connection():
    return await pool.acquire()


async def close_pool():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()


async def string_comp(name, price):
    try:
        name = str(name).lower().strip()
        risk = ""

        db_connection = await get_db_connection()
        cursor = await db_connection.cursor()

        query = "SELECT * FROM buff_skins WHERE market_hash_name = %s LIMIT 1;"
        await cursor.execute(query, (name,))
        data = await cursor.fetchall()

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
                        await cursor.close()
                        db_connection.close()
                        return [round(discount, 2), num, round(profit, 2), buff_link, risk, buff_name, buff_update_time, sell_num]        
        return None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        if cursor:
            await cursor.close()
        if db_connection:
            pool.release(db_connection)


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
        print("process_file: "+e)  
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
            print("send_latest_offers: ", e)



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
        await asyncio.sleep(cfg["main"]["message_send_delay"])


async def update_statistics(market_name, discount, profit):
    db_connection = await get_db_connection() 
    cursor = await db_connection.cursor()
    new_count = None  
    new_average = None  
    new_max_profit = None

    try:
        await db_connection.begin()
        
        query = """SELECT snipe_count, average_discount, max_profit
                   FROM snipe_statistics 
                   WHERE market_name = %s 
                   FOR UPDATE;"""
        await cursor.execute(query, (market_name,))
        data = await cursor.fetchone()

        if data:
            new_count = data[0] + 1
            new_average = float(((data[1] * data[0]) + discount) / new_count)
            new_average = round(new_average, 2)
            
            if data[2] is None:
                new_max_profit = profit
            else:
                new_max_profit = max(data[2], profit)    
            
            query = "UPDATE snipe_statistics SET snipe_count = %s, average_discount = %s, max_profit = %s WHERE market_name = %s;"
            await cursor.execute(query, (new_count, new_average, new_max_profit, market_name))
        else:
            new_count = 1
            new_average = float(discount)
            new_max_profit = profit  
            
            query = """INSERT INTO snipe_statistics (market_name, snipe_count, average_discount, max_profit)
                       VALUES (%s, %s, %s, %s);"""
            await cursor.execute(query, (market_name, new_count, new_average, new_max_profit))
        
        await db_connection.commit()
    except Exception as e:
        print(f"update_statistics:  {e}, Attempted value for average_discount: {new_average}")
        await db_connection.rollback()
    finally:
        await cursor.close()
        pool.release(db_connection)


async def find_existing_message(channel, target_title):
    try:
        async for message in channel.history(limit=100):
            for embed in message.embeds:
                if embed.title == target_title:
                    return message
        return None
    except Exception as e:
        print("find_existing_message: ",e)


async def send_statistics_embed():
    stats_channel = client.get_channel(cfg["main"]["stat_channels_id"][0])
    stats_message = await find_existing_message(stats_channel, "Market Statistics")

    if stats_message is None:
        async for message in stats_channel.history(limit=10):
            if message.author == client.user:
                stats_message = message
                break

    while not client.is_closed():
        db_connection = await get_db_connection()
        cursor = await db_connection.cursor()

        try:
            query = """SELECT market_name, snipe_count, average_discount, max_profit
                       FROM snipe_statistics
                       ORDER BY snipe_count DESC;"""
            await cursor.execute(query)
            data = await cursor.fetchall()

            if data:
                embed = discord.Embed(title="Market Statistics", description="Here are the latest stats:", color=discord.Color.blue())

                for row in data:
                    market_name, snipe_count, average_discount, max_profit = row
                    embed.add_field(name=f"{market_name}", value=f"Snipe Count: {snipe_count}\nAverage Discount: {average_discount}%\nMax recorded profit: ${max_profit}", inline=False)

                embed.set_footer(text=f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

                if stats_message:
                    await stats_message.edit(embed=embed)
                else:
                    stats_message = await stats_channel.send(embed=embed)

        except Exception as e:
            print(f"Error in send_statistics_embed: {e}")

        finally:
            await cursor.close()
            pool.release(db_connection)

        await asyncio.sleep(10)


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
        print("create_embed: ",e)


async def send_message(info,discount):
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
            await channel[0].send(embed=embed, view=view)
        elif price < cfg["main"]["price_ranges"][1]:
            embed.colour = discord.Colour(cfg["main"]["message_colors"][1])
            await channel[1].send(embed=embed, view=view)
        else:     
            embed.colour = discord.Colour(cfg["main"]["message_colors"][2])
            await channel[2].send(embed=embed, view=view)

        if price > cfg["main"]["price_ranges"][2] and float(discount[4]) < 7 and float(discount[0]) >= 10 or float(discount[2]) > 5 :
            embed.colour = discord.Colour(cfg["main"]["message_colors"][3])
            await channel[3].send(embed=embed, view=view)

    except Exception as e:
        print("send_message: ",e)
        return
    finally:
        await update_statistics(info[4], discount[0], discount[2])

@client.event
async def on_ready():
    global pool
    print(f'Logged on as {client.user}!')

    pool = await aiomysql.create_pool(
        host = cfg["database"]["host"],
        port = cfg["database"]["port"],
        user = cfg["database"]["user"],
        password = cfg["database"]["password"],
        db = cfg["database"]["db"],
        minsize = cfg["database"]["minsize"],
        maxsize = cfg["database"]["maxsize"]
    )
    
    asyncio.gather(send_latest_offers(), send_message_worker(), send_statistics_embed())


@client.event
async def on_close():
    await close_pool()


client.run(cfg["main"]["discord_client_token"])