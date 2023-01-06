from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Query,Body
import requests,json,random,string
from time import sleep

app = FastAPI()

@app.get("/pipi/{papa}")
def home(papa=0):
    return {"Home":papa}
@app.get("/binance/{type_order}/{payment_method}/{crypto}/{fiat}/filter")
def binance(type_order="SELL",payment_method="Brubank",crypto="USDT",fiat="ARS",merchant_check:Optional[bool]=Query(False),available_amount:Optional[float]=Query(0),min_limit:Optional[float]=Query(100000000)):#,max_limit=500000):
    if merchant_check:
        merchant_check="merchant"
    else:
        merchant_check=None
    datareq = {"asset": crypto,"fiat": fiat,"merchantCheck": "true","page": 1,"payTypes": [payment_method],"publisherType": merchant_check,"rows": 20,"tradeType": type_order}
    r = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",json=datareq)
    data=json.loads(r.text)
    response=[]
    for x in range(0,len(data['data'])):
        min=data['data'][x]['adv']["minSingleTransAmount"]
        max=data['data'][x]['adv']["maxSingleTransAmount"]
        price=data['data'][x]['adv']["price"]
        amount=data['data'][x]['adv']["surplusAmount"]  
        user=data['data'][x]['advertiser']['nickName']
        adv="https://p2p.binance.com/es/advertiserDetail?advertiserNo="+data['data'][x]['advertiser']['userNo']
        if available_amount<=float(amount) and min_limit>= float(min):
            response.append({"exchange" : "Binance P2P", "crypto" : datareq["asset"], "fiat" : datareq["fiat"], "payment_method" : datareq["payTypes"][0], "user" : user, "price" : price, "available_amount" : amount, "min_limit" : min, "max_limit" : max, "link": adv})
    #return len(data['data'])
    #return data
    return response
