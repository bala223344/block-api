import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import ONT_balance,ONT_transactions

#----------Function for fetching tx_history and balance storing in mongodb ----------

def ont_data(address,symbol,type_id):
    ret=ONT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ONT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions = res['result']
    array=[]
    
    for transaction in transactions:
        fee =transaction['fee']
        timestamp = transaction['tx_time']
        dt_object = datetime.fromtimestamp(timestamp)
        transfers=transaction['transfers']
        frm=[]
        to=[]
        for v_in in transfers:
            if v_in is not None:
                amount = v_in['amount']
                fro = v_in['from_address']
                too = v_in['to_address']
                frm.append({"from":fro,"send_amount":amount})
                to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    ret = mongo.db.address.update({
            "address":address            
        },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id
            }},upsert=True)

    amount_recived =""
    amount_sent =""
    reslt = response['result']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset_name']
            if asset_name == "ont":
                balance = ress['balance']
                
    
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
