import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BNB_balance,BNB_transactions


#----------Function for fetching tx_history and balance storing in mongodb----------

def b_chain_data(address,symbol,type_id):
    ret=BNB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    bln_detail=response['matchData']
    balances = bln_detail['balance']

    doc=BNB_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions=res['txArray']
    array=[]

    for transaction in transactions:
        frm=[]
        to=[]
        if "value" in transaction:
            fee =transaction['txFee']
            timestamp = transaction['timeStamp']
            conver_d =timestamp/1000.0
            dt_object = datetime.fromtimestamp(conver_d)
            fromAddr = transaction['fromAddr']
            value = transaction['value']
            frm.append({"from":fromAddr,"send_amount":value})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
     
    for balan in balances:
        sym=balan['mappedAsset']
        if sym =="BNB":
            balance = balan['free']
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
    return jsonify(transactions)
