import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.util import serialize_doc
from app.config import ETH_balance
from app.config import ETH_transactions
from app.config import mydb
from pymongo import MongoClient
import logging
import datetime
from datetime import timedelta  
from threading import Thread

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


client = MongoClient("mongodb+srv://remoteuser:0vXPeLcPxME40Ydv@cg-cluster.a3zdw.mongodb.net/marketcap?retryWrites=true&w=majority")

temp_db = client.marketcap


def EthSync():
    mycur = mydb()
    mycursor = mycur.cursor()
    mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(1)+'"')
    current_tx = mycursor.fetchall()
    mycursor.close()
    transactions = list(current_tx)
    rang = len(transactions)/10
    rang = round(rang)
    for a in range(0,rang+1):
        try:
            if len(transactions) > 10: 
                small_list = transactions[:10]
                del transactions[:10]
            else:
                small_list = transactions
            t = Thread(target=EthSyncFunc, args=(small_list,))
            t.start()
        except Exception:
            pass

def EthSyncFunc(small_list):
    """
    print("start")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(1)+'"')
    current_tx = mycursor.fetchall()
    mycursor.close()
    #addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4","0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b","0x467D629A836d50AbECec436A615030A845feD378","0x17DB4E652e5058CEE05E1dC6C39E392e5cFDD670"]
    """
    for addresses in small_list:
        array=[]
        try:
            address = addresses[0]
            ret=ETH_balance.replace("{{address}}",''+address+'')
            response_user_token = requests.get(url=ret)
            response = response_user_token.json()       
            blocks = mongo.db.dev_sws_history.aggregate(
            [  
                {"$unwind" : "$transactions"},
                {
                    "$match": {
                        "address":address,
                        "type_id":"1"
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
                if block['maxblockNumber'] is not None:
                    StartBlock = block['maxblockNumber'] + 1
                else:
                    StartBlock = 0
            else:
                StartBlock = 0
            EndBlock = StartBlock + SMART_CONTRACT_BLOCK_STEP
            transactions = get_txn_list(address,StartBlock,EndBlock,ETHERSCAN_API_KEY)
            temp_db = client.marketcap
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
                if send_amount != "0":
                    tx_id = transaction['hash']
                    blockNumber = transaction['blockNumber']
                    
                    token_details = temp_db.owners_data.find_one({"owner_address":transaction['to']},{"username":1,"_id":0})
                    if token_details is not None:
                        usern = token_details['username']
                    else:
                        usern = None
                    token_deta = temp_db.owners_data.find_one({"owner_address":transaction['from']},{"username":1,"_id":0})
                    if token_deta is not None:
                        fromusern = token_deta['username']
                    else:
                        fromusern = None                
                    mycur = mydb()
                    mycursor = mycur.cursor()
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'" AND address_safename_enabled="yes"')
                    to_safename = mycursor.fetchone()
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'" AND address_safename_enabled="yes"')
                    from_safename = mycursor.fetchone()
                    mycursor.close()
                    to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":usern})
                    frm.append({"from":fro,"send_amount":str(round((float(send_amount)/1000000000000000000),6)),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                    array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"dt_object":dt_object,"Tx_id":tx_id,"blockNumber":int(blockNumber)})
            try:
                balance = response['result']
            except Exception:
                balance = 0
            amount_recived =""
            amount_sent =""
            try:
                bal = round((float(balance)/1000000000000000000),6)
            except Exception:
                bal = 0
            ret = mongo.db.dev_sws_history.update({
                "address":address,
                "type_id":"1"            
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
                        "address":address,            
                        "type_id":"1"
                    },{
                        "$push":{    
                                "transactions":listobj}})
        except Exception:
            pass

"""
def EthTimeSync():
    EthTimeSyncc(10)
def EthTimeSync1():
    EthTimeSyncc(30)
def EthTimeSync2():
    EthTimeSyncc(40)
def EthTimeSync3():
    EthTimeSyncc(60)
def EthTimeSync4():
    EthTimeSyncc(1)
def EthTimeSyncc(minn):
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$lte": datetime.datetime.utcnow() - datetime.timedelta(minutes=minn)
        }
    }).distinct("address")
    for address in addresses:
        array=[]
        try:
            EthTransaction(address,array)
        except Exception:
            pass    
"""

#def EthTransaction(address,array):


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




#----------------------------------------------------------------------------------------------

def EthIntSync1():
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$gte": datetime.datetime.utcnow() - datetime.timedelta(minutes=58)
        }
    }).distinct("address")
    #print(addresses)

    rang = len(addresses)/10
    rang = round(rang)
    for a in range(0,rang+1):
        try:
            if len(addresses) > 10 : 
                small_list = addresses[:10]
                del addresses[:10]
            else:
                small_list = addresses
            t = Thread(target=EthIntSync, args=(small_list,))
            t.start()
        except Exception:
            pass
        #print("threads are running",len(addresses))

#    EthIntSync(5)

"""
def EthIntSync2():
    EthIntSync(12)
def EthIntSync3():
    EthIntSync(27)
def EthIntSync4():
    EthIntSync(30)
def EthIntSync5():
    EthIntSync(180)
"""

def EthIntSync(small_list):
    """
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        }).distinct("address")
    """
    """
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$gte": datetime.datetime.utcnow() - datetime.timedelta(minutes=minn)
        }
    }).distinct("address")
    """
    temp_db = client.marketcap
    #addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4","0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b","0x467D629A836d50AbECec436A615030A845feD378","0x17DB4E652e5058CEE05E1dC6C39E392e5cFDD670"]
    for address in small_list:
        array=[]
        try:
            blocks = mongo.db.dev_sws_history.aggregate(
            [  
                {"$unwind" : "$transactions"},
                {
                    "$match": {
                        "address":address,
                        "type_id":"1"
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
            for transaction in transactions:
                frm=[]
                to=[]
                fee =""
                timestamp = transaction['timeStamp']
                first_date=int(timestamp)
                dt_object = datetime.datetime.fromtimestamp(first_date)   

                fro =transaction['from']
                if 'to' in transaction:
                    too=transaction['to']
                else:
                    too=""
                send_amount=transaction['value']
                if send_amount != "0":
                    tx_id = transaction['hash']
                    intblockNumber = transaction['blockNumber']
                    token_details = temp_db.owners_data.find_one({"owner_address":transaction['to']},{"username":1,"_id":0})
                    if token_details is not None:
                        usern = token_details['username']
                    else:
                        usern = None

                    token_deta = temp_db.owners_data.find_one({"owner_address":transaction['from']},{"username":1,"_id":0})
                    if token_deta is not None:
                        fromusern = token_deta['username']
                    else:
                        fromusern = None
                    if too !="":
                        mycur = mydb()
                        mycursor = mycur.cursor()
                        mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'" AND address_safename_enabled="yes"')
                        to_safename = mycursor.fetchone()
                    else:
                        to_safename = []
                    
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'" AND address_safename_enabled="yes"')
                    from_safename = mycursor.fetchone()
                    mycursor.close()
                    to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":usern})
                    frm.append({"from":fro,"send_amount":str(round((float(send_amount)/1000000000000000000),6)),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                    array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"dt_object":dt_object,"Tx_id":tx_id,"internal_transaction":True,"intblockNumber":int(intblockNumber)})
        except Exception:
            pass
        if array:
            for arra in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address,
                    "type_id":"1"            
                },{'$push': {'transactions': arra}},upsert=False)
        else:
            pass        




#1GQhVHcghcNrgdvuWqzHxM3Ln23hxfqpvX
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
"""
def EthTimeSyncc(minn):
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$lte": datetime.datetime.utcnow() - datetime.timedelta(minutes=minn)
        }
    }).distinct("address")
    #addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4","0xBcBF6aC5F9D4D5D35bAC4029B73AA4B9Ed5e8c0b","0x467D629A836d50AbECec436A615030A845feD378","0x17DB4E652e5058CEE05E1dC6C39E392e5cFDD670"]
    for address in addresses:
        array=[]
        blocks = mongo.db.dev_sws_history.aggregate(
        [  
            {"$unwind" : "$transactions"},
            {
                "$match": {
                    "address":address,
                    "type_id":"1"
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
            fro =transaction['from']
            too=transaction['to']
            send_amount=transaction['value']
            if send_amount != "0":
                tx_id = transaction['hash']
                blockNumber = transaction['blockNumber']
        
                token_details = temp_db.owners_data.find_one({"owner_address":transaction['to']},{"username":1,"_id":0})
                if token_details is not None:
                    usern = token_details['username']
                else:
                    usern = None
                token_deta = temp_db.owners_data.find_one({"owner_address":transaction['from']},{"username":1,"_id":0})
                if token_deta is not None:
                    fromusern = token_deta['username']
                else:
                    fromusern = None
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'" AND address_safename_enabled="yes"')
                to_safename = mycursor.fetchone()
                mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'" AND address_safename_enabled="yes"')
                from_safename = mycursor.fetchone()
                to.append({"to":too,"receive_amount":"","safename":to_safename[0] if to_safename else None,"openseaname":usern})
                frm.append({"from":fro,"send_amount":str(round((float(send_amount)/1000000000000000000),6)),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"dt_object":dt_object,"Tx_id":tx_id,"blockNumber":int(blockNumber)})
        ret = mongo.db.dev_sws_history.update({
            "address":address,
            "type_id":"1"            
        },{
            "$set":{    
                    "date_time":datetime.datetime.utcnow(),
                }},upsert=False)
        if array:
            for listobj in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address,
                    "type_id":"1"            
                },{
                    "$push":{    
                            "transactions":listobj
                            }
                })
def EthTimeSync():
    EthTimeSyncc(10)
def EthTimeSync1():
    EthTimeSyncc(30)
def EthTimeSync2():
    EthTimeSyncc(40)
def EthTimeSync3():
    EthTimeSyncc(60)
"""