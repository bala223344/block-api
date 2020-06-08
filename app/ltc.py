import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import LTC_balance,LTC_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,LTC_balance
from app.config import mydb



#----------Function for fetching tx_history and balance storing in mongodb----------

def ltc_data(address,symbol,type_id):
    ret=LTC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    data = response['data']

    doc=LTC_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions = res['data']['data']

    array=[]
    for transaction in transactions:
        if transaction:
            inputs = transaction['inputs']
            outputs =transaction['outputs']
            frm=[]
            for inpu in inputs:
                if inpu:
                    prev_value=inpu['prev_value']
                    if "prev_addresses" in inpu:
                        prev_addresses=inpu['prev_addresses']
                        for pre in prev_addresses:
                            frm.append({"from":pre,"send_amount":prev_value})
            to=[]
            for out in outputs:
                if out:    
                    value=out['value']
                    if "addresses" in out:   
                        addresses=out['addresses']
                        for addr in addresses:
                            to.append({"to":addr,"receive_amount":value})
            fee =transaction['income']
            timestamp = transaction['time']
            conver_d = int(timestamp)
            dt_object = datetime.fromtimestamp(conver_d)
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = data['balance']
    amount_recived =data['total_receive']
    amount_sent =data['total_send']

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
    




#----------Function for send notification if got new one transaction movement----------

def ltc_notification(address,symbol,type_id):
    ret=LTC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()  
    datta = transaction['data']
    total_current_tx=datta['tx_count']  
    mycursor = mydb.cursor()
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchone()
    tx_count=current_tx[0]

    if tx_count is None or int(total_current_tx) > int(tx_count):
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
                html_content= '<h3> You got a new transaction on your LTC address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            print("email is none")
    else:
        print("no new transaction")

