import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BSV_balance,BSV_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BSV_balance
from app.config import mydb,mycursor




#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def bitcoin_svs_data(address,symbol,type_id):
    ret=BSV_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    respon = response_user_token.json()  
    response = respon['data']

    doc=BSV_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       

    transactions=res['data']['data']

    array=[]
    for transaction in transactions:
        fee =transaction['income']
        timestamp = transaction['time']
        date = int(timestamp)
        dt_object = datetime.fromtimestamp(date)
        inputs=transaction['inputs']
        outputs=transaction['outputs']
        frm=[]
        for inpt in inputs:
            prev_address=inpt['prev_addresses']
            prev_value = inpt['prev_value']
            for frmm in prev_address:
                frm.append({"from":frmm,"send_amount":prev_value})
        to=[]
        for outp in outputs:
            addresses=outp['addresses']
            val =outp['value']
            for too in addresses:
                to.append({"to":too,"receive_amount":val})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})

    balance = response['balance']
    amount_recived =response['total_receive']
    amount_sent =response['total_send']

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":balance,
                "amountReceived":amount_recived,
                "amountSent":amount_sent,
                "transactions":array
            }},upsert=True)

    return jsonify({"status":"success"})




#-----------Function for send notification about transactions movement------------

def bsv_notification(address,symbol,type_id):
    print("bsv_notification")
    ret=BSV_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()  
    total_current_tx=transaction['data']['tx_count'] 
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchone()
    tx_count=current_tx[0]
    if tx_count is None or int(total_current_tx) > tx_count:
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        email_id=email[0]
        if email_id is not None:
            message = Mail(
                from_email=Sendgrid_default_mail,
                to_emails=email_id,
                subject='SafeName - New Transaction Notification In Your Account',
                html_content= '<h3> You got a new transaction on your BSV address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            pass
    else:
        pass
