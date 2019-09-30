import requests
from flask import jsonify
from datetime import datetime
import dateutil.parser as parser
from app import mongo
from app.config import UNUS_SED_LEO_balance,UNUS_SED_LEO_transactions



#----------Function for fetching tx_history and balance storing in mongodb----------

def unus_sed_leo_data(address,symbol,type_id):
    ret=UNUS_SED_LEO_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=UNUS_SED_LEO_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['result']
    array=[]

    for transaction in transactions:
        frm=[]
        to=[]
        fee =transaction['value']
        timestamp = transaction['timeStamp']
        first_date = int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        if "to" and "from" in transaction:
            too = transaction['to']
            fro = transaction['from']
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":(int(fee)/1000000000000000000)})
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
