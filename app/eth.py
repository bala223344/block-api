from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import mongo
from app.config import SendGridAPIClient_key,Sendgrid_default_mail

import mysql.connector
mydb = mysql.connector.connect(host='198.38.93.150',user='dexter',password='cafe@wales1',database='db_safename',auth_plugin='mysql_native_password')
mycursor=mydb.cursor()




def eth_data(address,symbol,type_id):
    print("asdsadsadasdadaasd")
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['result']
    total_current_tx=len(transactions)
    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        fee =""
        timestamp = transaction['timeStamp']
        first_date=int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        fro =transaction['from']
        too=transaction['to']
        send_amount=transaction['value']
        tx_id = transaction['hash']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    
    balance = response['result']
    amount_recived =""
    amount_sent =""
    '''
    ret = mongo.db.address.update({
            "address":address            
        },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id
            }},upsert=True)

    ret = mongo.db.address.find_one({
        "address":address
    })
    _id=ret['_id']
    '''
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                #"record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/1000000000000000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    mycursor.execute('SELECT tx_notification_preferred FROM sws_address WHERE address="'+str(address)+'"')
    sws_addresses = mycursor.fetchall()
    preffered_value = sws_addresses[0]
    value_check = preffered_value[0]
    if value_check == 1:
        print("87")
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchall()
        transactions_count=current_tx[0]
        tx_count=transactions_count[0]
        if tx_count is None or total_current_tx > tx_count:
            print("93")
            latest_transaction=array[-1]
            transaction_id = latest_transaction['Tx_id']
            date = latest_transaction['date']
            frm = latest_transaction['from']
            to = latest_transaction['to']
            for frm_address in frm:
                from_addr = frm_address['from']
                send_amou = frm_address['send_amount']
            for to_address in to:
                to_addr = to_address['to']
            print(send_amou)
            if send_amou != 0:  
                print("105")
                mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
                print(address)
                mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
                email = mycursor.fetchone()
                email_id=email[0]
                print(email_id) 
                if email_id is not None:
                    print("sendinnnnnngggggggg")
                    message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - New Transaction Notification In Your Account',
                        html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(date) +' <div><strong>From:</strong> ' + str(from_addr) + ' </div><strong>To:</strong> ' + str(to_addr) + ' </div><div><strong>Amount:</strong> ' + str(send_amou) + ' </div><div><strong>Tx_id:</strong> ' + str(transaction_id) + ' </div><div><strong>Coin Type:</strong> ''ETH''  </div>' )
                    sg = SendGridAPIClient(SendGridAPIClient_key)
                    response = sg.send(message)
                    print(response.status_code, response.body, response.headers)
                else:
                    print("email is none")
            else:
                print("amount is 0")
        else:
            print("no new transaction")


            
    #SELECT a.cms_login_name, u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address=''; 
                #SELECT a.cms_login_name, u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address='0xa6fe83Dcf28Cc982818656ba680e03416824D5E4';