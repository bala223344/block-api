import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.util import serialize_doc
from app.config import ETH_balance
from app.config import ETH_transactions
from app.config import mydb,mycursor
from pymongo import MongoClient
import logging
import datetime
from datetime import timedelta  

ETHER_SCAN_DOMAIN = "http://api.etherscan.io/api"

ETHERSCAN_API_KEYS = {
	"stats": "F5RG1UUIIGST6FXCSVJZQJQV88KC69VC37",
	"cron_1": "PAUIKFWUFNVT4UHPDSPSSCNTCIJ2EEVHT5",
	"cron_2": "UKIKGWXX57YZQBVF2DYG1KQYQFVKUU8CEH",
	"cron_3": "6972HTQYMQS44K5K4M4FXWBFWV8V91DWZX",
	"cron_4": "CIY5WV7P8QNCKX9MPWPYJCJCCRSTRJ1WD4"
}

SMART_CONTRACT_BLOCK_STEP = 10000000
ETHERSCAN_API_KEY = "UKIKGWXX57YZQBVF2DYG1KQYQFVKUU8CEH"

TOPIC_TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ETH_internal_transactions ="http://api.etherscan.io/api?module=account&action=txlistinternal&address={{address}}&startblock={{startblock}}&endblock={{endblock}}&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"

client = MongoClient("mongodb://admin:0vXPeLcPxME40Yd@157.245.124.93/marketcap?authSource=admin")
temp_db = client.marketcap

def EthSync():
    print("start")
    #mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(1)+'"')
    #current_tx = mycursor.fetchall()
    addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4","0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b","0x467D629A836d50AbECec436A615030A845feD378","0x17DB4E652e5058CEE05E1dC6C39E392e5cFDD670"]
    for addresses in addresses:
        array=[]
        address = addresses#[0]
        ret=ETH_balance.replace("{{address}}",''+address+'')
        response_user_token = requests.get(url=ret)
        response = response_user_token.json()       
        blocks = mongo.db.dev_sws_history.aggregate(
        [  
            {"$unwind" : "$transactions"},
            {
                "$match": {
                    "address":address
                }
            },
            {
                "$group" : {
                    "_id" : "$_id",
                    "maxblockNumber" : {"$max" : "$transactions.blockNumber"}
                }
            }
        ])
        blocks = [serialize_doc(doc) for doc in blocks]
        if blocks:
            block = blocks[0]
            StartBlock = block['maxblockNumber'] + 1
        else:
            StartBlock = 0
        EndBlock = StartBlock + SMART_CONTRACT_BLOCK_STEP
        transactions = get_txn_list(address,StartBlock,EndBlock,ETHERSCAN_API_KEY)
        for transaction in transactions:
            frm=[]
            to=[]
            fee =""
            timestamp = transaction['timeStamp']
            first_date=int(timestamp)
            dt_object = datetime.datetime.fromtimestamp(first_date)
            current_t = datetime.datetime.utcnow()

            diff = current_t- dt_object
            total_time = diff.days*24*60*60 + diff.seconds

            if total_time <= 60:
                total_time = round(total_time,2)
                total_expected_time = "{} second ago".format(total_time)
            elif total_time>60 and total_time<=3600:
                total_time = total_time/60
                total_time = round(total_time,1)
                total_expected_time = "{} minutes ago".format(total_time)
            elif total_time>3600 and total_time<=86400:
                total_time = total_time/3600
                total_time = round(total_time,1)
                total_expected_time = "{} hours ago".format(total_time)
            else:
                total_time = total_time/86400
                total_time = round(total_time,1)
                total_expected_time = "{} days ago".format(total_time)

            fro =transaction['from']
            too=transaction['to']
            send_amount=transaction['value']
            if send_amount != "0":
                tx_id = transaction['hash']
                blockNumber = transaction['blockNumber']
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'"')
                to_safename = mycursor.fetchone()
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'"')
                from_safename = mycursor.fetchone()

                token_details = temp_db.owners_data.find_one({"owner_address":str(too)},{"username":1,"_id":0})
                if token_details is not None:
                    usern = token_details['username']
                else:
                    usern = None

                token_deta = temp_db.owners_data.find_one({"owner_address":str(fro)},{"username":1,"_id":0})
                if token_deta is not None:
                    fromusern = token_deta['username']
                else:
                    fromusern = None

                to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":usern})
                frm.append({"from":fro,"send_amount":str(float(send_amount)/1000000000000000000),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                array.append({"fee":fee,"from":frm,"to":to,"date":total_expected_time,"dt_object":dt_object,"Tx_id":tx_id,"blockNumber":int(blockNumber)})
        balance = response['result']
        amount_recived =""
        amount_sent =""
        try:
            bal = round((float(balance)/1000000000000000000),6)
        except Exception:
            bal = 0
        print(address)
        ret = mongo.db.dev_sws_history.update({
            "address":address            
        },{
            "$set":{    
                    "address":address,
                    "symbol":"ETH",
                    "type_id":"1",
                    "date_time":datetime.datetime.utcnow(),
                    "balance":bal,
                    "amountReceived":amount_recived,
                    "amountSent":amount_sent
                }},upsert=True)
        if array:
            for listobj in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address            
                },{
                    "$push":{    
                            "transactions":listobj}})

def EthTimeSyncc(minn):
    """
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$lte": datetime.datetime.utcnow() - datetime.timedelta(minutes=minn)
        }
    }).distinct("address")
    """
    addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4","0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b","0x467D629A836d50AbECec436A615030A845feD378","0x17DB4E652e5058CEE05E1dC6C39E392e5cFDD670"]

    for address in addresses:
        array=[]
        blocks = mongo.db.dev_sws_history.aggregate(
        [  
            {"$unwind" : "$transactions"},
            {
                "$match": {
                    "address":address
                }
            },
            {
                "$group" : {
                    "_id" : "$_id",
                    "maxblockNumber" : {"$max" : "$transactions.blockNumber"}
                }
            }
        ])
        blocks = [serialize_doc(doc) for doc in blocks]
        if blocks:
            block = blocks[0]
            StartBlock = block['maxblockNumber'] + 1
        else:
            StartBlock = 0
        EndBlock = StartBlock + SMART_CONTRACT_BLOCK_STEP
        transactions = get_txn_list(address,StartBlock,EndBlock,ETHERSCAN_API_KEY)
        for transaction in transactions:
            frm=[]
            to=[]
            fee =""
            timestamp = transaction['timeStamp']
            first_date=int(timestamp)
            dt_object = datetime.datetime.fromtimestamp(first_date)
            current_t = datetime.datetime.utcnow()

            diff = current_t- dt_object
            total_time = diff.days*24*60*60 + diff.seconds

            if total_time <= 60:
                total_time = round(total_time,2)
                total_expected_time = "{} second ago".format(total_time)
            elif total_time>60 and total_time<=3600:
                total_time = total_time/60
                total_time = round(total_time,1)
                total_expected_time = "{} minutes ago".format(total_time)
            elif total_time>3600 and total_time<=86400:
                total_time = total_time/3600
                total_time = round(total_time,1)
                total_expected_time = "{} hours ago".format(total_time)
            else:
                total_time = total_time/86400
                total_time = round(total_time,1)
                total_expected_time = "{} days ago".format(total_time)


            fro =transaction['from']
            too=transaction['to']
            send_amount=transaction['value']
            if send_amount != "0":
                tx_id = transaction['hash']
                blockNumber = transaction['blockNumber']
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'"')
                to_safename = mycursor.fetchone()
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'"')
                from_safename = mycursor.fetchone()

                token_details = temp_db.owners_data.find_one({"owner_address":str(too)},{"username":1,"_id":0})
                if token_details is not None:
                    usern = token_details['username']
                else:
                    usern = None

                token_deta = temp_db.owners_data.find_one({"owner_address":str(fro)},{"username":1,"_id":0})
                if token_deta is not None:
                    fromusern = token_deta['username']
                else:
                    fromusern = None


                to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":usern})
                frm.append({"from":fro,"send_amount":str(float(send_amount)/1000000000000000000),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                array.append({"fee":fee,"from":frm,"to":to,"date":total_expected_time,"dt_object":dt_object,"Tx_id":tx_id,"blockNumber":int(blockNumber)})
        ret = mongo.db.dev_sws_history.update({
            "address":address            
        },{
            "$set":{    
                    "date_time":datetime.datetime.utcnow(),
                }},upsert=False)
        if array:
            for listobj in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address            
                },{
                    "$push":{    
                            "transactions":listobj
                            }
                })

def get_txn_list(address, start_block, end_block, apikey):
    try:
        params = {
            "module": "account",
            "action": "txlist",
            "sort": "asc",
            "apikey": apikey,
            "address": address,
            "startblock": start_block,
            "endblock": end_block
        }
        response = requests.get(ETHER_SCAN_DOMAIN, params=params)
        if response.status_code != 200:
            logging.error("get_txn_fail|address=%s,start_block=%s,end_block=%s,api_key=%s,response_code=%s", address, start_block, end_block, apikey, response.status_code)
            return None
        response_data = response.json()
        if int(response_data["status"]) != 1:
            logging.info("get_txn_status_empty|address=%s,start_block=%s,end_block=%s,api_key=%s,response_data=%s", address, start_block, end_block, apikey, response_data)
            return []
        return response_data["result"]
    except Exception as error:
        logging.error("get_txn_exception|address=%s,start_block=%s,end_block=%s,api_key=%s,msg=%s", address, start_block, end_block, apikey, error.message)
        return None



def EthTimeSync():
    EthTimeSyncc(10)
def EthTimeSync1():
    EthTimeSyncc(30)
def EthTimeSync2():
    EthTimeSyncc(40)
def EthTimeSync3():
    EthTimeSyncc(60)

#----------------------------------------------------------------------------------------------

def EthIntSync1():
    EthIntSync()

def EthIntSync2():
    EthIntSync()

def EthIntSync3():
    EthIntSync()

def EthIntSync4():
    EthIntSync()


def EthIntSync():
    """
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$gte": datetime.datetime.utcnow() - datetime.timedelta(minutes=minn)
        }
    }).distinct("address")
    """
    addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4","0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b","0x467D629A836d50AbECec436A615030A845feD378","0x17DB4E652e5058CEE05E1dC6C39E392e5cFDD670"]
    for address in addresses:
        array=[]
        blocks = mongo.db.dev_sws_history.aggregate(
        [  
            {"$unwind" : "$transactions"},
            {
                "$match": {
                    "address":address
                }
            },
            {
                "$group" : {
                    "_id" : "$_id",
                    "maxintblockNumber" : {"$max" : "$transactions.intblockNumber"}
                }
            }
        ])
        blocks = [serialize_doc(doc) for doc in blocks]
        if blocks:
            block = blocks[0]
            if block['maxintblockNumber'] is not None:
                StartBlock = int(block['maxintblockNumber']) + 1
            else:
                StartBlock = 0
        else:
            StartBlock = 0
        EndBlock = StartBlock + SMART_CONTRACT_BLOCK_STEP
        ret1=ETH_internal_transactions.replace("{{address}}",''+address+'')
        rett=ret1.replace("{{startblock}}",''+str(StartBlock)+'')
        ret=rett.replace("{{endblock}}",''+str(EndBlock)+'')
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
            dt_object = datetime.datetime.fromtimestamp(first_date)   
            current_t = datetime.datetime.utcnow()

            diff = current_t- dt_object
            total_time = diff.days*24*60*60 + diff.seconds

            if total_time <= 60:
                total_time = round(total_time,2)
                total_expected_time = "{} second ago".format(total_time)
            elif total_time>60 and total_time<=3600:
                total_time = total_time/60
                total_time = round(total_time,1)
                total_expected_time = "{} minutes ago".format(total_time)
            elif total_time>3600 and total_time<=86400:
                total_time = total_time/3600
                total_time = round(total_time,1)
                total_expected_time = "{} hours ago".format(total_time)
            else:
                total_time = total_time/86400
                total_time = round(total_time,1)
                total_expected_time = "{} days ago".format(total_time)

            fro =transaction['from']
            if 'to' in transaction:
                too=transaction['to']
            else:
                too=""
            send_amount=transaction['value']
            if send_amount != "0":
                tx_id = transaction['hash']
                intblockNumber = transaction['blockNumber']
                if too !="":
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'"')
                    to_safename = mycursor.fetchone()
                else:
                    to_safename = []
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'"')
                from_safename = mycursor.fetchone()
                token_details = temp_db.owners_data.find_one({"owner_address":str(too)},{"username":1,"_id":0})
                if token_details is not None:
                    usern = token_details['username']
                else:
                    usern = None

                token_deta = temp_db.owners_data.find_one({"owner_address":str(fro)},{"username":1,"_id":0})
                if token_deta is not None:
                    fromusern = token_deta['username']
                else:
                    fromusern = None
                to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":usern})
                frm.append({"from":fro,"send_amount":str(float(send_amount)/1000000000000000000),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                array.append({"fee":fee,"from":frm,"to":to,"date":total_expected_time,"dt_object":dt_object,"Tx_id":tx_id,"internal_transaction":True,"intblockNumber":int(intblockNumber)})
        if array:
            for arra in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address            
                },{'$push': {'transactions': arra}},upsert=False)
        else:
            pass        



"""
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

"""









"""
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
"""