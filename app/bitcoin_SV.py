from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
import dateutil.parser as parser
from app.util import serialize_doc
from app import mongo


def bitcoin_svs_data(address,symbol):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    respon = response_user_token.json()  
    response = respon['data']

    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       

    transactions=res['data']['data']

    array=[]
    for transaction in transactions:
        fee =transaction['income']
        timestamp = transaction['time']
        date = int(timestamp)
        dt_object = datetime.fromtimestamp(date)
        inputs=transaction['inputs']
        outputs=transaction['outputs']
        frm=[]
        for inpt in inputs:
            prev_address=inpt['prev_addresses']
            prev_value = inpt['prev_value']
            for frmm in prev_address:
                frm.append({"from":frmm,"send_amount":prev_value})
        to=[]
        for outp in outputs:
            addresses=outp['addresses']
            val =outp['value']
            for too in addresses:
                to.append({"to":too,"receive_amount":val})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})

    balance = response['balance']
    amount_recived =response['total_receive']
    amount_sent =response['total_send']

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
                "amountReceived":amount_recived,
                "amountSent":amount_sent,
                "transactions":array
            }},upsert=True)

    return jsonify(transactions)
