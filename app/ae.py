import requests
from flask import request,jsonify
from datetime import datetime
from app import mongo



#----------Function for fetching tx_history and balance storing in mongodb----------

def ae_data(address,symbol,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    print(ret)
    print(url)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    transactions = response_user.json()       
    total_current_tx=len(transactions)
    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        timestamp = transaction['time']
        tx_id = transaction['hash']
        txs_history = transaction['tx']
        fro =txs_history['sender_id']
        too=""
        fee =txs_history['fee']
        send_amount=txs_history['amount']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":timestamp,"Tx_id":tx_id})
    
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
                "balance":(int(balance)/1000000000000000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify(balance)
