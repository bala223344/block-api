import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import USDT_balance,USDT_transactions
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BTC_balance
from app.config import mydb
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



#----------Function for fetching tx_history and balance storing in mongod----------

def usdc_data(address,symbol,type_id):
    ret=USDT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=USDT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['result']
    

    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        fee =""
        timestamp = transaction['timeStamp']
        first_date=int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        fro =transaction['from']
        send_amount=transaction['value']
        too=transaction['to']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":send_amount})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['result']
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


def usdc_notification(address,symbol,type_id):
    doc=USDT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()  
    transactions=res['result']
    tx_list = []
    for transaction in transactions:
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xb63b606ac810a52cca15e44bb630fd42d8d1d83d":
            tx_list.append({"transaction":"tx"})

    total_current_tx = len(tx_list)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchone()
    tx_count=current_tx[0]
    if tx_count is None or total_current_tx > tx_count:
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        mycursor.close()
        email_id=email[0]
        if email_id is not None:
            message = Mail(
                from_email=Sendgrid_default_mail,
                to_emails=email_id,
                subject='SafeName - New Transaction Notification In Your Account',
                html_content= '<h3> You got a new transaction on your USDC address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
        else:
            pass
    else:
        pass
