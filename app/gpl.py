import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import GPL_balance,GPL_transactions
from app.ethersync import temp_db
from app.config import mydb,mycursor
from app.util import serialize_doc

GplBalance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xeeddaa78e0b2de769e969bd049c8faff3280df97&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
GplTransactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock={{startblock}}&endblock={{endblock}}&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
SMART_CONTRACT_BLOCK_STEP = 10000000

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
    return jsonify({"status":"success"})



def GplDataSync():
    print("gpl_data_running")
    #mycursor.execute('SELECT address FROM sws_address WHERE type_id="'+str(1)+'"')
    #current_tx = mycursor.fetchall()
    current_tx = ["0xa6fe83Dcf28Cc982818656ba680e03416824D5E4"]
    for addresses in current_tx:
        array=[]
        address = addresses#[0]

        #ret=GplBalance.replace("{{address}}",''+address+'')
        #response_user_token = requests.get(url=ret)
        #response = response_user_token.json()       
    
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
                    "maxercblockNumber" : {"$max" : "$transactions.ercblockNumber"}
                }
            }
        ])
        blocks = [serialize_doc(doc) for doc in blocks]
        print(blocks)
        if blocks:
            block = blocks[0]
            if block['maxercblockNumber'] is not None:
                StartBlock = block['maxercblockNumber'] + 1
            else:
                StartBlock = 0
        else:
            StartBlock = 0
        EndBlock = StartBlock + SMART_CONTRACT_BLOCK_STEP
        print(StartBlock)
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
            timestamp = transaction['timeStamp']
            first_date=int(timestamp)
            dt_object = datetime.fromtimestamp(first_date)
            fro =transaction['from']
            too=transaction['to']
            send_amount=transaction['value']
            blockNumber = transaction['blockNumber']
            tx_id = transaction['hash']
            contractAddress = transaction['contractAddress']
            if contractAddress == "0xeeddaa78e0b2de769e969bd049c8faff3280df97":
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
                frm.append({"from":fro,"send_amount":(int(send_amount)/1000000000000000000),"safename":from_safename[0] if from_safename else None,"openseaname":fromusern})
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"dt_object":dt_object,"Tx_id":tx_id,"is_erc20":True,"ercblockNumber":int(blockNumber)})
        
        if array:
            for listobj in array:
                print(address)
                ret = mongo.db.dev_sws_history.update({
                    "address":address
                },{
                    "$push":{    
                            "transactions":listobj}})



