from flask import jsonify
import requests
from datetime import datetime
from app import mongo
from app.config import DASH_balance,DASH_transactions

#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def dash_data(address,symbol,type_id):
    
    ret=DASH_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    doc=DASH_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['txs'] 
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        fee = transaction['fees']
        time =transaction['time']
        dt_object = datetime.fromtimestamp(time)
        vin = transaction['vin']
        vout = transaction['vout']
        for v_in in vin:
            fro = v_in['addr']
            send_amount=v_in['value']
            frm.append({"from":fro,"send_amount":send_amount})

        for v_out in vout:
            val = v_out['value']
            scriptPubKey = v_out['scriptPubKey']
            if "addresses" in scriptPubKey:
                addresses=scriptPubKey['addresses']
                for addd in addresses:
                    to.append({"to":addd,"receive_amount":val})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance=response['balance']
    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']
    
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
    