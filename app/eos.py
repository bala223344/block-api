import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import EOS_balance,EOS_transactions




#----------Function for fetching tx_history and balance storing in mongodb----------

def eos_data(address,symbol,type_id):
    acouunt={"account_name":address}
    response_user_token = requests.post(url=EOS_balance,json=acouunt)
    response = response_user_token.json()       
    pay={"account_name":address,"offset":"-20","pos":"-1"}
    response_user = requests.post(url=EOS_transactions,json=pay)
    res = response_user.json()       
    transactions=res['actions'] 
    
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        block_time=transaction['block_time']
        action_trace=transaction['action_trace']['act']['data']
        if "from" in action_trace:
            fro = action_trace['from']
        else:
            fro=""
        if "to" in action_trace:   
            too=action_trace['to']
        else:
            too=""
        if "quantity" in action_trace:   
            amount_sent=action_trace['quantity']

        else:
            amount_sent=""
        amount_sent = amount_sent.replace(" EOS", "")

        frm.append({"from":fro,"send_amount":amount_sent})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":"","from":frm,"to":to,"date":block_time})
    
    balance=float(response['core_liquid_balance'].replace(" EOS", ""))
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
    
    return jsonify(balance)


