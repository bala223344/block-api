import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import GPL_balance,GPL_transactions
from app.ethersync import client
from app.config import mydb
from app.util import serialize_doc
import datetime
from threading import Thread


GplBalance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x95daaab98046846bf4b2853e23cba236fa394a31&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
GplTransactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock={{startblock}}&endblock={{endblock}}&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
SMART_CONTRACT_BLOCK_STEP = 10000000


def EmontDataSync():
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        }).distinct("address")

    transactions = addresses
    rang = len(transactions)/10
    rang = round(rang)
    for a in range(0,rang+1):
        try:
            if len(transactions) > 10 : 
                small_list = transactions[:10]
                del transactions[:10]
            else:
                small_list = transactions
            t = Thread(target=EmontDataFunc, args=(small_list,))
            t.start()
        except Exception:
            pass
"""
def EmontDataSync1():
    EmontDataFunc()
def EmontDataSync2():
    EmontDataFunc()
def EmontDataSync3():
    EmontDataFunc()
"""

def EmontDataFunc(small_list):
    #mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(1)+'"')
    #current_tx = mycursor.fetchall()
    #addresses = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4"]
    """
    addresses = mongo.db.dev_sws_history.find({
        "type_id": "1",
        }).distinct("address")
    """
    temp_db = client.marketcap
    for address in small_list:
        try:
            array=[]
            #address = addresses[0]
            ret=GplBalance.replace("{{address}}",''+address+'')
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
                blocks = [serialize_doc(doc) for doc in blocks]
                if blocks:
                    block = blocks[0]
                    if block['maxercblockNumber'] is not None:
                        StartBlock = block['maxercblockNumber'] + 1
                    else:
                        StartBlock = 0
                else:
                    StartBlock = 0
                EndBlock = StartBlock + SMART_CONTRACT_BLOCK_STEP
                doc=GplTransactions.replace("{{address}}",''+address+'')
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
                        frm.append({"from":fro,"send_amount":(float(send_amount)/100000000),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
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
        except Exception:
            pass