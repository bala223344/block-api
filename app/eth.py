from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def eth_data(address,symbol):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_trans" in records:
        url1=records['url_trans']
    ret=url.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    response_user_token = requests.get(url=ret1)
    response = response_user_token.json()       

    if symbol == "ETH":
        transaction = response['data']
        balance =transaction['balance']
        amountReceived =transaction['amountReceived']
        amountSent =transaction['amountSent']
        transactions = transaction['txs']
        array=[]
        
        for transaction in transactions:
            to=[]
            frm=[]
            too=transaction['to']
            to.append({"to":too,"receive_amount":""})
            frrm=transaction['from']
            frm.append({"from":frrm,"send_amount":""})
            price=transaction['quote']['price']
            timestamp =transaction['timestamp']
            dt_object = datetime.fromtimestamp(timestamp)
            array.append({"from":frm,"to":to,"date":dt_object,"fee":price})
    
    ret = mongo.db.address.update({
        "address":address            
    },{
        "$set":{
                "address":address,
                "symbol":symbol
            }},upsert=True)

    ret = mongo.db.address.find_one({
        "address":address
    })
    _id=ret['_id']

    ret = mongo.db.balance.update({
        "address":address            
    },{
        "$set":{
                "record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "balance":balance,
                "transactions":array,
                "amountReceived":amountReceived,
                "amountSent":amountSent
            }},upsert=True)
    
    return jsonify(response)
