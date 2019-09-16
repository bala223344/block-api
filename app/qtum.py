import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import QTUM_balance,QTUM_transactions

#----------Function for fetching tx_history and balance storing in mongodb----------

def qtum_data(address,symbol,type_id):
    ret=QTUM_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=QTUM_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['transactions']
    
    array=[]
    for transaction in transactions:
        
        
        ret1=url_hash.replace("{{hash}}",''+transaction+'')
        response_u = requests.get(url=ret1)
        res1 = response_u.json()
        
        for tran in res1:
            fee=tran['fees']
            timestamp=tran['timestamp']
            dt_object = datetime.fromtimestamp(timestamp)
            inputs=tran['inputs']
            outputs=tran['outputs']
            frm=[]
            for inp in inputs:
                addre=inp['address']
                val=inp['value']
                frm.append({"from":addre,"send_amount":(int(val)/100000000)})
            to=[]
            for inpp in outputs:
                ad=inpp['address']
                value=inpp['value']
                to.append({"to":ad,"receive_amount":(int(value)/100000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']

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
                "balance":(int(balance)/100000000),
                "transactions":array,
                "amountReceived":(int(amount_recived)/100000000),
                "amountSent":(int(amount_sent)/100000000)
            }},upsert=True)

    return jsonify({"status":"success"})
