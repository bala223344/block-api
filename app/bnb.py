import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BNB_balance,BNB_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BNB_balance
from app.config import mydb,mycursor



#----------Function for fethcing tx_history and balance from api and send notification if got a new transaction---------- 

def bnb_data(address,symbol,type_id):
    ret=BNB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=BNB_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()      
    transactions = res['txArray']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        if "fromAddr" and "toAddr" in transaction:
            tx_id = transaction['txHash']
            fee =transaction['txFee']
            timestamp = transaction['timeStamp']
            conver_d =timestamp/1000.0
            dt_object = datetime.fromtimestamp(conver_d)
            amount = transaction['value']
            fro = transaction['fromAddr']
            too = transaction['toAddr']   
            frm.append({"from":fro,"send_amount":amount})
            to.append({"to":too,"receive_amount":""})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    
 
    amount_recived =""
    amount_sent =""
    reslt = response['balance']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset']
            if asset_name == "BNB":
                balance = ress['free']
                
    
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
    



#-----------Function for send notifications about transactions movement-----------

def bnb_notification(address,symbol,type_id):
    print("bnb_notification")
    ret=BNB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()  
    total_current_tx=transaction['transactions'] 
    
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchone()
    tx_count=current_tx[0]
    if tx_count is None or total_current_tx > tx_count:
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        email_id=email[0]
        if email_id is not None:
            message = Mail(
                from_email=Sendgrid_default_mail,
                to_emails=email_id,
                subject='SafeName - New Transaction Notification In Your Account',
                html_content= '<h3> You got a new transaction on your BNB address</h3>')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            print("email is none")
    else:
        print("no new transaction")






'''
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
'''




