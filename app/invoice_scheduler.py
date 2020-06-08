import requests
from flask import (
    Blueprint,request,jsonify,abort
)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import mydb,Sendgrid_default_mail,SendGridAPIClient_key
from app import mongo
import datetime
from app.util import serialize_doc

from app.transactions_util import eth_data
from app.transactions_util import btc_data
from app.transactions_util import zrx_data
from app.transactions_util import elf_data
from app.transactions_util import ae_data
from app.transactions_util import rep_data
from app.transactions_util import aoa_data
from app.transactions_util import bat_data
from app.transactions_util import bnb_data
from app.transactions_util import btc_cash_data
from app.transactions_util import btc_gold_data
from app.transactions_util import bitcoin_svs_data
from app.transactions_util import btt_data
from app.transactions_util import link_data
from app.transactions_util import cccx_data
from app.transactions_util import mco_data
from app.transactions_util import cro_data
from app.transactions_util import dai_data
from app.transactions_util import dash_data
from app.transactions_util import ekt_data
from app.transactions_util import egt_data
from app.transactions_util import enj_data
from app.transactions_util import eos_data
from app.transactions_util import gnt_data
from app.transactions_util import ht_data
from app.transactions_util import icx_data
from app.transactions_util import inb_data
from app.transactions_util import iota_data
from app.transactions_util import kcs_data
from app.transactions_util import lamb_data
from app.transactions_util import ltc_data
from app.transactions_util import mkr_data
from app.transactions_util import ont_data
from app.transactions_util import qtum_data
from app.transactions_util import xrp_data
from app.transactions_util import usdc_data
from app.transactions_util import xtz_data
from app.transactions_util import tron_data
from app.transactions_util import vet_data
from app.transactions_util import zcash_data
from app.transactions_util import gpl_data
from app.transactions_util import matic_data

#--scheduler for safename verification payment--

def safename_verification():
    dab = mongo.db.sws_pending_txs_from_app.find({
        "type":"verification"})
    dab = [serialize_doc(doc) for doc in dab]
    for data in dab:
        frm=data['from']
        to = data['to']
        symbol = data['symbol']
        amount=data['amt']
        notes = data['from_notes']
        from_username = data['from_username']
        type_id = data['type_id']
        tx_type = data['type']
        is_erc20 = data['is_erc20']
        
        #check destination
        if is_erc20 == 1:
            fetch_history(to,symbol,"1")
        else:
            fetch_history(to,symbol,type_id)


        #some doesn't have a receive_amt
        if is_erc20 == 1 or type_id == "1" or type_id == "35" :
        #     print({
        #         "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":str(frm).lower(),"send_amount":str(amount)}},"to":{'$elemMatch':{"to":str(to).lower()}}}}
        #     ,
        # "address":str(to) },{"transactions.$": 1 })
        
            dabb = mongo.db.sws_history.find({
                "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":str(frm).lower(),"send_amount":str(amount)}},"to":{'$elemMatch':{"to":str(to).lower()}}}}
            ,
        "address":str(to) },{"transactions.$": 1 })
        else :
        #other coins 
         # for coins with split amount, it doesn't matter what amt they sent..just confirm   
            if type_id == "2" or type_id == "75":
               # print ('ok 75')
    #             print ({
    #            "transactions": {'$elemMatch': {"from":{'$elemMatch':
    #            {"from":str(frm)}},"to":{'$elemMatch':
    #            {"to":str(to)}}}}
    #        ,
    #    "address":str(to) }) 
         
                dabb = mongo.db.sws_history.find({
                "transactions": {'$elemMatch': {"from":{'$elemMatch':
                {"from":str(frm)}},"to":{'$elemMatch':
                {"to":str(to)}}}}
            ,
            "address":str(to) },{"transactions.$": 1 })

 

          #need to match exact amt  
            else :  
                dabb = mongo.db.sws_history.find({
                "transactions": {'$elemMatch': {"from":{'$elemMatch':
                {"from":str(frm)}},"to":{'$elemMatch':
                {"to":str(to),"receive_amount":  str(amount)}}}}
            ,
        "address":str(to) },{"transactions.$": 1 })




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
                "type":"verification"
            }) 

            report = mongo.db.sws_notes.insert_one({
                "tx_id": transaction_id,
                "notes": notes,
                "from": frm,
                "to": to,
                "type":tx_type,
                "username":from_username,
                "update_at":datetime.datetime.now(),
                "created_at":datetime.datetime.now()
            }).inserted_id
        
            #update the address as verified
            if tx_type == 'verification':
                 mycursor = mydb.cursor()
                 #print ('UPDATE sws_address SET address_status ="verified" WHERE address = "'+str(frm)+'" AND type_id = '+type_id+' AND cms_login_name =  "'+str(from_username)+'"')
                 mycursor.execute('UPDATE sws_address SET address_status ="verified" WHERE address = "'+str(frm)+'" AND type_id = '+type_id+' AND cms_login_name =  "'+str(from_username)+'"' )

                #delete other records added and still waiting for verified..because now this is verifed
                 mycursor.execute('DELETE FROM sws_address WHERE address_status ="unverified" AND address = "'+str(frm)+'" AND type_id = '+type_id )
                  

                 #send a mail
                 mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(frm)+'"')
                 email = mycursor.fetchone()
                 mycursor.close()
                 if email[0]:
                    email_id=email[0]
                    if email_id is not None:
                        msg = ' Your address  <h3>' + str(frm) +'</h3>   is now verified <div><strong>coin:</strong> ' + str(symbol) + ' </div>'
                        message = Mail(
                                from_email=Sendgrid_default_mail,
                                to_emails=email_id,
                                subject='SafeName - Address verification done', 
                                html_content= msg)
                        sg = SendGridAPIClient(SendGridAPIClient_key)
                        response = sg.send(message)
                        print(response.status_code, response.body, response.headers)
                    else:
                        pass
                 else:
                   pass




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
        from_username = data['from_username']
        type_id = data['type_id']
        tx_type = data['type']

   
        #press: fetch latest tx and put it in sws_history..or else we will not have the latest txs until someone hit POST /transaction    
      
        fetch_history(to,symbol,type_id)
        dabb = mongo.db.sws_history.find({
            "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":str(to),"send_amount":str(amount)}},"to":{'$elemMatch':{"to":str(frm)}}}}
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
                "type":tx_type,
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
        mycursor = mydb.cursor()
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(to)+'"')
        email = mycursor.fetchone()
        mycursor.close()
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


def fetch_history(address,symbol,type_id):
    if type_id == "1":
        currency = eth_data(address,symbol,type_id)
        
    if type_id == "2":
        currency = btc_data(address,symbol,type_id)
        
    if type_id == "3":
        currency = zrx_data(address,symbol,type_id)
        
    if type_id == "5":
        currency = elf_data(address,symbol,type_id)
        
    if type_id == "6":
        currency = ae_data(address,symbol,type_id)
        
    if type_id == "8":
        currency = rep_data(address,symbol,type_id)
        
    if type_id == "9":
        currency = aoa_data(address,symbol,type_id)
        
    if type_id == "10":
        currency = bat_data(address,symbol,type_id)
        
    if type_id == "11":
        currency = bnb_data(address,symbol,type_id)
        
    if type_id == "12":
        currency = btc_cash_data(address,symbol,type_id)
        
    if type_id == "14":
        currency = btc_gold_data(address,symbol,type_id)
        
    if type_id == "15":
        currency = bitcoin_svs_data(address,symbol,type_id)
        
    if type_id == "17":
        currency = btt_data(address,symbol,type_id)            

    if type_id == "21":
        currency = link_data(address,symbol,type_id)
        
    if type_id == "22":
        currency = cccx_data(address,symbol,type_id)
        
    if type_id == "24":
        currency = mco_data(address,symbol,type_id)
        
    if type_id == "25":
        currency = cro_data(address,symbol,type_id)
        
    if type_id == "26":
        currency = dai_data(address,symbol,type_id)
        
    if type_id == "27":
        currency = dash_data(address,symbol,type_id)
        
    if type_id == "31":
        currency = ekt_data(address,symbol,type_id)
        
    if type_id == "32":
        currency = egt_data(address,symbol,type_id)
        
    if type_id == "34":
        currency = enj_data(address,symbol,type_id)
        
    if type_id == "35":  
        currency = eos_data(address,symbol,type_id)
        
    if type_id == "38":
        currency = gnt_data(address,symbol,type_id)
        
    if type_id == "42":
        currency = ht_data(address,symbol,type_id)
        
    if type_id == "44":
        currency = icx_data(address,symbol,type_id)
        
    if type_id == "45":
        currency = inb_data(address,symbol,type_id)
        
    if type_id == "47":
        currency = iota_data(address,symbol,type_id)
        
    if type_id == "50":
        currency = kcs_data(address,symbol,type_id)
        
    if type_id == "51":
        currency = lamb_data(address,symbol,type_id)
        
    if type_id == "53":
        currency = ltc_data(address,symbol,type_id)
        
    if type_id == "55":
        currency = mkr_data(address,symbol,type_id)
        
    if type_id == "67":
        currency = ont_data(address,symbol,type_id)
        
    if type_id == "70":
        currency = qtum_data(address,symbol,type_id)
        
    if type_id == "75":
        currency = xrp_data(address,symbol,type_id)
        
    if type_id == "83":
        currency = usdc_data(address,symbol,type_id)
        
    if type_id == "84":
        currency = xtz_data(address,symbol,type_id)
        
    if type_id == "87":
        currency = tron_data(address,symbol,type_id)
        
    if type_id == "91":
        currency = vet_data(address,symbol,type_id)
        
    if type_id == "98":
        currency = zcash_data(address,symbol,type_id)
        
    if type_id == "101":
        currency = gpl_data(address,symbol,type_id)
        
    if type_id == "102":
        print("Matic")
        currency = matic_data(address,symbol,type_id)





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


