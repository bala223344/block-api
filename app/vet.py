import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import VET_balance,VET_transactions



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

    return jsonify({"status":"success"})


def vet_data_sync():
    current_tx = ["1416bVmA8Wwd3GGGA9W3kgmWiJTota7U62","18xmAHjjsTe8FJ6PAKAL5TxBc4Ypewo6q3","1BPnQZhMzVmM2Rnhs9YpRf8kJvBAzaUcAt","1EAECn7nzqMbk7FD3qa1dvbYkWj58iSV69","1GQhVHcghcNrgdvuWqzHxM3Ln23hxfqpvX","1JDSPz2rsfwNixJzc8pWBQx5v7b4wr5equ","1LP5s5m1VVXd59AYzdjcDLm4Rz1Duw1s2v","3NxLx7v8N2uA1HA4z7cncYVMcjKakqBmm9"]
    for addresses in current_tx:
        address = addresses[0]
        array=[]
        try:
            Recblocks = mongo.db.dev_sws_history.find_one({"address":address,"type_id":"2"})
            if Recblocks is not None:
                block = Recblocks['block']
            else:
                block = 1
            ret=VET_balance.replace("{{address}}",''+address+'')
            ret1=ret.replace("{{block}}",''+str(block)+'')
            response_user_token = requests.get(url=ret1)
            transaction = response_user_token.json()       
            
            balance =transaction['balance'] if "balance" in transaction else 0
            amountReceived =transaction['amount_received']
            amountSent =transaction['amount_sent']
            transactions = transaction['txs']
            
            for transaction in transactions:
                fee=transaction['fee']
                tx_id = transaction['hash']
                
                frmm=transaction['inputs']
                frm=[]
                for trans in frmm:
                    fro=trans['address']
                    send=trans['value']
                    frm.append({"from":fro,"send_amount":str(round((float(send)/100000000),6))})
                
                transac=transaction['outputs']
                to=[]
                for too in transac:
                    t = too['address'] 
                    recive =too['value']/100000000
                    to.append({"to":t,"receive_amount": (recive)})
                timestamp =transaction['timestamp']
                dt_object = datetime.datetime.fromtimestamp(timestamp)
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"dt_object":dt_object,"Tx_id":tx_id})
            if array:
                block = block+len(array)
            ret = mongo.db.dev_sws_history.update({
                "address":address,
                "type_id":"2"            
            },{
                "$set":{    
                        "address":address,
                        "symbol":"BTC",
                        "type_id":"2",
                        "block":int(block),
                        "date_time":datetime.datetime.utcnow(),
                        "balance":round((float(balance)/100000000),6),
                        "amountReceived":round((float(amountReceived)/100000000),6),
                        "amountSent":round((float(amountSent)/100000000),6)
                    }},upsert=True)
        except Exception:
            pass
        if array:
            for listobj in array:
                ret = mongo.db.dev_sws_history.update({
                    "address":address,
                    "type_id":"2"            
                },{
                    "$push":{    
                            "transactions":listobj}})

