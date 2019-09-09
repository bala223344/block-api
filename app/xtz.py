from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def xtz_data(address,symbol,type_id):
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
    array=[]
    
    for transaction in res:
        frm=[]
        to=[]
        trans =transaction['type']['operations']
        for tra in trans:
            amount=tra['amount']
            fee=""
            timestamp=tra['timestamp'] 
            too=tra['destination']
            tz = too['tz']
            fro=tra['src']
            tzz=fro['tz']
            frm.append({"from":tzz,"send_amount":(int(amount)/1000000)})
            to.append({"to":tz,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":timestamp})
    
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

    balance=response['balance']
    amount_recived =""
    amount_sent =""
    
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/1000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)

    return jsonify(response)
