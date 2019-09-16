from flask import jsonify
import requests
from datetime import datetime
from app import mongo
from app.config import BTC_balance


#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------


def btc_data(address,symbol,type_id):
    ret=BTC_balance.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    print(ret1)
    response_user_token = requests.get(url=ret1)
    transaction = response_user_token.json()       
    
    balance =transaction['balance']
    amountReceived =transaction['amount_received']
    amountSent =transaction['amount_sent']
    transactions = transaction['txs']
    array=[]
    for transaction in transactions:
        fee=transaction['fee']
        tx_id = transaction['hash']
        frmm=transaction['inputs']
        frm=[]
        for trans in frmm:
            fro=trans['address']
            send=trans['value']
            frm.append({"from":fro,"send_amount":(int(send)/100000000)})
        transac=transaction['outputs']
        to=[]
        for too in transac:
            t = too['address'] 
            recive =too['value']
            to.append({"to":t,"receive_amount":(int(recive)/100000000)})
        timestamp =transaction['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/100000000),
                "transactions":array,
                "amountReceived":(int(amountReceived)/100000000),
                "amountSent":(int(amountSent)/100000000)
            }},upsert=True)
    return jsonify({"status":"success"})