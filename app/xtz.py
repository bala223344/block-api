import requests
from flask import jsonify
from app import mongo
from app.config import XTZ_balance,XTZ_transactions
from app.config import mycursor,mydb
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BTC_balance


#----------Function for fetching tx_history and balance storing in mongodb----------

def xtz_data(address,symbol,type_id):
    ret=XTZ_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    doc=XTZ_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    array=[]
    
    for transaction in res:
        frm=[]
        to=[]
        trans =transaction['type']['operations']
        for tra in trans:
            amount=tra['amount']
            fee=""
            timestamp=tra['timestamp'] 
            too=tra['destination']
            tz = too['tz']
            fro=tra['src']
            tzz=fro['tz']
            frm.append({"from":tzz,"send_amount":(int(amount)/1000000)})
            to.append({"to":tz,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":timestamp})
    

    balance=response['balance']
    amount_recived =""
    amount_sent =""
    
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/1000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)

    return jsonify({"status":"success"})


def xtz_notification(address,symbol,type_id):
    ret=XTZ_balance.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    response_user_token = requests.get(url=ret1)
    transaction = response_user_token.json()  
    total_current_tx=transaction['transaction_count']
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
                html_content= '<h3> You got a new transaction on your XTZ address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
        else:
            pass
    else:
        pass
