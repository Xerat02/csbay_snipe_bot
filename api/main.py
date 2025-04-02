from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional



mongo_client = MongoClient("mongodb://192.168.88.16:27017/")
db = mongo_client["csbay"]



app = FastAPI()
limiter = Limiter(key_func=get_remote_address)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except RateLimitExceeded as e:
        raise HTTPException(status_code=429, detail="Too many requests")



@app.get("/servers")
@limiter.limit("20/minute")
async def root(request: Request):
    data = db["snipe_discord_channels"].find().sort("info.member_count", -1)
    new_list = [value["info"] for value in data]
    return new_list



@app.get("/snipes")
@limiter.limit("80/minute")
async def get_snipes(
    request: Request,
    risk_factor: Optional[float] = Query(None, ge=0, le=3),
    buff_discount: Optional[float] = Query(None, ge=0.0),
    min_price: Optional[float] = Query(None, ge=0.0),
    max_price: Optional[float] = Query(None, ge=0.0)
):
    query = {}
    
    if risk_factor is not None:
        query["market_risk_factor"] = {"$lte": risk_factor}
    
    if buff_discount is not None:
        query["buff_discount"] = {"$gte": buff_discount}
    
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        query["market_price"] = price_filter

    data = db["snipe_processed_items"].find(query).sort("inserted_time", -1).limit(30)
    new_list = list(data)
    return new_list
