import requests
from flask import jsonify
from datetime import datetime
from app.config import ZEC_balance,ZEC_transactions
from app import mongo
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BTC_balance
from app.config import mydb
from sendgrid import SendGridAPIClient



#----------Function for fetching tx_history and balance storing in mongodb----------

def zcash_data(address,symbol,type_id):
    print("zcash_data_zcash") 
    ret=ZEC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ZEC_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    array=[]
    for transaction in res:
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        vin = transaction['vin']
        vout= transaction['vout']
        frm=[]
        for v_in in vin:
            if v_in is not None:
                retrievedVout = v_in['retrievedVout']['scriptPubKey']
                val = v_in['retrievedVout']['value']
                if "addresses" in retrievedVout:
                    addresses=retrievedVout['addresses']
                    for h in addresses:
                        frm.append({"from":h,"send_amount":val})
        to=[]
        for v_out in vout:
            if v_out is not None:
                retrieved = v_out['scriptPubKey']['addresses']
                valu = v_out['value']
                for a in retrieved:
                    to.append({"to":a,"receive_amount":valu})

        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    balance = response['balance']
    amount_recived =response['totalRecv']
    amount_sent =response['totalSent']

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




#----------Function for send notification about transactions movement----------

def zcash_notification(address,symbol,type_id):
    ret=ZEC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    sent = response['sentCount']
    recv = response['recvCount']
    total_current_tx  = int(sent) + int(recv)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchall()
    transactions_count=current_tx[0]
    tx_count=transactions_count[0]
    if tx_count is None or int(total_current_tx) > tx_count:
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
                    html_content= '<h3> You got a new transaction on your ZEC address </h3><strong>Address:</strong> ' + str(address) +'' )
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
                print("email is not none")
    else:
        print("no new transaction")
