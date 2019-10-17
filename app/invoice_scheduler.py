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
    print("invoice schedulerrrrrrrrrrrrrrrrr")
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
        dabb = mongo.db.sws_history.find({
            "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":to,"send_amount":amount}}, "to":{'$elemMatch':{"to":frm}}}}
        },{"transactions.$": 1 })
        dabb=[serialize_doc(doc) for doc in dabb]
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
            print("elseeeeeeeeeeee")
            mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(to)+'"')
            email = mycursor.fetchone()
            if email is not None:
                email_id=email[0]
                msg = '<h3> You have a pendig invoice request for {{notes}}</h3>'
                massegee = msg.replace("{{notes}}",''+notes+'')
                message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails=email_id,
                        subject='SafeName - Invoice Notification In Your Account', 
                        html_content= massegee)
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)

