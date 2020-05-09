import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.util import serialize_doc
from app.config import ETH_balance
from app.config import ETH_transactions
from app.config import mydb,mycursor
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



def EthSync():
    mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(1)+'"')
    current_tx = mycursor.fetchall()
    #current_tx = ["0x467D629A836d50AbECec436A615030A845feD378","0xdabb1e456cb0c490a34f65eff43ed0c449f039a7","0xa6fe83Dcf28Cc982818656ba680e03416824D5E4"]
    for addresses in current_tx:
        array=[]
        address = addresses[0]
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
            fro =transaction['from']
            too=transaction['to']
            send_amount=transaction['value']
            if send_amount != "0":
                tx_id = transaction['hash']
                blockNumber = transaction['blockNumber']
                to.append({"to":too,"receive_amount":""})
                frm.append({"from":fro,"send_amount":str(int(send_amount)/1000000000000000000)})
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id,"blockNumber":int(blockNumber)})
        balance = response['result']
        amount_recived =""
        amount_sent =""
        ret = mongo.db.dev_sws_history.update({
            "address":address            
        },{
            "$set":{    
                    "address":address,
                    "symbol":"ETH",
                    "type_id":"1",
                    "date_time":datetime.datetime.utcnow(),
                    "balance":(int(balance)/1000000000000000000),
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

def EthTimeSync():
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        "date_time": {
            "$lte": datetime.datetime.utcnow() - datetime.timedelta(minutes=3)
        }
    }).distinct("address")
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
            fro =transaction['from']
            too=transaction['to']
            send_amount=transaction['value']
            if send_amount != "0":
                tx_id = transaction['hash']
                blockNumber = transaction['blockNumber']
                to.append({"to":too,"receive_amount":""})
                frm.append({"from":fro,"send_amount":str(int(send_amount)/1000000000000000000)})
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id,"blockNumber":int(blockNumber)})
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

"""
def EthIntSync(address,symbol,type_id):
    #ret=ETH_internal_transactions.replace("{{address}}",''+address+'')
    #response_user_token = requests.get(url=ret)
    #response = response_user_token.json()       
    
    #transactions=response['result']
    #array=[]
    addresses = []

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


def get_event_list(address, start_block, end_block, apikey, topic):
	try:
		params = {
			"module": "logs",
			"action": "getLogs",
			"apikey": apikey,
			"address": address,
			"fromBlock": start_block,
			"toBlock": end_block,
			"topic0": topic
		}
		response = requests.get(ETHER_SCAN_DOMAIN, params=params)
		if response.status_code != 200:
			logging.error("get_event_log_fail|address=%s,start_block=%s,end_block=%s,api_key=%s,topic=%s,response_code=%s", address, start_block, end_block, apikey, topic, response.status_code)
			return None
		response_data = response.json()
		if int(response_data["status"]) != 1:
			logging.info("get_event_status_empty|address=%s,start_block=%s,end_block=%s,api_key=%s,topic=%s,response_data=%s", address, start_block, end_block, apikey, topic, response_data)
			return []
		return response_data["result"]
	except Exception as error:
		logging.error("get_event_exception|address=%s,start_block=%s,end_block=%s,api_key=%s,topic=%s,msg=%s", address, start_block, end_block, apikey, topic, error.message)
		return None
"""



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