####################################
#
#
# This snipe bot is created by Xerat
#
#
####################################

import aiohttp
import asyncio
import shutil
import os
import re
import unicodedata
import tools.module as tl
import json
import time 
import threading
from datetime import datetime, timedelta
from collections import deque
from pymongo import MongoClient, UpdateOne
from pymongo.errors import DuplicateKeyError



#config
cfg = tl.cfg_load("config")



#mongoDB
mongo_client = MongoClient(cfg["mongoDB"]["uri"])
db = mongo_client["csbay"]



# Main function that processes new offers and saves them into the database
def process_data(market_array):
    try:
        collection = db["buff_items"]

        for market_row in market_array:
            if len(market_row) > 1:
                market_risk_factor = 0
                market_skin_name = str(market_row["name"])
                market_price = float(market_row["price"])
                market_item_link = market_row["link"].replace(" ", "%20")
                market_name = market_row["source"]
                market_stickers = None
                if market_row.get("stickers"):
                    market_stickers = market_row.get("stickers")
                
                search_name = tl.preprocess_string(market_skin_name)
                buff_row = collection.find_one({"search_name": search_name})

                if buff_row:
                    buff_id = buff_row["_id"]
                    buff_skin_name = str(buff_row["market_hash_name"]).strip()
                    buff_sell_price = round(buff_row["price_in_usd"], 2)
                    buff_buy_price = round(buff_row["buy_max_price"], 2)
                    buff_item_buy_num = buff_row["buy_num"]
                    buff_item_sell_num = buff_row["sell_num"]
                    buff_item_image = buff_row["item_image"]
                    buff_data_update_time = buff_row["update_time"]
                    steam_price = buff_row["steam_price"]

                    if buff_buy_price <= 0 or buff_sell_price <= 0 or market_price <= 0:
                        continue
                
                    buff_price = buff_sell_price if buff_sell_price != 0 else buff_buy_price
                    if buff_sell_price != 0 and buff_buy_price != 0:
                        price_diff = abs(buff_sell_price - buff_buy_price) / min(buff_sell_price, buff_buy_price)
                        if price_diff > 0.10:
                            buff_price = min(buff_sell_price, buff_buy_price)

                    # Calculate risk factor
                    if buff_item_sell_num < 50:
                        market_risk_factor += 1
                    if buff_item_buy_num < 30:
                        market_risk_factor += 1    
                    if (abs(((buff_buy_price / buff_sell_price) - 1) * 100)) > 7:
                        market_risk_factor += 1

                    market_price = round(market_price, 2)
                    if market_price < buff_price and buff_price > 0.5:
                        buff_discount = round(((buff_price / market_price) - 1) * 100, 2)
                        steam_discount = round(((steam_price / market_price) - 1) * 100, 2)
                        profit = [round(buff_price - market_price, 2), round((buff_price * 0.975) - market_price, 2)]

                        # Save good items to the database
                        if buff_discount < 220 and ((buff_discount > 4 and profit[0] > 1) or profit[0] > 30):
                            item_data = {
                                "_id": market_item_link + str(market_price) + str(buff_discount),  
                                "item_name": buff_skin_name,
                                "market_name": market_name,
                                "market_link": market_item_link,
                                "market_logo": cfg["main"]["icons_urls"].get(market_name, ""),
                                "buff_price": buff_price,
                                "market_price": market_price,
                                "buff_discount": buff_discount,
                                "steam_discount": steam_discount,
                                "market_risk_factor": market_risk_factor,
                                "profit": profit,
                                "buff_item_sell_num": buff_item_sell_num,
                                "buff_item_link": f"https://buff.163.com/goods/{buff_id}",
                                "buff_item_image": buff_item_image,
                                "buff_data_update_time": buff_data_update_time,
                                "inserted_time": datetime.now()
                            }
                            if market_stickers:
                                item_data["stickers"] = market_stickers
                            try:
                                db["snipe_processed_items"].insert_one(item_data)
                                print(item_data)
                                update_statistics(item_name=buff_skin_name, market_name=market_name, discount=buff_discount, profit=profit, message_url=market_item_link)
                            except DuplicateKeyError:
                                pass
                else:
                    if market_name == "":
                        print("----------------------------")
                        print(market_skin_name)
                        print(market_name)
                        print(search_name)
                        print(len(search_name))
                        print("----------------------------")             
    except Exception as e:
        tl.exceptions(e)



# Function to read data from market script files and execute process_data function with that data
def process_file(filename):
    while True:
        start_time = time.time()
        temp_folder = cfg["main"]["temp_files_location"]
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        base_name = os.path.basename(filename)
        temp_filename = os.path.join(temp_folder, "temp_" + base_name)
        shutil.copy(filename, temp_filename)
        try:
            with open(temp_filename, "r", encoding="utf-8") as file:
                item_array = file.read()
                if item_array:
                    process_data(json.loads(item_array))
                    with open(filename, "w", encoding="utf-8") as file:
                        pass            
        except Exception as e:
            print(filename)
            tl.exceptions(e)  
        finally:               
            os.remove(temp_filename)
            if time.time() - start_time < 1:
                time.sleep(0.2)
            #print(filename)



# Function to run process data function in threads
async def latest_offers():
    try:
        for filename in cfg["main"]["files"]:
            thread = threading.Thread(target=process_file, args=(f"textFiles/{filename}",))
            thread.start()
    except Exception as e:
        tl.exceptions(e)



#function that updating individual markets statistics
def update_statistics(item_name, market_name, discount, profit, message_url):
    collection = db["snipe_statistic_market_data"]
    new_count = None  
    new_average = None  
    new_max_profit = None
    
    try:
        data = collection.find_one({"_id": market_name})

        #general snipe data
        if data:
            old_count = data.get("count", 0) 
            old_average = data.get("average", 0)   
            old_potencial_profit = data.get("potencial_profit")
            old_total_profit = data.get("total_profit", 0)

            new_count = old_count + 1
            new_average = float(((old_average * old_count) + discount) / new_count)
            new_average = round(new_average, 2)
            new_message_url = data.get("message_url")
            new_total_profit = old_total_profit + profit[0]

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
                                "total_profit": new_total_profit,
                                "message_url": new_message_url,
                                "update_time": datetime.now(),
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
                                "last_hour_count": 0,
                                "average": new_average,
                                "max_profit": new_max_profit,
                                "total_profit": profit[0],
                                "message_url": message_url,
                                "update_time": datetime.now(),
                                "last_hour_update_time": datetime.now()
                            }
                },
                upsert=True
            )



        #time snipe data (1 min, 10min, 1h, 1d, 1w)
        collection = db["snipe_statistic_time_frame"]
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

        #most common items      
        collection = db["snipe_statistic_item_snipes"]
        item = collection.find_one({"_id": item_name})

        if item:
            collection.update_one(
                {"_id": item_name},
                {
                    "$set": {
                                "average_discount": (item.get("average_discount") + discount) / item.get("count"),
                                "count": item.get("count") + 1
                            }
                },
                upsert=True
            )
        else:
            collection.update_one(
                {"_id": item_name},
                {
                    "$set": {
                                "average_discount": discount,
                                "count": 1
                            }
                },
                upsert=True
            )    
    except Exception as e:
        tl.exceptions(e)
    finally:
        update_total_statistics(profit[0])



#function that updating total markets statistics
def update_total_statistics(profit):
    collection = db["snipe_statistic_market_data"]
    try:
        market_data = list(collection.find().sort({"max_profit": -1}))
        if len(market_data) > 0:
            # Market last hour count            
            for value in market_data:
                last_hour_update_time = value.get("last_hour_update_time")
                if abs(datetime.now() - last_hour_update_time) > timedelta(hours=1):
                    collection.update_one(
                        {"_id": value.get("_id")},
                        {
                            "$set": {
                                        "last_hour_count": value.get("count", 0),
                                        "last_hour_update_time": datetime.now()
                                    }
                        },
                        upsert=True
                    )   

            # Total market stats
            count = 0
            hour_count = 0
            average = 0
            total_profit = 0
            last_hour_count = 0

            for value in market_data:
                count = count + value.get("count", 0)
                hour_count = hour_count + (value.get("count") - value.get("last_hour_count"))
                average = average + value.get("average", 0)
                total_profit = total_profit + value.get("total_profit", 0)
                last_hour_count = last_hour_count + value.get("last_hour_count", 0)
            average = round(average / len(market_data), 2)

            collection = db["snipe_statistic"]
            collection.update_one(
                {"_id": "All markets"},
                {
                    "$set": {
                                "count": count,
                                "last_hour_count": last_hour_count,
                                "average": average,
                                "max_profit": market_data[0].get("max_profit"),
                                "total_profit": total_profit,
                                "message_url": market_data[0].get("message_url"),
                                "update_time": datetime.now(),
                            }
                },
                upsert=True
            )

        # Hour time stats
        collection = db["snipe_statistic_hour_data"]
        hour_data = list(collection.find())

        if len(hour_data) > 0 and count != 0:
            curent_hour_data = collection.find_one({"_id": datetime.now().hour})
            if curent_hour_data:
                curent_hour_data_new_count = curent_hour_data.get("count", 0) + 1
                curent_hour_data_new_total_profit = curent_hour_data.get("total_profit", 0) + profit
                collection.update_one(
                    {"_id": float(datetime.now().hour)},
                    {
                        "$set": {
                                    "count": curent_hour_data_new_count,
                                    "total_profit": curent_hour_data_new_total_profit
                                }
                    },
                    upsert=True
                )

            busyness_percentage = 0
            profit_percentage = 0

            for x in hour_data:
                busyness_percentage = busyness_percentage + x.get("count", 0)
                profit_percentage = profit_percentage + x.get("total_profit", 0)
            busyness_percentage = 100 / busyness_percentage   
            profit_percentage = 100 / profit_percentage   
            for x in hour_data:
                collection.update_one(
                    {"_id": x.get("_id")},
                    {
                        "$set": {
                                    "busyness_percentage": round((busyness_percentage * x.get("count")), 2),
                                    "profit_percentage": round((profit_percentage * x.get("total_profit", 0)), 2)
                                }
                    },
                    upsert=True
                )        
        else:
            for x in range(0, 24, 1):
                collection.update_one(
                    {"_id": x},
                    {
                        "$set": {
                                    "count": 0,
                                }
                    },
                    upsert=True
                )

    except Exception as e:
        tl.exceptions(e)        



#functions that every 24h updating currency in the database
async def currency_updater():
    while True:
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



#functions that every 4h update steam prices
async def steam_updater():
    while True:
        collection = db["buff_items"]
        token = cfg["main"]["steam_updater_token"]
        try:
            last_update = collection.find_one({}, sort=[("steam_update_time", -1)])
            current_time = datetime.now()
            if not last_update or (current_time - last_update.get("steam_update_time", datetime.min)) > timedelta(hours=4):
                data = await tl.fetch(f"https://www.steamwebapi.com/steam/api/items?key={token}", proxy=False, timeout=300)
                if data:
                    for obj in data:
                        market_hash_name = obj.get("markethashname")
                        steam_price = obj.get("pricelatest")

                        if not market_hash_name or steam_price is None:
                            continue
                        
                        collection.update_one(
                            {"market_hash_name": market_hash_name},
                            {
                                "$set": {
                                    "steam_price": steam_price,
                                    "steam_update_time": current_time,
                                }
                            },
                        )
        except Exception as e:
            tl.exceptions(e)
        finally:
            await asyncio.sleep(cfg["main"]["steam_updater_delay"])



#run scripts
async def main():
    await asyncio.gather(latest_offers(),currency_updater(), steam_updater())



#run main function
asyncio.run(main())