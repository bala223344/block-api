from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,host,user,password,database,auth_plugin


#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def icx_data(address,symbol,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    print(ret)
    print(url)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['data']
    total_current_tx=len(transactions)
    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        fee =transaction['fee']
        timestamp = transaction['createDate']
        fro =transaction['fromAddr']
        too=transaction['toAddr']
        send_amount=transaction['amount']
        tx_id = transaction['txHash']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":(send_amount)})
        array.append({"fee":fee,"from":frm,"to":to,"date":timestamp,"Tx_id":tx_id})
    
    balance = response['data']['balance']
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
    return "success"
