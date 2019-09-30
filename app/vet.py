import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import VET_balance,VET_transactions



#----------Function for fetching tx_history and balance storing in mongodb ----------

def vet_data(address,symbol,type_id):
    ret=VET_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=VET_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       

    transactions=res['transactions']
    array=[]
    
    for transaction in transactions:
        if transaction:
            frm=[]
            to=[]
            timestamp = transaction['timestamp']
            origin =transaction['origin']
            dt_object = datetime.fromtimestamp(timestamp)
            vin = transaction['clauses']
            for trans in vin:
                too=trans['to']
                to.append({"to":too,"receive_amount":""})
                frm.append({"from":origin,"send_amount":""})
            array.append({"fee":"","from":frm,"to":to,"date":dt_object})
    
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
