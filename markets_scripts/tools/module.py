import asyncio
import aiohttp
import time
import logging
import os
import sys
import json
import random
import re
import unicodedata
from aiohttp import ClientError, ClientResponseError, ServerTimeoutError, ClientPayloadError
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from pymongo import MongoClient, UpdateOne



#######################################
# Expection function
#######################################



def exceptions(e, level=logging.ERROR, log_file=None):
    logger = logging.getLogger(__name__)
    e_type, e_object, e_traceback = sys.exc_info()
    e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
    e_message = str(e)
    e_line_number = e_traceback.tb_lineno

    log_message = "\n---------------------------------------------------------------------------------------------\n"
    log_message += "---------------------------------------------------------------------------------------------\n"
    log_message += f"Exception type: {e_type}\n"
    log_message += f"Exception filename: {e_filename}\n"
    log_message += f"Exception line number: {e_line_number}\n"
    log_message += f"Exception message: {e_message}\n"
    log_message += f"Exception args: {e.args}\n" 

    if hasattr(e, 'cause'):
        log_message += f"Cause: {e.cause}\n"  

    log_message += "---------------------------------------------------------------------------------------------\n"
    log_message += "---------------------------------------------------------------------------------------------"

    if log_file:
        logging.basicConfig(filename=log_file, level=level)
    else:
        logging.basicConfig(level=level)

    logger.log(level, log_message)
    time.sleep(0.3)



#######################################
# Config load function
#######################################



def cfg_load(file_name, dir = "configs/"):
    try:
        return json.load(open(dir+str(file_name)+".json"))
    except FileNotFoundError as e:
        exceptions(e)
    except Exception as e:
        exceptions(e)    



cfg = cfg_load("config")



#######################################
# Request
#######################################

## List of proxies
#proxies = [
#    "192.53.66.122:6228:hhocrsgo:g84uej4uz8ug",
#    "192.145.71.191:6828:hhocrsgo:g84uej4uz8ug",
#    "204.93.147.10:6564:hhocrsgo:g84uej4uz8ug",
#]
#
#current_proxy_index = 0
#
#def get_next_proxy():
#    global current_proxy_index
#    proxy = proxies[current_proxy_index]
#    ip_port, username, password = proxy.rsplit(":", 2)
#    current_proxy_index = (current_proxy_index + 1) % len(proxies)
#    return {
#        "http": f"http://{username}:{password}@{ip_port}",
#        "https": f"https://{username}:{password}@{ip_port}",
#        "raw": f"{ip_port}" 
#    }



async def fetch(url, headers=None, cookies=None, json_format=None, mode=1, response_format="json", proxy=True, method="get", params=None):
    retries = 3  # Increase retries for better fault tolerance
    headers = headers or {}
    proxy_url = "http://hhocrsgo-rotate:g84uej4uz8ug@p.webshare.io:80/" if proxy else None

    for attempt in range(retries):
        try:
            headers.update(random.choice(cfg_load("headers")["result"]))
            async with aiohttp.ClientSession() as session:
                response = None
                if method == "get":
                    response = await session.get(url, proxy=proxy_url, headers=headers, timeout=15, cookies=cookies, json=json_format, params=params)
                elif method == "post":
                    response = await session.post(url, proxy=proxy_url, headers=headers, timeout=15, cookies=cookies, json=json_format, params=params)
                
                response.raise_for_status()
                text = await response.text()
                if response_format == "json":
                    try:
                        return await response.json()
                    except ClientResponseError as e:
                        print(f"Error decoding JSON: {e}")
                        return extract_json_from_html(text)
                elif response_format == "html":
                    return text

        except (ClientResponseError, ServerTimeoutError, ClientPayloadError) as e:
            print(f"Attempt {attempt + 1} failed with a client/server error: {e}")
        except ClientError as e:
            print(f"Attempt {attempt + 1} encountered a client error: {e}")
        except asyncio.TimeoutError as e:
            print(f"Attempt {attempt + 1} timed out: {e}")
        except Exception as e:
            print(f"Attempt {attempt + 1} encountered an unexpected error: {e}")

        await asyncio.sleep(5)

    return None

def extract_json_from_html(html):
    """
    Extract JSON data from HTML content using regex
    """
    try:
        json_str = re.search(r'{.*}', html, re.DOTALL)
        if json_str:
            return json.loads(json_str.group(0))
        else:
            print("No JSON found in HTML.")
            return None
    except Exception as e:
        print(f"Error extracting JSON from HTML: {e}")
        return None


#######################################
# Currency function
#######################################



async def get_dollar(from_curr, amount):
    mongo_client = MongoClient(cfg["mongoDB"]["uri"])
    db = mongo_client["csbay"]
    collection = db["currency"]
    try:
        curr = float(collection.find_one({"_id": from_curr}).get("value"))
        usd = float(collection.find_one({"_id": "USD"}).get("value"))
        curr = curr / usd
        #print(amount / curr)
        if from_curr == "USD":
            return usd
        else:    
            return float(amount) / float(curr)
    except Exception as e:
        exceptions(e)    



#######################################
# String function
#######################################



def preprocess_string(input_string):
    normalized_string = unicodedata.normalize("NFC", input_string)
    ascii_string = normalized_string.encode('ascii', 'ignore').decode('ascii')
    alphanumeric_string = re.sub(r'[^a-zA-Z0-9]', '', ascii_string)
    final_string = alphanumeric_string.lower()
    
    return final_string
