import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import BTC_GOLD_balance,BTC_GOLD_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail
from app.config import mydb,mycursor



#----------Function for fetching tx_history and balance storing in mongodb ----------

def btc_gold_data(address,symbol,type_id):
    ret=BTC_GOLD_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=BTC_GOLD_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions = res['txs']
    array=[]
    
    for transaction in transactions:
        fee =transaction['fees']
        timestamp = transaction['time']
        dt_object = datetime.fromtimestamp(timestamp)
        transfers=transaction['vin']
        vout = transaction['vout']
        frm=[]
        for v_in in transfers:
            amount = v_in['value']
            fro = v_in['addr']
            frm.append({"from":fro,"send_amount":amount})
        to=[]
        for v_out in vout:
            scriptPubKey =v_out['scriptPubKey']
            recv_amount =v_out['value']
            if "addresses" in scriptPubKey:
                adrr =scriptPubKey['addresses']
                for addre in adrr:
                    to.append({"to":addre,"receive_amount":recv_amount})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']
    balance = response['balance']
                
    
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



def btg_notification(address,symbol,type_id):
    print("btc_notification")
    ret=BTC_GOLD_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()  
    total_current_tx=transaction['txApperances']
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
                html_content= '<h3> You got a new transaction on your BTG address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            pass
    else:
        pass

