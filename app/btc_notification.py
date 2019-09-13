from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import mongo
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,host,user,password,database,auth_plugin,BTC_balance


#----------My sql connection-----------

import mysql.connector
mydb = mysql.connector.connect(host=host,user=user,password=password,database=database,auth_plugin=auth_plugin)
mycursor=mydb.cursor()


#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------


def btc_notification(address,symbol,type_id):
    print("ashgajhghgggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
    ret=BTC_balance.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    print(ret1)
    response_user_token = requests.get(url=ret1)
    transaction = response_user_token.json()  
    total_current_tx=transaction['transaction_count']
    '''
    transactions = transaction['txs']
    
    array=[]
    total_current_tx=len(transactions)
    '''
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchall()
    transactions_count=current_tx[0]
    tx_count=transactions_count[0]
    
    if tx_count is None or total_current_tx > tx_count:
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        email_id=email[0]
        if email_id is not None:
            message = Mail(
                from_email=Sendgrid_default_mail,
                to_emails="rasealex000000@gmail.com",
                subject='SafeName - New Transaction Notification In Your Account',
                html_content= '<h3> You got a new transaction on your BTC address</h3>')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            print("email is none")
    else:
        print("no new transaction")




    
    '''
    last_transaction = transactions[-1]
       
    tx_id = last_transaction['hash']
    frmm=last_transaction['inputs']
    frm=[]
    for trans in frmm:
        fro=trans['address']
        send=trans['value']
        frm.append({"from":fro,"send_amount":(int(send)/100000000)})
    transac=transaction['outputs']
    to=[]
    for too in transac:
        t = too['address'] 
        recive =too['value']
        to.append({"to":t,"receive_amount":(int(recive)/100000000)})
    timestamp =transaction['timestamp']
    dt_object = datetime.fromtimestamp(timestamp)
    array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    '''
    