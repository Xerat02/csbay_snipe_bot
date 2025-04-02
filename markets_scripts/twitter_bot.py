import tweepy
from pymongo import MongoClient
import os
import requests
import time
import pyshorteners
import tools.module as tl



# Config
cfg = tl.cfg_load("config")



bearer_token = "AAAAAAAAAAAAAAAAAAAAAE9AvgEAAAAAgvAcqal%2BPjKHYkPV%2F5hSTIrB5z0%3DiQShDZtM5pZI23WSjMVSCi63O11aeLqF6F60xXEna0RWORUK2h"
consumer_key = "2Ph28Zb750d0kRlFgIhbB1WNm"
consumer_secret = "8RD0aBpVmvTW0aybkaRJMnIFjX9SlVXBGpdKyUSiwkFw96IvSN"
access_token = "1826925788647591936-OHDvvaPfZFdu18kNHcwrt5bTT4yjbl"
access_token_secret = "tyCW9RDVBsy4O1XIBYZc7u83BVJKNim2GvOBJAingLK1J"



# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)



# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)



# Initialize the URL shortener
s = pyshorteners.Shortener()



def tweet_best_snipes():
    # MongoDB connection
    mongo_client = MongoClient(cfg["mongoDB"]["uri"])
    db = mongo_client["csbay"]
    collection = db["snipe_processed_items"]

    snipes = collection.find({"tweeted": {"$ne": True}})
    image_path = None
    try:
        for snipe in snipes:
            if snipe["buff_discount"] > 15 and snipe["market_price"] > 30:
                # Shorten the market link
                short_link = s.tinyurl.short(snipe['market_link'])

                tweet_text = (
                    f"🔥 Snipe Alert! 🔥\n\n"
                    f"{snipe['item_name']}\n"
                    f"Market Price: ${snipe['market_price']}\n"
                    f"Buff Price: ${snipe['buff_price']}\n"
                    f"Discount: {snipe['buff_discount']}%\n"
                    f"Market name: {snipe['market_name']}\n"
                    f"Link: {short_link}\n\n"
                    f"🚀 See live deals at csbay.org.\n\n"
                    f"#Gaming #CS2 #CounterStrike #Deals"
                )

                image_id = download_image(snipe["buff_item_image"])
                print(image_id)

                client.create_tweet(text=tweet_text, media_ids=[image_id])

                # Mark the item as tweeted
                collection.update_one({"_id": snipe["_id"]}, {"$set": {"tweeted": True}})
                print(f"Tweet was sent: {tweet_text}")
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"Temp file {image_path} was deleted.")
                break
    except Exception as e:
        tl.exceptions(e)



def download_image(url):
    response = requests.get(url)
    image_path = "temp_image.jpg"
    
    with open(image_path, "wb") as file:
        file.write(response.content)
    
    return api.media_upload(filename=image_path).media_id_string



if __name__ == "__main__":
    while True:
        tweet_best_snipes()
        time.sleep(2700)
