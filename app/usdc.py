import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import USDT_balance,USDT_transactions



#----------Function for fetching tx_history and balance storing in mongod----------

def usdc_data(address,symbol,type_id):
    ret=USDT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=USDT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['result']
    

    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        fee =""
        timestamp = transaction['timeStamp']
        first_date=int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        fro =transaction['from']
        send_amount=transaction['value']
        too=transaction['to']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":send_amount})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['result']
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
