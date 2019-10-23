import requests
from flask import jsonify
from app import mongo
from app.config import XRP_balance,XRP_transactions




#----------Function for fetching tx_history and balance storing in mongodb ----------

def xrp_data(address,symbol,type_id):
    ret=XRP_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    doc=XRP_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['transactions']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        fro = transaction['Account']
        if "Destination" in transaction:
            too = transaction['Destination']
        else:
            too=""
        fee = transaction['Fee']
        date = transaction['date']
        frm.append({"from":fro,"send_amount":""})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":date})
    

    balance=response['initial_balance']
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
