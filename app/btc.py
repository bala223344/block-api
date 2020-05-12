import requests
from flask import jsonify
import datetime
from app.config import BTC_balance
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BTC_balance
from app.config import mydb,mycursor
from app import mongo
import numpy as np

BTC_sync_balance="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start={{block}}&limit=50"


#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def btc_data(address,symbol,type_id):
    ret=BTC_balance.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    response_user_token = requests.get(url=ret1)
    transaction = response_user_token.json()       
    
    if symbol == "BTC":
        balance =transaction['balance']
        amountReceived =transaction['amount_received']
        amountSent =transaction['amount_sent']
        transactions = transaction['txs']
        array=[]
        for transaction in transactions:
            fee=transaction['fee']
            tx_id = transaction['hash']
            frmm=transaction['inputs']
            frm=[]
            for trans in frmm:
                fro=trans['address']
                send=trans['value']
                frm.append({"from":fro,"send_amount":str(int(send)/100000000)})
            transac=transaction['outputs']
            to=[]
            for too in transac:
                t = too['address'] 
                recive =too['value']/100000000
               
                to.append({"to":t,"receive_amount": np.format_float_positional(recive)})
            timestamp =transaction['timestamp']
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/100000000),
                "transactions":array,
                "amountReceived":(int(amountReceived)/100000000),
                "amountSent":(int(amountSent)/100000000)
            }},upsert=True)
    return jsonify({"status":"success"})




#----------Function for send notification if got new one----------

def btc_notification(address,symbol,type_id):
    print("btc_notification")
    ret=BTC_balance.replace("{{address}}",''+address+'')
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
                html_content= '<h3> You got a new transaction on your BTC address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            pass
    else:
        pass



#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def btc_data_sync():
    mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(2)+'"')
    current_tx = mycursor.fetchall()
    current_tx = ["1416bVmA8Wwd3GGGA9W3kgmWiJTota7U62","18xmAHjjsTe8FJ6PAKAL5TxBc4Ypewo6q3","1BPnQZhMzVmM2Rnhs9YpRf8kJvBAzaUcAt","1EAECn7nzqMbk7FD3qa1dvbYkWj58iSV69","1GQhVHcghcNrgdvuWqzHxM3Ln23hxfqpvX","1JDSPz2rsfwNixJzc8pWBQx5v7b4wr5equ","1LP5s5m1VVXd59AYzdjcDLm4Rz1Duw1s2v","3NxLx7v8N2uA1HA4z7cncYVMcjKakqBmm9"]
    for addresses in current_tx:
        address = addresses[0]
        Recblocks = mongo.db.dev_sws_history.find_one({"address":address,"type_id":"2"})
        if Recblocks is not None:
            block = Recblocks['block']
        else:
            block = 1
        ret=BTC_sync_balance.replace("{{address}}",''+address+'')
        ret1=ret.replace("{{block}}",''+str(block)+'')
        response_user_token = requests.get(url=ret1)
        transaction = response_user_token.json()       
        
        balance =transaction['balance']
        amountReceived =transaction['amount_received']
        amountSent =transaction['amount_sent']
        transactions = transaction['txs']
        array=[]
        for transaction in transactions:
            fee=transaction['fee']
            tx_id = transaction['hash']
            frmm=transaction['inputs']
            frm=[]
            for trans in frmm:
                fro=trans['address']
                send=trans['value']
                frm.append({"from":fro,"send_amount":str(int(send)/100000000)})
            transac=transaction['outputs']
            to=[]
            for too in transac:
                t = too['address'] 
                recive =too['value']/100000000
            
                to.append({"to":t,"receive_amount": np.format_float_positional(recive)})
            timestamp =transaction['timestamp']
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
        if array:
            block = block+len(array)
        ret = mongo.db.dev_sws_history.update({
            "address":address            
        },{
            "$set":{    
                    "address":address,
                    "symbol":"BTC",
                    "type_id":"2",
                    "block":int(block),
                    "date_time":datetime.datetime.utcnow(),
                    "balance":(int(balance)/100000000),
                    "amountReceived":(int(amountReceived)/100000000),
                    "amountSent":(int(amountSent)/100000000)
                }},upsert=True)
        if array:
            for listobj in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address            
                },{
                    "$push":{    
                            "transactions":listobj}})

















'''
def btc_data(address,symbol,type_id):
    ret=BTC_balance.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    data = response['data']
    addr =data[''+address+'']
    add =addr['address']
    balance =add['balance']
    bal = (balance/100000000)
    receive_amount=add['received']
    send_amount=add['spent']
    transactions=addr['transactions']
    array=[]
    for tran in transactions:
        doc=BTC_transactions.replace("{{address}}",''+tran+'')
        response_user = requests.get(url=doc)
        res = response_user.json()       
        trs =res['data'][''+tran+'']
        inputs=trs['inputs']
        outputs=trs['outputs']
        transact=trs['transaction']
        fee =transact['fee']
        time =transact['time']

        frm=[]
        for inp in inputs:
            recipient = inp['recipient']
            value=inp['value']
            frm.append({"from":recipient,"send_amount":(value/100000000)})
        to=[]
        for out in outputs:
            recipient1 = out['recipient']
            value1=out['value']
            to.append({"to":recipient1,"receive_amount":(value1/100000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":time})

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":bal,
                "transactions":array,
                "amountReceived":(receive_amount/100000000),
                "amountSent":(send_amount/100000000)
            }},upsert=True)
    return jsonify({"status":"success"})


'''
'''


def btc_data(address,symbol,type_id):
    print("ashgajhghgggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_trans" in records:
        url1=records['url_trans']
    ret=url.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    response_user_token = requests.get(url=ret1)
    transaction = response_user_token.json()       
    
    if symbol == "BTC":
        balance =transaction['balance']
        amountReceived =transaction['amount_received']
        amountSent =transaction['amount_sent']
        transactions = transaction['txs']
        array=[]
        total_current_tx=len(transactions)
        for transaction in transactions:
            fee=transaction['fee']
            tx_id = transaction['hash']
            frmm=transaction['inputs']
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
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/100000000),
                "transactions":array,
                "amountReceived":(int(amountReceived)/100000000),
                "amountSent":(int(amountSent)/100000000)
            }},upsert=True)
    mycursor.execute('SELECT tx_notification_preferred FROM sws_address WHERE address="'+str(address)+'"')
    sws_addresses = mycursor.fetchall()
    preffered_value = sws_addresses[0]
    value_check = preffered_value[0]
    if value_check == 1:
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchall()
        transactions_count=current_tx[0]
        tx_count=transactions_count[0]
        if tx_count is None or total_current_tx > tx_count:
            #latest_transaction=array[-1]
            #transaction_id = latest_transaction['Tx_id']
            #date = latest_transaction['date']
            #frm = latest_transaction['from']
            #too = latest_transaction['to']
            mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
            mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
            email = mycursor.fetchone()
            email_id=email[0]
            if email_id is not None:
                message = Mail(
                    from_email=Sendgrid_default_mail,
                    to_emails='rasealex000000@gmail.com',
                    subject='SafeName - New Transaction Notification In Your Account',
                    html_content= '<h3> You got a new transaction </h3>')
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)
            else:
                print("email is none")
        else:
            print("no new transaction")
        return "success"
    return "success"



'''
























'''
def btc_cash_data(address,symbol,type_id):
    ret=BCH_balance.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    data = response['data']
    addr =data[''+address+'']
    add =addr['address']
    balance =add['balance']
    bal = (balance/100000000)
    receive_amount=add['received']
    send_amount=add['spent']
    transactions=addr['transactions']
    array=[]
    for tran in transactions:
        doc=BCH_transactions.replace("{{address}}",''+tran+'')
        response_user = requests.get(url=doc)
        res = response_user.json()       
        trs =res['data'][''+tran+'']
        inputs=trs['inputs']
        outputs=trs['outputs']
        transact=trs['transaction']
        fee =transact['fee']
        time =transact['time']

        frm=[]
        for inp in inputs:
            recipient = inp['recipient']
            value=inp['value']
            frm.append({"from":recipient,"send_amount":(value/100000000)})
        to=[]
        for out in outputs:
            recipient1 = out['recipient']
            value1=out['value']
            to.append({"to":recipient1,"receive_amount":(value1/100000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":time})

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":bal,
                "transactions":array,
                "amountReceived":(receive_amount/100000000),
                "amountSent":(send_amount/100000000)
            }},upsert=True)
    return jsonify({"status":"success"})


'''