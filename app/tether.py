from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def tether_data(address,symbol):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    response_user_token = requests.post(url ,data={"addr":address})
    response = response_user_token.json()          

    transactions=response['transactions']
    balances = response['balance']
    array=[]
    
    

    for transaction in transactions:
        fee =transaction['fee']
        timestamp = transaction['blocktime']
        dt_object = datetime.fromtimestamp(timestamp)
        frm=[]
        if "referenceaddress" in transaction:
            fromm=transaction['referenceaddress']
            frm.append({"from":fromm,"send_amount":""})
        to=[]
        if "sendingaddress" in transaction:
            too = transaction['sendingaddress']
            to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
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
      
    bal=balances[0]
    value=bal['value']
    amount_recived =""
    amount_sent =""


    ret = mongo.db.balance.update({
        "address":address            
    },{
        "$set":{
                "record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "balance":(int(value)/100000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    
    return jsonify(response)
    