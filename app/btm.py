from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
import dateutil.parser as parser
from app import mongo



#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def btm_data(address,symbol,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    response_user_token = requests.post(url ,data={"account_name":address})
    response = response_user_token.json()          
    
    if "url_transaction" in records:
        url1=records['url_transaction']
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    
    
    return jsonify(res)
