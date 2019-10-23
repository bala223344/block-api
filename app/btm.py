import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BTM_balance,BTM_transactions



#----------Function for fetching tx_history and balance storing in mongodb----------

def btm_data(address,symbol,type_id):
    response_user_token = requests.post(BTM_balance ,data={"account_name":address})
    response = response_user_token.json()          
    
    doc=BTM_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    
    
    return jsonify(res)
