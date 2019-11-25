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
from app.btc import btc_data
from app.eth import eth_data,eth_data_internal
from app.bnb import bnb_data
from app.bch import btc_cash_data
from app.bsv import bitcoin_svs_data
from app.ltc import ltc_data
from app.tether import tether_data
from app.xtz import xtz_data
from app.qtum import qtum_data
from app.tron import tron_data
from app.mkr import mkr_data
from app.btt import btt_data
from app.vet import vet_data
from app.cro import cro_data
from app.xrp import xrp_data
from app.eos import eos_data
from app.dash import dash_data
from app.usdc import usdc_data
from app.ont import ont_data
from app.bat  import bat_data
from app.zcash import zcash_data
from app.btg import btc_gold_data
from app.iota import iota_data
from app.leo import unus_sed_leo_data
from app.icx import icx_data
from app.ae import ae_data
from app.btm import btm_data
from app.link import link_data
from app.zrx import zrx_data
from app.elf import elf_data
from app.rep import rep_data
from app.aoa import aoa_data
from app.cccx import cccx_data
from app.mco import mco_data
from app.cro import cro_data
from app.dai import dai_data
from app.ekt import ekt_data
from app.egt import egt_data
from app.enj import enj_data
from app.gnt import gnt_data
from app.ht import ht_data
from app.inb import inb_data
from app.kcs import kcs_data
from app.lamb import lamb_data
from app.gpl import gpl_data
from app.matic import matic_data


#-------Scheduler for invoice moving-------

def invoice_moving():

    dab = mongo.db.sws_pending_txs_from_app.find()
    #{        "type":"invoice"}
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
        address = frm
        #press: fetch latest tx and put it in sws_history..or else we will not have the latest txs until someone hit POST /transaction    
        # if type_id == "1":
        #     currency = eth_data(address,symbol,type_id)
            

        # if type_id == "2":
        #     currency = btc_data(address,symbol,type_id)
            

        # if type_id == "3":
        #     currency = zrx_data(address,symbol,type_id)
            

        # if type_id == "5":
        #     currency = elf_data(address,symbol,type_id)
            

        # if type_id == "6":
        #     currency = ae_data(address,symbol,type_id)
            

        # if type_id == "8":
        #     currency = rep_data(address,symbol,type_id)
            

        # if type_id == "9":
        #     currency = aoa_data(address,symbol,type_id)
            

        # if type_id == "10":
        #     currency = bat_data(address,symbol,type_id)
            

        # if type_id == "11":
        #     currency = bnb_data(address,symbol,type_id)
            

        # if type_id == "12":
        #     currency = btc_cash_data(address,symbol,type_id)
            

        # if type_id == "14":
        #     currency = btc_gold_data(address,symbol,type_id)
            

        # if type_id == "15":
        #     currency = bitcoin_svs_data(address,symbol,type_id)
            

        # if type_id == "17":
        #     currency = btt_data(address,symbol,type_id)
            

        # if symbol == "19":     
        #     currency = btm_data(address,symbol,type_id)
            

        # if type_id == "21":
        #     currency = link_data(address,symbol,type_id)
            

        # if type_id == "22":
        #     currency = cccx_data(address,symbol,type_id)
            

        # if type_id == "24":
        #     currency = mco_data(address,symbol,type_id)
            

        # if type_id == "25":
        #     currency = cro_data(address,symbol,type_id)
            

        # if type_id == "26":
        #     currency = dai_data(address,symbol,type_id)
            

        # if type_id == "27":
        #     currency = dash_data(address,symbol,type_id)
            

        # if type_id == "31":
        #     currency = ekt_data(address,symbol,type_id)
            

        # if type_id == "32":
        #     currency = egt_data(address,symbol,type_id)
            

        # if type_id == "34":
        #     currency = enj_data(address,symbol,type_id)
            

        # if type_id == "35":  
        #     currency = eos_data(address,symbol,type_id)
            

        # if type_id == "38":
        #     currency = gnt_data(address,symbol,type_id)
            

        # if type_id == "42":
        #     currency = ht_data(address,symbol,type_id)
            

        # if type_id == "44":
        #     currency = icx_data(address,symbol,type_id)
            

        # if type_id == "45":
        #     currency = inb_data(address,symbol,type_id)
            

        # if type_id == "47":
        #     currency = iota_data(address,symbol,type_id)
            

        # if type_id == "50":
        #     currency = kcs_data(address,symbol,type_id)
            

        # if type_id == "51":
        #     currency = lamb_data(address,symbol,type_id)
            

        # if type_id == "53":
        #     currency = ltc_data(address,symbol,type_id)
            

        # if type_id == "55":
        #     currency = mkr_data(address,symbol,type_id)
            

        # if type_id == "67":
        #     currency = ont_data(address,symbol,type_id)
            

        # if type_id == "70":
        #     currency = qtum_data(address,symbol,type_id)
            

        # if type_id == "75":
        #     currency = xrp_data(address,symbol,type_id)
            

        # if type_id == "83":
        #     currency = usdc_data(address,symbol,type_id)
            

        # if type_id == "84":
        #     currency = xtz_data(address,symbol,type_id)
            

        # if type_id == "87":
        #     currency = tron_data(address,symbol,type_id)
            

        # if type_id == "89":
        #     currency = unus_sed_leo_data(address,symbol,type_id)
            

        # if type_id == "91":
        #     currency = vet_data(address,symbol,type_id)
            

        # if type_id == "98":
        #     currency = zcash_data(address,symbol,type_id)
            
    
        # if type_id == "101":
        #     currency = gpl_data(address,symbol,type_id)
            

        # if type_id == "102":
        #     print("Matic")
        #     currency = matic_data(address,symbol,type_id)
            



      
        
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
                "amt": amount
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
        
            #update the address as verified
            if tx_type == 'verification':
                 mycursor.execute('UPDATE sws_address SET address_status ="verified" WHERE address = "'+str(address)+'" AND type_id = '+type_id+' AND cms_login_name =  "'+str(from_username)+'"' )
                 #send a mail
                 mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
                 email = mycursor.fetchone()
                 if email[0]:
                    email_id=email[0]
                    if email_id is not None:
                        msg = '<h3> Your address  ' + str(address) +'  is now verified </h3><strong>Date:</strong> ' + str(created_at) +' <div><strong>coin:</strong> ' + str(symbol) + ' </div>'
                        message = Mail(
                                from_email=Sendgrid_default_mail,
                                to_emails=email_id,
                                subject='SafeName - Address verification done', 
                                html_content= massegee)
                        sg = SendGridAPIClient(SendGridAPIClient_key)
                        response = sg.send(message)
                        print(response.status_code, response.body, response.headers)
                    else:
                        pass
                 else:
                   pass


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

