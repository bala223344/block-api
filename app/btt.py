import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BTT_balance,BTT_transactions



#----------Function for fetching tx_history and balance storing in mongodb----------

def btt_data(address,symbol,type_id):
    ret=BTT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=BTT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions=res['data']
    
    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        conver_d =timestamp/1000.0
        dt_object = datetime.fromtimestamp(conver_d)
        fro =transaction['ownerAddress']
        too=transaction['toAddress']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":""})
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
                "balance":balance,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)

    return jsonify({"status":"success"})
