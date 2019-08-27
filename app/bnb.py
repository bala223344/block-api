from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def bnb_data(address,symbol,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()      
    transactions = res['txArray']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        if "fromAddr" and "toAddr" in transaction:
            fee =transaction['txFee']
            timestamp = transaction['timeStamp']
            conver_d =timestamp/1000.0
            dt_object = datetime.fromtimestamp(conver_d)
            amount = transaction['value']
            fro = transaction['fromAddr']
            too = transaction['toAddr']   
            frm.append({"from":fro,"send_amount":amount})
            to.append({"to":too,"receive_amount":""})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    ret = mongo.db.address.update({
            "address":address            
        },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id
            }},upsert=True)

    ret = mongo.db.address.find_one({
        "address":address
    })
    _id=ret['_id']

    amount_recived =""
    amount_sent =""
    reslt = response['balance']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset']
            if asset_name == "BNB":
                balance = ress['free']
                
    
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":balance,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify(res)
