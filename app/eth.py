import requests
from flask import jsonify
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import mongo
from app.config import ETH_balance,ETH_internal_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import ETH_transactions
from app.config import mydb,mycursor,Sendgrid_default_mail,SendGridAPIClient_key



#----------Function for fetching tx_history and balance for ETH storing in mongodb----------

def eth_data(address,symbol,type_id):
    ret=ETH_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ETH_transactions.replace("{{address}}",''+address+'')
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
        too=transaction['to']
        send_amount=transaction['value']
        if send_amount != "0":
            tx_id = transaction['hash']
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":str(int(send_amount)/1000000000000000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
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
                "balance":(int(balance)/1000000000000000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    internal_transact = eth_data_internal(address,symbol,type_id)
    return jsonify({"status":"success"})




def eth_data_internal(address,symbol,type_id):
    ret=ETH_internal_transactions.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    transactions=response['result']
    array=[]

    for transaction in transactions:
        frm=[]
        to=[]
        fee =""
        timestamp = transaction['timeStamp']
        first_date=int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)   
        fro =transaction['from']
        if 'to' in transaction:
            too=transaction['to']
        else:
            too=""
        send_amount=transaction['value']
        if send_amount != "0":
            tx_id = transaction['hash']
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":str(int(send_amount)/1000000000000000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id,"internal_transaction":True})
    for arra in array:
        ret = mongo.db.sws_history.update({
            "address":address            
        },{'$push': {'transactions': arra}},upsert=False)
    




#----------Function for fetching tx_history and balance for ETH storing in mongodb----------

def eth_notification(address,symbol,type_id):    
    doc=ETH_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()  
    transactions=res['result']
    if transactions:
        total_current_tx=len(transactions)
        transaction = transactions[-1]
        timestamp = transaction['timeStamp']
        first_date=int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        fro =transaction['from']
        too=transaction['to']
        send_amount=(int(transaction['value'])/1000000000000000000)
        tx_id = transaction['hash']
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchall()
        transactions_count=current_tx[0]
        tx_count=transactions_count[0]
        if tx_count is None or total_current_tx > tx_count:
            if send_amount != 0:
                mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
                mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
                email = mycursor.fetchone()
                email_id=email[0]
                
                if email_id is not None:    
                    frm_safename=fro
                    to_safename=too
                    message = Mail(
                            from_email=Sendgrid_default_mail,
                            to_emails=email_id,
                            subject='SafeName - New Transaction Notification In Your Account',
                            html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(frm_safename) + ' </div><strong>To:</strong> ' + str(to_safename) + ' </div><div><strong>Amount:</strong> ' + str(send_amount) + ' </div><div><strong>Tx_id:</strong> ' + str(tx_id) + ' </div><div><strong>Coin Type:</strong> ''ETH''  </div>' )
                    sg = SendGridAPIClient(SendGridAPIClient_key)
                    response = sg.send(message)
                    print(response.status_code, response.body, response.headers)
                else:
                    print("email is not none")
            else:
                print("amount is 0")
        else:
            print("no new transaction")
    else:
        print("no transcations")














#return jsonify({"status":"success"})

'''
def eth_data(address,symbol,type_id):
    print("etheeeeeeeeeeeeeeeeeeeee")
    ret=ETH_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ETH_transactions.replace("{{address}}",''+address+'')
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
        too=transaction['to']
        send_amount=transaction['value']
        if send_amount == "0":
            print(send_amount)
            tx_id = transaction['hash']
            print(tx_id)
            docc=ETH_internal_transactions.replace("{{hash}}",''+tx_id+'')
            internal_response_user = requests.get(url=docc)
            ress = internal_response_user.json()  
            print("response",ress)
            print("from:",fro,"and","to:",too)
            message = ress['message']
            if message == 'OK':
                result = ress['result']   
                resul = result[0]
                frrr = resul['from']
                tooo = resul['to'] 
                value = resul['value']
                timeSta = resul['timeStamp']
                first_dae=int(timeSta)
                dt_obj = datetime.fromtimestamp(first_dae)
                to.append({"to":tooo,"receive_amount":""})
                frm.append({"from":frrr,"send_amount":str(int(value)/1000000000000000000)})
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_obj,"Tx_id":tx_id,"internal_transaction":True})
            else:
                pass
        else:
            print("elseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            print(send_amount)
            tx_id = transaction['hash']
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":str(int(send_amount)/1000000000000000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    print(len(array))
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
                "balance":(int(balance)/1000000000000000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify({"status":"success"})
'''


