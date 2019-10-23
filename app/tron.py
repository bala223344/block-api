import requests
from flask import jsonify
from datetime import datetime
import dateutil.parser as parser
from app import mongo
from app.config import TRON_balance,TRON_transactions



#----------Function for fetching tx_history and balance storing in mongodb----------

def tron_data(address,symbol,type_id):
    ret=TRON_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    doc=TRON_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions = res['data']
    
    array=[]
    
    for transaction in transactions:
        to=[]
        frm=[]
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        conver_d =timestamp/1000.0
        fro = transaction['ownerAddress']
        too = transaction['toAddress']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":""})
        dt_object = datetime.fromtimestamp(conver_d)
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =""
    amount_sent =""

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(balance/1000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify({"status":"success"})
