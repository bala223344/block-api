import requests
from flask import jsonify
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import mongo
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,ETH_transactions,ETH_balance,ETH_internal_transactions



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



















#return jsonify({"status":"success"})

'''
def eth_data(address,symbol,type_id):
    print("etheeeeeeeeeeeeeeeeeeeee")
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
        if send_amount == "0":
            print(send_amount)
            tx_id = transaction['hash']
            print(tx_id)
            docc=ETH_internal_transactions.replace("{{hash}}",''+tx_id+'')
            internal_response_user = requests.get(url=docc)
            ress = internal_response_user.json()  
            print("response",ress)
            print("from:",fro,"and","to:",too)
            message = ress['message']
            if message == 'OK':
                result = ress['result']   
                resul = result[0]
                frrr = resul['from']
                tooo = resul['to'] 
                value = resul['value']
                timeSta = resul['timeStamp']
                first_dae=int(timeSta)
                dt_obj = datetime.fromtimestamp(first_dae)
                to.append({"to":tooo,"receive_amount":""})
                frm.append({"from":frrr,"send_amount":str(int(value)/1000000000000000000)})
                array.append({"fee":fee,"from":frm,"to":to,"date":dt_obj,"Tx_id":tx_id,"internal_transaction":True})
            else:
                pass
        else:
            print("elseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            print(send_amount)
            tx_id = transaction['hash']
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":str(int(send_amount)/1000000000000000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object,"Tx_id":tx_id})
    print(len(array))
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
'''


