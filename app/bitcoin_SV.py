import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BSV_balance,BSV_transactions

#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def bitcoin_svs_data(address,symbol,type_id):
    ret=BSV_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    respon = response_user_token.json()  
    response = respon['data']

    doc=BSV_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       

    transactions=res['data']['data']

    array=[]
    for transaction in transactions:
        fee =transaction['income']
        timestamp = transaction['time']
        date = int(timestamp)
        dt_object = datetime.fromtimestamp(date)
        inputs=transaction['inputs']
        outputs=transaction['outputs']
        frm=[]
        for inpt in inputs:
            prev_address=inpt['prev_addresses']
            prev_value = inpt['prev_value']
            for frmm in prev_address:
                frm.append({"from":frmm,"send_amount":prev_value})
        to=[]
        for outp in outputs:
            addresses=outp['addresses']
            val =outp['value']
            for too in addresses:
                to.append({"to":too,"receive_amount":val})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})

    balance = response['balance']
    amount_recived =response['total_receive']
    amount_sent =response['total_send']

    ret = mongo.db.address.update({
            "address":address            
        },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id
            }},upsert=True)

    ret = mongo.db.address.find_one({
        "address":address
    })
    _id=ret['_id']

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":balance,
                "amountReceived":amount_recived,
                "amountSent":amount_sent,
                "transactions":array
            }},upsert=True)

    return jsonify({"status":"success"})
