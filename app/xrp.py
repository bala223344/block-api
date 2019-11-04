import requests
from flask import jsonify
from app import mongo
from app.config import XRP_balance,XRP_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,XRP_transactions
from app.config import mydb,mycursor



#----------Function for fetching tx_history and balance storing in mongodb----------

def xrp_data(address,symbol,type_id):
    ret=XRP_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    doc=XRP_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['transactions']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        fro = transaction['Account']
        if "Destination" in transaction:
            too = transaction['Destination']
        else:
            too=""
        fee = transaction['Fee']
        date = transaction['date']
        frm.append({"from":fro,"send_amount":""})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":date})
    

    balance=response['initial_balance']
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




#-----------Function for send notifications about transactions notification movement-----------

def xrp_notification(address,symbol,type_id):
    ret=XRP_transactions.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()  
    total_current_tx=transaction['count'] 
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
                html_content= '<h3> You got a new transaction on your XRP address</h3>')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            print("email is none")
    else:
        print("no new transaction")
