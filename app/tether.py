import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import USDT_balance


#----------Function for fetching tx_history and balance storing in mongodb----------

def tether_data(address,symbol,type_id):
    response_user_token = requests.post(USDT_balance ,data={"account_name":address})
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
    
      
    bal=balances[0]
    value=bal['value']
    amount_recived =""
    amount_sent =""


    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{ 
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(value)/100000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    
    return jsonify({"status":"success"})
    