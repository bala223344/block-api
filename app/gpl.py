import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import GPL_balance,GPL_transactions



#----------Function for fetching tx_history and balance storing in mongodb----------

def gpl_data(address,symbol,type_id):
    print("gpl_data_running")
    ret=GPL_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=GPL_transactions.replace("{{address}}",''+address+'')
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
        too=transaction['to']
        send_amount=transaction['value']
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xeeddaa78e0b2de769e969bd049c8faff3280df97":
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000)})
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
                "balance":(int(balance)/1000000000000000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify({"status":"success"})