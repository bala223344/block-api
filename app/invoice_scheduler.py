import requests
from flask import (
    Blueprint,request,jsonify,abort
)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import mydb,mycursor,Sendgrid_default_mail,SendGridAPIClient_key
from app import mongo
import datetime
from app.util import serialize_doc



#-------Scheduler for invoice notifications-------

def invoice_notification():
    print("asdasndas,na")
    dab = mongo.db.sws_pending_txs_from_app.find({
        "type":"invoice"})
    dab = [serialize_doc(doc) for doc in dab]
    for data in dab:
        frm=data['from']
        to = data['to']
        symbol = data['symbol']
        amount=data['amt']
        notes = data['from_notes']
        to_username = data['to_username']
        print("from")
        print(frm)
        print("to")
        print(to)
        print(amount)
        dabb = mongo.db.sws_history.find({
            "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":to,"send_amount":amount}}, "to":{'$elemMatch':{"to":frm}}}}
        },{"transactions.$": 1 })
        dabb=[serialize_doc(doc) for doc in dabb]
        print(dabb)
        if dabb:
            for data in dabb:
                trans = data['transactions']
                for tx_id in trans:
                    transaction_id = tx_id['Tx_id']
            
            docs = mongo.db.sws_pending_txs_from_app.remove({
                "from": frm,
                "to": to,
                "amt": amount,
                "type":"invoice"
            }) 
                       
            report = mongo.db.sws_notes.insert_one({
                "tx_id": transaction_id,
                "notes": notes,
                "from": frm,
                "to": to,
                "type":"invoice",
                "username":to_username,
                "update_at":datetime.datetime.now(),
                "created_at":datetime.datetime.now()
            }).inserted_id
        else:
            mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(to)+'"')
            email = mycursor.fetchone()
            print(email)
            if email is not None:
                email_id=email[0]
                print(email_id)
                message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - Invoice Notification In Your Account',
                        html_content= '<h3> Your invoice is not clear please accept the request</h3>')
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)


'''
{"transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":"0xe85dA0b7510F497978801A129638E0f2b4449C09","send_amount":"1.5"}}, "to":{'$elemMatch':{"to":"0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b"}}}}}

to = 0xe85dA0b7510F497978801A129638E0f2b4449C09
frm = 0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b
'''