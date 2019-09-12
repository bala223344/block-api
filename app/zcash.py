from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo
from app.config import ZEC_balance,ZEC_transactions

#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def zcash_data(address,symbol,type_id):
    print("zcash") 
    ret=ZEC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ZEC_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    array=[]
    for transaction in res:
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        vin = transaction['vin']
        vout= transaction['vout']
        frm=[]
        for v_in in vin:
            if v_in is not None:
                retrievedVout = v_in['retrievedVout']['scriptPubKey']
                val = v_in['retrievedVout']['value']
                if "addresses" in retrievedVout:
                    addresses=retrievedVout['addresses']
                    for h in addresses:
                        frm.append({"from":h,"send_amount":val})
        to=[]
        for v_out in vout:
            if v_out is not None:
                retrieved = v_out['scriptPubKey']['addresses']
                valu = v_out['value']
                for a in retrieved:
                    to.append({"to":a,"receive_amount":valu})

        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    balance = response['balance']
    amount_recived =response['totalRecv']
    amount_sent =response['totalSent']

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":balance,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify({"status":"success"})
