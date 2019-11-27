import requests
from flask import jsonify
from datetime import datetime
from app import mongo

from app.config import ETH_balance,ETH_internal_transactions
from app.config import ETH_transactions
from app.config  import BTC_balance
from app.config import ZRX_balance,ZRX_transactions
from app.config import ELF_balance,ELF_transactions
from app.config import AE_balance,AE_transactions
from app.config import REP_balance,REP_transactions
from app.config import AOA_balance,AOA_transactions
from app.config import BAT_balance,BAT_transactions
from app.config import BNB_balance,BNB_transactions
from app.config import BCH_transactions,BCH_balance
from app.config import BTC_GOLD_balance,BTC_GOLD_transactions
from app.config import BSV_balance,BSV_transactions
from app.config import BTT_balance,BTT_transactions
from app.config import LINK_balance,LINK_transactions
from app.config import CCCX_balance,CCCX_transactions
from app.config import MCO_balance,MCO_transactions
from app.config import CRO_balance,CRO_transactions
from app.config import DAI_balance,DAI_transactions
from app.config import DASH_balance,DASH_transactions
from app.config import EKT_balance,EKT_transactions
from app.config import EGT_balance,EGT_transactions
from app.config import ENJ_balance,ENJ_transactions
from app.config import EOS_balance,EOS_transactions
from app.config import GNT_balance,GNT_transactions
from app.config import HT_balance,HT_transactions
from app.config import ICX_balance,ICX_transactions
from app.config import INB_balance,INB_transactions
from app.config import IOTA_balance
from app.config import KCS_balance,KCS_transactions
from app.config import LAMB_balance,LAMB_transactions
from app.config import LTC_balance,LTC_transactions
from app.config import MKR_balance,MKR_transactions
from app.config import ONT_balance,ONT_transactions
from app.config import QTUM_balance,QTUM_transactions
from app.config import XRP_balance,XRP_transactions
from app.config import USDT_balance,USDT_transactions
from app.config import XTZ_balance,XTZ_transactions
from app.config import TRON_balance,TRON_transactions
from app.config import VET_balance,VET_transactions
from app.config import ZEC_balance,ZEC_transactions
from app.config import GPL_balance,GPL_transactions
from app.config import MATIC_balance,MATIC_transactions


#----------Function for fetching tx_history and balance storing in mongodb----------

def matic_data(address,symbol,type_id):
    print("gpl_data_running")
    ret=MATIC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=MATIC_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def gpl_data(address,symbol,type_id):
    print("gpl_data_running")
    ret=GPL_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=GPL_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xeeddaa78e0b2de769e969bd049c8faff3280df97":
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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def zcash_data(address,symbol,type_id):
    print("zcash_data_zcash") 
    ret=ZEC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ZEC_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    array=[]
    for transaction in res:
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        vin = transaction['vin']
        vout= transaction['vout']
        frm=[]
        for v_in in vin:
            if v_in is not None:
                retrievedVout = v_in['retrievedVout']['scriptPubKey']
                val = v_in['retrievedVout']['value']
                if "addresses" in retrievedVout:
                    addresses=retrievedVout['addresses']
                    for h in addresses:
                        frm.append({"from":h,"send_amount":val})
        to=[]
        for v_out in vout:
            if v_out is not None:
                retrieved = v_out['scriptPubKey']['addresses']
                valu = v_out['value']
                for a in retrieved:
                    to.append({"to":a,"receive_amount":valu})

        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    balance = response['balance']
    amount_recived =response['totalRecv']
    amount_sent =response['totalSent']

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


#----------Function for fetching tx_history and balance storing in mongodb----------

def vet_data(address,symbol,type_id):
    ret=VET_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=VET_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       

    transactions=res['transactions']
    array=[]
    
    for transaction in transactions:
        if transaction:
            frm=[]
            to=[]
            timestamp = transaction['timestamp']
            origin =transaction['origin']
            dt_object = datetime.fromtimestamp(timestamp)
            vin = transaction['clauses']
            for trans in vin:
                too=trans['to']
                to.append({"to":too,"receive_amount":""})
                frm.append({"from":origin,"send_amount":""})
            array.append({"fee":"","from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =""
    amount_sent =""

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


#----------Function for fetching tx_history and balance storing in mongodb----------

def tron_data(address,symbol,type_id):
    ret=TRON_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    doc=TRON_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions = res['data']
    
    array=[]
    
    for transaction in transactions:
        to=[]
        frm=[]
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        conver_d =timestamp/1000.0
        fro = transaction['ownerAddress']
        too = transaction['toAddress']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":""})
        dt_object = datetime.fromtimestamp(conver_d)
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =""
    amount_sent =""

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(balance/1000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)


#----------Function for fetching tx_history and balance storing in mongodb----------

def xtz_data(address,symbol,type_id):
    ret=XTZ_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    doc=XTZ_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    array=[]
    
    for transaction in res:
        frm=[]
        to=[]
        trans =transaction['type']['operations']
        for tra in trans:
            amount=tra['amount']
            fee=""
            timestamp=tra['timestamp'] 
            too=tra['destination']
            tz = too['tz']
            fro=tra['src']
            tzz=fro['tz']
            frm.append({"from":tzz,"send_amount":(int(amount)/1000000)})
            to.append({"to":tz,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":timestamp})
    

    balance=response['balance']
    amount_recived =""
    amount_sent =""
    
    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/1000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)



#----------Function for fetching tx_history and balance storing in mongod----------

def usdc_data(address,symbol,type_id):
    ret=USDT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=USDT_transactions.replace("{{address}}",''+address+'')
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
        send_amount=transaction['value']
        too=transaction['to']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":send_amount})
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
                "balance":balance,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    

#----------Function for fetching tx_history and balance storing in mongodb----------

def xrp_data(address,symbol,type_id):
    ret=XRP_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    doc=XRP_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['transactions']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        fro = transaction['Account']
        if "Destination" in transaction:
            too = transaction['Destination']
        else:
            too=""
        fee = transaction['Fee']
        date = transaction['date']
        frm.append({"from":fro,"send_amount":""})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":date})
    

    balance=response['initial_balance']
    amount_recived =""
    amount_sent =""
    
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def qtum_data(address,symbol,type_id):
    ret=QTUM_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=QTUM_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['transactions']
    
    array=[]
    for transaction in transactions:
        
        
        ret1=url_hash.replace("{{hash}}",''+transaction+'')
        response_u = requests.get(url=ret1)
        res1 = response_u.json()
        
        for tran in res1:
            fee=tran['fees']
            timestamp=tran['timestamp']
            dt_object = datetime.fromtimestamp(timestamp)
            inputs=tran['inputs']
            outputs=tran['outputs']
            frm=[]
            for inp in inputs:
                addre=inp['address']
                val=inp['value']
                frm.append({"from":addre,"send_amount":(int(val)/100000000)})
            to=[]
            for inpp in outputs:
                ad=inpp['address']
                value=inpp['value']
                to.append({"to":ad,"receive_amount":(int(value)/100000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    balance = response['balance']
    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":(int(balance)/100000000),
                "transactions":array,
                "amountReceived":(int(amount_recived)/100000000),
                "amountSent":(int(amount_sent)/100000000)
            }},upsert=True)



#----------Function for fetching tx_history and balance storing in mongodb ----------

def ont_data(address,symbol,type_id):
    ret=ONT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ONT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions = res['result']
    array=[]
    
    for transaction in transactions:
        fee =transaction['fee']
        timestamp = transaction['tx_time']
        dt_object = datetime.fromtimestamp(timestamp)
        transfers=transaction['transfers']
        frm=[]
        to=[]
        for v_in in transfers:
            if v_in is not None:
                amount = v_in['amount']
                fro = v_in['from_address']
                too = v_in['to_address']
                frm.append({"from":fro,"send_amount":amount})
                to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    amount_recived =""
    amount_sent =""
    reslt = response['result']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset_name']
            if asset_name == "ont":
                balance = ress['balance']
                    
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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def mkr_data(address,symbol,type_id):
    ret=MKR_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=MKR_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2":
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
    



#----------Function for fetching tx_history and balance storing in mongodb----------

def ltc_data(address,symbol,type_id):
    ret=LTC_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    data = response['data']

    doc=LTC_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions = res['data']['data']

    array=[]
    for transaction in transactions:
        if transaction:
            inputs = transaction['inputs']
            outputs =transaction['outputs']
            frm=[]
            for inpu in inputs:
                if inpu:
                    prev_value=inpu['prev_value']
                    if "prev_addresses" in inpu:
                        prev_addresses=inpu['prev_addresses']
                        for pre in prev_addresses:
                            frm.append({"from":pre,"send_amount":prev_value})
            to=[]
            for out in outputs:
                if out:    
                    value=out['value']
                    if "addresses" in out:   
                        addresses=out['addresses']
                        for addr in addresses:
                            to.append({"to":addr,"receive_amount":value})
            fee =transaction['income']
            timestamp = transaction['time']
            conver_d = int(timestamp)
            dt_object = datetime.fromtimestamp(conver_d)
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = data['balance']
    amount_recived =data['total_receive']
    amount_sent =data['total_send']

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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def lamb_data(address,symbol,type_id):
    ret=LAMB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=LAMB_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x8971f9fd7196e5cee2c1032b50f656855af7dd26":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def kcs_data(address,symbol,type_id):
    ret=KCS_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=KCS_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x039b5649a59967e3e936d7471f9c3700100ee1ab":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def iota_data(address,symbol,type_id):
    ret=IOTA_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    transactions = response['transactions']
    array=[]
    
    for transaction in transactions:
        to =[]
        fro =[]
        fee =transaction['value']
        timestamp = transaction['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        addr=transaction['address'] 
        amount=transaction['value']
        amo =int(amount)/1000000000000000
        amou=float("{0:.2f}".format(amo))
        fro.append({"from":addr,"send_amount":amou}) 
        array.append({"fee":fee,"from":fro,"to":to,"date":dt_object})
    
    balance = response['balance']
    ball =int(balance)/1000000000000000
    bal=float("{0:.2f}".format(ball))
    amount_recived =""
    amount_sent =""

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":bal,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)

   

#----------Function for fetching tx_history and balance storing in mongodb----------

def inb_data(address,symbol,type_id):
    ret=INB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=INB_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x17aa18a4b64a55abed7fa543f2ba4e91f2dce482":
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
        dt_object = datetime.fromtimestamp(first_date)
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




#----------Function for fetching tx_history and balance storing in mongodb----------

def ht_data(address,symbol,type_id):
    ret=HT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=HT_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x6f259637dcd74c767781e37bc6133cd6a68aa161":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def gnt_data(address,symbol,type_id):
    ret=GNT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=GNT_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xa74476443119a942de498590fe1f2454d7d4ac0d":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def eos_data(address,symbol,type_id):
    acouunt={"account_name":address}
    response_user_token = requests.post(url=EOS_balance,json=acouunt)
    response = response_user_token.json()       
    pay={"account_name":address,"offset":"-20","pos":"-1"}
    response_user = requests.post(url=EOS_transactions,json=pay)
    res = response_user.json()       
    transactions=res['actions'] 
    
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        block_time=transaction['block_time']
        action_trace=transaction['action_trace']['act']['data']
        if "from" in action_trace:
            fro = action_trace['from']
        else:
            fro=""
        if "to" in action_trace:   
            too=action_trace['to']
        else:
            too=""
        if "quantity" in action_trace:   
            amount_sent=action_trace['quantity']
        else:
            amount_sent=""
        frm.append({"from":fro,"send_amount":amount_sent})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":"","from":frm,"to":to,"date":block_time})
    
    balance=response['core_liquid_balance']
    amount_recived =""
    amount_sent =""
    
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
    

#----------Function for fetching tx_history and balance storing in mongodb----------

def enj_data(address,symbol,type_id):
    ret=ENJ_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ENJ_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xf0ee6b27b759c9893ce4f094b49ad28fd15a23e4":
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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def egt_data(address,symbol,type_id):
    ret=EGT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=EGT_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x8e1b448ec7adfc7fa35fc2e885678bd323176e34":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def ekt_data(address,symbol,type_id):
    ret=EKT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=EKT_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xbab165df9455aa0f2aed1f2565520b91ddadb4c8":
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


#----------Function for fetching tx_history and balance storing in mongodb ----------

def dash_data(address,symbol,type_id):
    ret=DASH_balance.replace("{{address}}",''+address+'')
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
        doc=DASH_transactions.replace("{{address}}",''+tran+'')
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
    

#----------Function for fetching tx_history and balance storing in mongodb----------

def dai_data(address,symbol,type_id):
    print("dai_data_running")
    ret=DAI_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=DAI_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def cro_data(address,symbol,type_id):
    print("cro_data")
    ret=CRO_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=CRO_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def mco_data(address,symbol,type_id):
    ret=MCO_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=MCO_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xb63b606ac810a52cca15e44bb630fd42d8d1d83d":
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
    

#----------Function for fetching tx_history and balance storing in mongodb----------

def cccx_data(address,symbol,type_id):
    ret=CCCX_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=CCCX_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x378903a03fb2c3ac76bb52773e3ce11340377a32":
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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def link_data(address,symbol,type_id):
    ret=LINK_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=LINK_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x514910771af9ca656af840dff83e8264ecf986ca":
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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def btt_data(address,symbol,type_id):
    ret=BTT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=BTT_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions=res['data']
    
    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        conver_d =timestamp/1000.0
        dt_object = datetime.fromtimestamp(conver_d)
        fro =transaction['ownerAddress']
        too=transaction['toAddress']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =""
    amount_sent =""

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
   




#----------Function for fetching tx_history and balance storing in mongodb----------

def btc_cash_data(address,symbol,type_id):
    ret=BCH_balance.replace("{{address}}",''+address+'')
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




#----------Function for fethcing tx_history and balance from api and send notification if got a new transaction---------- 

def bnb_data(address,symbol,type_id):
    ret=BNB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=BNB_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()      
    transactions = res['txArray']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        if "fromAddr" and "toAddr" in transaction:
            tx_id = transaction['txHash']
            fee =transaction['txFee']
            timestamp = transaction['timeStamp']
            conver_d =timestamp/1000.0
            dt_object = datetime.fromtimestamp(conver_d)
            amount = transaction['value']
            fro = transaction['fromAddr']
            too = transaction['toAddr']   
            frm.append({"from":fro,"send_amount":amount})
            to.append({"to":too,"receive_amount":""})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    
 
    amount_recived =""
    amount_sent =""
    reslt = response['balance']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset']
            if asset_name == "BNB":
                balance = ress['free']
                
    
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
    


#----------Function for fetching tx_history and balance storing in mongodb----------

def bat_data(address,symbol,type_id):
    ret=BAT_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=BAT_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x0d8775f648430679a709e98d2b0cb6250d2887ef":
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
    



#----------Function for fetching tx_history and balance storing in mongodb----------

def aoa_data(address,symbol,type_id):
    ret=AOA_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=AOA_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0x9ab165d795019b6d8b3e971dda91071421305e5a":
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
    



#----------Function for fetching tx_history and balance storing in mongodb----------

def rep_data(address,symbol,type_id):
    ret=REP_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=REP_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xe94327d07fc17907b4db788e5adf2ed424addff6":
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
    



#----------Function for fetching tx_history and balance storing in mongodb----------

def ae_data(address,symbol,type_id):
    ret=AE_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=AE_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    transactions = response_user.json()       
    array=[]
    for transaction in transactions:
        frm=[]
        to=[]
        timestamp = transaction['time']
        tx_id = transaction['hash']
        txs_history = transaction['tx']
        fro =txs_history['sender_id']
        too=""
        fee =txs_history['fee']
        send_amount=txs_history['amount']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":timestamp,"Tx_id":tx_id})
    
    balance = response['balance']
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
    




#----------Function for fetching tx_history and balance storing in mongodb----------

def elf_data(address,symbol,type_id):
    ret=ELF_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ELF_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xbf2179859fc6D5BEE9Bf9158632Dc51678a4100e":
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


#----------Function for fetching tx_history and balance storing in mongodb----------

def zrx_data(address,symbol,type_id):
    ret=ZRX_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=ZRX_transactions.replace("{{address}}",''+address+'')
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
        contractAddress = transaction['contractAddress']
        if contractAddress == "0xe41d2489571d322189246dafa5ebde1f4699f498":
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
                recive =too['value']
                to.append({"to":t,"receive_amount":str(int(recive)/100000000)})
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
