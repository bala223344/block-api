import requests
from app.util import serialize_doc
from app import mongo
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect( user="VsaqpBhCxL" , password="sW9BgYhqmG", host="remotemysql.com", database="VsaqpBhCxL")
mycursor=mydb.cursor()


def auto_fetch():
    print("runing")
    response_user_token = requests.get(url="https://etherscamdb.info/api/scams")
    response = response_user_token.json()
    result = response['result']
    if result:
        for record in result:
            if "addresses" in record:
                name = record['name']
                coin = record['coin']
                category = record['category']
                status =  record['status']
                addr = record['addresses']
                for add in addr:
                    addresses = add
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE addresses="'+str(addresses)+'"')
                    check = mycursor.fetchall()
                    if not check:
                        print("added")
                        mycursor.execute('''SELECT MAX(id) FROM sws_heist_address''')
                        maxid = mycursor.fetchone()
                        check=maxid[0]
                        if check is None:
                            ids = 1
                        else:
                            ids=(maxid[0]+1)
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(addresses)+'")')
                        mydb.commit()
                        
                






'''
def auto_fetch():
    print('running...')
    records = mongo.db.address.find({})
    records = [serialize_doc(doc) for doc in records]
    for record in records:
        records = mongo.db.symbol_url.find_one({"symbol":symbol})
        url=records['url_balance']
        if "url_trans" in records:
            url1=records['url_trans']
        ret=url.replace("{{address}}",''+address+'')
        ret1=ret.replace("{{symbol}}",''+symbol+'')
        address=record['address']
        symbol=record['symbol']
        response_user_token = requests.get(url=ret1)
        response = response_user_token.json()       
        
        if symbol == "BTC" or "LTC":
            transaction = response['data']
            balance =transaction['balance']
            amountReceived =transaction['amountReceived']
            amountSent =transaction['amountSent']
            transactions = transaction['txs']
            array=[]
            for transaction in transactions:
                fee=transaction['fee']
                to=transaction['outputs'][0]['address']
                timestamp =transaction['timestamp']
                dt_object = datetime.fromtimestamp(timestamp)
                array.append({"fee":fee,"from":address,"to":to,"date":dt_object})
    
        if symbol == "ETH":
            transaction = response['data']
            balance =transaction['balance']
            amountReceived =transaction['amountReceived']
            amountSent =transaction['amountSent']
            transactions = transaction['txs']
            array=[]
            for transaction in transactions:
                to=transaction['to']
                frm=transaction['from']
                price=transaction['quote']['price']
                timestamp =transaction['timestamp']
                dt_object = datetime.fromtimestamp(timestamp)
                array.append({"from":frm,"to":to,"date":dt_object,"fee":price})
    
        ret = mongo.db.address.update({
            "address":address            
        },{
        "$set":{
            "address":address,
            "symbol":symbol
        }},upsert=True)

        ret = mongo.db.address.find_one({
            "address":address
        })
        _id=ret['_id']
        
        ret = mongo.db.balance.update({
            "address":address            
        },{
            "$set":{
                    "record_id":str(_id),    
                    "address":address,
                    "symbol":symbol,
                    "balance":balance,
                    "amountReceived":amountReceived,
                    "amountSent":amountSent
                }},upsert=True)

        ret = mongo.db.transactions.update({
            "address":address            
        },{
            "$set":{
                    "record_id":str(_id),
                    "address":address,
                    "transactions":array,
                    "symbol":symbol
                }},upsert=True)

'''


