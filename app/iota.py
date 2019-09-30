import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import IOTA_balance


#----------Function for fetching tx_history and balance storing in mongodb----------

def iota_data(address,symbol,type_id):
    ret=IOTA_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    transactions = response['transactions']
    array=[]
    
    for transaction in transactions:
        to =[]
        fro =[]
        fee =transaction['value']
        timestamp = transaction['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        addr=transaction['address'] 
        amount=transaction['value']
        amo =int(amount)/1000000000000000
        amou=float("{0:.2f}".format(amo))
        fro.append({"from":addr,"send_amount":amou}) 
        array.append({"fee":fee,"from":fro,"to":to,"date":dt_object})
    
    balance = response['balance']
    ball =int(balance)/1000000000000000
    bal=float("{0:.2f}".format(ball))
    amount_recived =""
    amount_sent =""

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":bal,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)

    return jsonify({"status":"success"})
