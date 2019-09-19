import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import LINK_balance,LINK_transactions

#----------Function for fetching tx_history and balance storing in mongodb----------

def link_data(address,symbol,type_id):
    print("011111")
    ret=LINK_balance.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=LINK_transactions.replace("{{address}}",''+address+'')
    print(doc)
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['result']
    print("8888")
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
        if contractAddress == "0x514910771af9ca656af840dff83e8264ecf986ca":
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    print("333333")
    balance = response['result']
    amount_recived =""
    amount_sent =""
    print("377777")
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
    print("50000000")
    return jsonify({"status":"success"})
