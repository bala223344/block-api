from flask import jsonify
import requests
from app import mongo
from app.config import ICX_balance,ICX_transactions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail
from app.config import mydb
import datetime

#----------Function for fetching tx_history and balance storing in mongodb also send notification if got new one----------

def icx_data(address,symbol,type_id):
    ret=ICX_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ICX_transactions.replace("{{address}}",''+address+'')
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
        dt_object = datetime.datetime.fromtimestamp(first_date)
        fro =transaction['from']
        too=transaction['to']
        send_amount=transaction['value']
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xb5a5f22694352c15b00323844ad545abb2b11028":
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
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


def icx_notification(address,symbol,type_id):
    doc=ICX_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()  
    transactions=res['result']
    tx_list = []
    for transaction in transactions:
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xb5a5f22694352c15b00323844ad545abb2b11028":
            tx_list.append({"transaction":"tx"})

    total_current_tx = len(tx_list)
    mycur = mydb()
    mycursor = mycur.cursor()
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchone()
    tx_count=current_tx[0]
    if tx_count is None or total_current_tx > tx_count:
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
                html_content= '<h3> You got a new transaction on your ICX address </h3><strong>Address:</strong> ' + str(address) +'')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            pass
    else:
        pass


def EmontDataSync():
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        }).distinct("address")
    mycur = mydb()
    mycursor = mycur.cursor()
    for address in addresses:
        array=[]
        ret=ICX_transactions.replace("{{address}}",''+address+'')
        response_user_token = requests.get(url=ret)
        response = response_user_token.json()       
        try:
            blocks = mongo.db.dev_sws_history.aggregate(
            [  
                {"$unwind" : "$transactions"},
                {
                    "$match": {
                        "address":address,
                        "type_id":"103"
                    }
                },
                {
                    "$group" : {
                        "_id" : "$_id",
                        "maxercblockNumber" : {"$max" : "$transactions.ercblockNumber"}
                    }
                }
            ])
            if blocks:
                block = blocks[0]
                if block['maxercblockNumber'] is not None:
                    StartBlock = block['maxercblockNumber'] + 1
                else:
                    StartBlock = 0
            else:
                StartBlock = 0
            EndBlock = 1
            doc=ICX_transactions.replace("{{address}}",''+address+'')
            StarBlockrepl=doc.replace("{{startblock}}",''+str(StartBlock)+'')
            EndBlockRep = StarBlockrepl.replace("{{endblock}}",''+str(EndBlock)+'')
            response_user = requests.get(url=EndBlockRep)
            res = response_user.json()
            transactions=res['result']
            for transaction in transactions:
                frm=[]
                to=[]
                fee =""
                try:
                    timestamp = transaction['timeStamp']
                except Exception:
                    timestamp = 0
                first_date=int(timestamp)
                dt_object = datetime.datetime.fromtimestamp(first_date)
                fro =transaction['from']
                too=transaction['to']
                send_amount=transaction['value']
                blockNumber = transaction['blockNumber']
                tx_id = transaction['hash']
                contractAddress = transaction['contractAddress']
                ErcContracts = ["0x95daaab98046846bf4b2853e23cba236fa394a31"]
                if contractAddress in ErcContracts:
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'" AND address_safename_enabled="yes"')
                    to_safename = mycursor.fetchone()
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'" AND address_safename_enabled="yes"')
                    from_safename = mycursor.fetchone()
                    mycursor.close()
                    to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":None})
                    frm.append({"from":fro,"send_amount":(float(send_amount)/100000000),"safename":from_safename[0] if from_safename else None,"openseaname":None})
                    array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"dt_object":dt_object,"Tx_id":tx_id,"is_erc20":True,"ercblockNumber":int(blockNumber)})
        except Exception:
            pass
        try:
            balance = response['result']
        except Exception:
            balance = 0
        amount_recived =""
        amount_sent =""
        try:
            bal = round((float(balance)/100000000),6)
        except Exception:
            bal = 0

        ret = mongo.db.dev_sws_history.update({
            "address":address,
            "type_id":"103"            
        },{
            "$set":{    
                    "address":address,
                    "symbol":"EMONT",
                    "type_id":"103",
                    "date_time":datetime.datetime.utcnow(),
                    "balance":bal,
                    "amountReceived":amount_recived,
                    "amountSent":amount_sent
                }},upsert=True)

        if array:
            for listobj in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address,
                    "type_id":"103"
                },{
                    "$push":{    
                            "transactions":listobj}})


