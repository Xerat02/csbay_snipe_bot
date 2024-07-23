####################################
#
#
# This snipe bot is created by Xerat
#
#
####################################

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
from pymongo.errors import DuplicateKeyError


#variable that stores latest snipes
processed_messages = deque(maxlen=300)



#config
cfg = tl.cfg_load("config")



#mongoDB
mongo_client = MongoClient(cfg["mongoDB"]["uri"])
db = mongo_client["csbay"]



#main function that processing new offers and saving them into the database
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
                    buff_data_update_time = buff_row["update_time"]

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

                        #if item is good item will be saved into the database   
                        if buff_discount > 4 or profit[0] > 2:
                            item_data = {
                                "_id": market_item_link,  
                                "item_name": buff_skin_name,
                                "market_name": market_name,
                                "buff_price": buff_price,
                                "market_price": market_price,
                                "buff_discount": buff_discount,
                                "market_risk_factor": market_risk_factor,
                                "profit": profit,
                                "buff_item_sell_num": buff_item_sell_num,
                                "buff_item_link": f"https://buff.163.com/goods/{buff_id}",
                                "buff_item_image": buff_item_image,
                                "buff_data_update_time": buff_data_update_time,
                                "inserted_time": datetime.now()
                            }
                            print(item_data)
                            await update_statistics(item_name=buff_skin_name, market_name=market_name, discount=buff_discount, profit=profit, message_url=market_item_link)
                            processed_messages.append(market_item_link)
                            try:
                                db["snipe_processed_items"].insert_one(item_data)
                            except DuplicateKeyError:
                                pass 
                #else:
                #    print("Not found!")
                #    print("-------------")
                #    print(buff_row)
                #    print(market_skin_name)  
                #    print(search_value)
                #    print(market_name)  
                #    print("-------------")              
    except Exception as e:
        tl.exceptions(e)



#fuction that reads data from market script files and executing process_data function with that data
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



#function that running process data function in the threads
async def latest_offers():
    try:
        while True:
            tasks = [process_file("textFiles/"+filename) for filename in cfg["main"]["files"]]            
            await asyncio.gather(*tasks)            
            await asyncio.sleep(cfg["main"]["offers_check_delay"])            
    except Exception as e:
        tl.exceptions(e)



#function that updating individual markets statistics
async def update_statistics(item_name, market_name, discount, profit, message_url):
    collection = db["snipe_statistic_market_data"]
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

            last_hour_update_time = data.get("last_hour_update_time")

            if abs(datetime.now() - last_hour_update_time) > timedelta(hours=1):
                collection.update_one(
                    {"_id": market_name},
                    {
                        "$set": {
                                    "last_hour_count": data.get("count", 0),
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
        await update_total_statistics(profit[0])



#function that updating total markets statistics
async def update_total_statistics(profit):
    collection = db["snipe_statistic_market_data"]
    
    try:
        market_data = list(collection.find().sort({"max_profit": -1}))
        if len(market_data) > 0:
            collection = db["snipe_statistic"]

            count = 0
            hour_count = 0
            average = 0
            total_profit = 0

            for value in market_data:
                count = count + value.get("count", 0)
                hour_count = hour_count + (value.get("count") - value.get("last_hour_count"))
                average = average + value.get("average", 0)
                total_profit = total_profit + value.get("total_profit", 0)
            average = average / len(market_data)

            collection.update_one(
                {"_id": "All markets"},
                {
                    "$set": {
                                "count": count,
                                "average": average,
                                "max_profit": market_data[0].get("max_profit"),
                                "total_profit": total_profit,
                                "message_url": market_data[0].get("message_url"),
                                "update_time": datetime.now(),
                            }
                },
                upsert=True
            )

            #hour time stats
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



#run scripts
async def main():
    await asyncio.gather(latest_offers(),currency_updater())



#run main function
if __name__ == "__main__":
    asyncio.run(main())