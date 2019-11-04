import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import EOS_balance,EOS_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,XRP_transactions
from app.config import mydb,mycursor



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
        frm.append({"from":fro,"send_amount":amount_sent})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":"","from":frm,"to":to,"date":block_time})
    
    balance=response['core_liquid_balance']
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



#-----------send EOS transactions movement notification-------------

def eos_notification(address,symbol,type_id):
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
