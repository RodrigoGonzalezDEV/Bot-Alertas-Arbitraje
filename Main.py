from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Query,Body
import requests,json,random,string
from time import sleep

app = FastAPI()

class binance_consult(BaseModel):
    type_order: str
    payment_method: list
    crypto: str
    fiat: str
    merchant_check:Optional[bool]
    available_amount:Optional[float] = Query(100)
    min_limit: Optional[float] = Query(100)
    

@app.get("/pipi/{papa}")
def home(papa=0):
    return {"Home":papa}

@app.get("/binance/{type_order}/{payment_method}/{crypto}/{fiat}/filter")
def binance(type_order="SELL",payment_method="Brubank",crypto="USDT",fiat="ARS",merchant_check:Optional[bool]=Query(False),available_amount:Optional[float]=Query(0),min_limit:Optional[float]=Query(100)):
    if merchant_check:
        merchant_check="merchant"
    else:
        merchant_check=None
    datareq = {"asset": crypto,"fiat": fiat,"merchantCheck": "true","page": 1,"payTypes": [payment_method],"publisherType": merchant_check,"rows": 20,"tradeType": type_order}
    r = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",json=datareq)
    data=json.loads(r.text)
    print(datareq)
    response=[]
    for x in range(0,len(data['data'])):
        min=data['data'][x]['adv']["minSingleTransAmount"]
        max=data['data'][x]['adv']["maxSingleTransAmount"]
        price=data['data'][x]['adv']["price"]
        amount=data['data'][x]['adv']["surplusAmount"]  
        user=data['data'][x]['advertiser']['nickName']
        adv="https://p2p.binance.com/es/advertiserDetail?advertiserNo="+data['data'][x]['advertiser']['userNo']
        if available_amount<=float(amount) and min_limit>= float(min)and min_limit<= float(max):
            response.append({"exchange" : "Binance P2P", "crypto" : datareq["asset"], "fiat" : datareq["fiat"], "payment_method" : datareq["payTypes"][0], "user" : user, "price" : price, "available_amount" : amount, "min_limit" : min, "max_limit" : max, "link": adv})
    #return len(data['data'])
    #return data
    return response

@app.post("/binance")
def binance(consult: binance_consult = Body(...)):
    if consult.merchant_check:
        merchant_check="merchant"
    else:
        merchant_check=None
    datareq = {"asset": consult.crypto,"fiat": consult.fiat,"merchantCheck": "true","page": 1,"payTypes": consult.payment_method,"publisherType": merchant_check,"rows": 20,"tradeType": consult.type_order}
    r = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",json=datareq)
    data=json.loads(r.text)
    print(datareq)
    print(r.text)
    response=[]
    for x in range(0,len(data['data'])):
        min=data['data'][x]['adv']["minSingleTransAmount"]
        max=data['data'][x]['adv']["maxSingleTransAmount"]
        price=data['data'][x]['adv']["price"]
        amount=data['data'][x]['adv']["surplusAmount"]  
        user=data['data'][x]['advertiser']['nickName']
        adv="https://p2p.binance.com/es/advertiserDetail?advertiserNo="+data['data'][x]['advertiser']['userNo']
        if float(consult.available_amount)<=float(amount) and float(consult.min_limit)>= float(min)and float(consult.min_limit)<= float(max):
            response.append({"exchange" : "Binance P2P", "crypto" : datareq["asset"], "fiat" : datareq["fiat"], "payment_method" : datareq["payTypes"][0], "user" : user, "price" : price, "available_amount" : amount, "min_limit" : min, "max_limit" : max, "link": adv})
    #return len(data['data'])
    #return data
    return response

@app.get("/binance/payment_method/{fiat}")
def payment_method(fiat="USD"):
    datareq = {"fiat": fiat}
    r = requests.post("https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/filter-conditions",json=datareq)
    data=json.loads(r.text)
    response=[]
    for x in range(0,len(data['data']['tradeMethods'])):
        response.append(data['data']['tradeMethods'][x]['identifier'])
    return response

@app.get("/criptoya/{coin}/{fiat}")
def criptoya(coin="usdt",fiat="ars"):
    r = requests.get("https://criptoya.com/api/"+coin+"/"+fiat)
    data=json.loads(r.text)
    return data