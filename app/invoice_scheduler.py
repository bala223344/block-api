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



#-------Scheduler for invoice moving-------

def invoice_moving():
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
            "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":str(to),"send_amount":amount}},"to":{'$elemMatch':{"to":str(frm)}}}}
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
        

#-------Scheduler for invoice notifications-------

def invoice_notification_interval():
    dab = mongo.db.sws_pending_txs_from_app.find({
        "type":"invoice"})
    dab = [serialize_doc(doc) for doc in dab]
    for data in dab:
        frm=data['from']
        to = data['to']
        symbol = data['symbol']
        amount=data['amt']
        created_at = data['created_at']
        notes = data['from_notes']
        to_username = data['to_username']
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(to)+'"')
        email = mycursor.fetchone()
        if email[0]:
            email_id=email[0]
            if email_id is not None:
                msg = '<h3> You have a pendig invoice request for {{notes}}</h3><strong>Date:</strong> ' + str(created_at) +' <div><strong>From:</strong> ' + str(frm) + ' </div><strong>To:</strong> ' + str(to) + ' </div><div><strong>Amount:</strong> ' + str(amount) + ' </div><div><strong>coin:</strong> ' + str(symbol) + ' </div>'
                massegee = msg.replace("{{notes}}",''+notes+'')
                message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails=email_id,
                        subject='SafeName - Invoice Notification In Your Account', 
                        html_content= massegee)
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)
            else:
                pass
        else:
            pass








'<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(frm_safename) + ' </div><strong>To:</strong> ' + str(to_safename) + ' </div><div><strong>Amount:</strong> ' + str(send_amount) + ' </div><div><strong>Tx_id:</strong> ' + str(tx_id) + ' </div><div><strong>Coin Type:</strong> ''ETH''  </div>'



'''
else:
            mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(to)+'"')
            email = mycursor.fetchone()
            if email[0]:
                email_id=email[0]
                if email_id is not None:
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
                else:
                    pass
            else:
                pass
'''


