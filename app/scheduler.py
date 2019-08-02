import requests
from app.util import serialize_doc
from app import mongo
from datetime import datetime
import mysql.connector
from app.config import ETH_SCAM_URL,ETH_TRANSACTION_URL,BTC_TRANSACTION_URL

mydb = mysql.connector.connect( user="VsaqpBhCxL" , password="sW9BgYhqmG", host="remotemysql.com", database="VsaqpBhCxL")
mycursor=mydb.cursor()

def auto_fetch():
    print("runing")
    response_user_token = requests.get(url=ETH_SCAM_URL)
    response = response_user_token.json()
    result = response['result']
    if result:
        for record in result:
            if "addresses" in record:
                name = record['name']
                coin = record['coin']
                category = record['category']
                status =  record['status']
                url = record['url']
                if "subcategory" in record:         
                    subcate = record['subcategory']
                else:
                    subcate = ""
                subcategory = subcate
                if "description" in record:         
                    description = record['description']
                else:
                    description = ""
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
                        print(ids)
                        conversion =description.replace('"','')
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses,url,subcategory,description) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(addresses)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'")')
                        mydb.commit()
    


def heist_associated_fetch():
    mycursor.execute('select coin, addresses from `sws_heist_address`')
    result = mycursor.fetchall()
    for res in result:
        coin = res[0]
        address= res[1]
        if coin == 'ETH':
            print("eth")
            url1=ETH_TRANSACTION_URL
            doc=url1.replace("{{address}}",''+address+'')
            response_user = requests.get(url=doc)
            res = response_user.json()       
            if 'status' in res:
                status_code = res['status']
            else:
                status_code = "1"
            if status_code != "0":
                transactions=res['result']
                frm=[]
                to=[]
                for transaction in transactions:
                    fro =transaction['from']
                    too=transaction['to']
                    to.append({"to":too})
                    frm.append({"from":fro})
                for fund_trans in frm:
                    address=fund_trans['from']
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE addresses="'+str(address)+'"')
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
                        print(ids)
                        name = ""
                        category = "heist_associated"
                        status = "Active"
                        url = ""
                        subcategory = ""
                        conversion = ""
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses,url,subcategory,description) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'")')
                        mydb.commit()
                    else:
                        print("already_exist")
                for fund_reci in to:
                    address=fund_reci['to']
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE addresses="'+str(address)+'"')
                    check = mycursor.fetchall()
                    if not check:
                        print("to_added")
                        mycursor.execute('''SELECT MAX(id) FROM sws_heist_address''')
                        maxid = mycursor.fetchone()
                        check=maxid[0]
                        if check is None:
                            ids = 1
                        else:
                            ids=(maxid[0]+1)
                        print(ids)
                        name = ""
                        category = "heist_associated"
                        status = "Active"
                        url = ""
                        subcategory = ""
                        conversion = ""
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses,url,subcategory,description) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'")')
                        mydb.commit()
                    else:
                        print("already_exist")


        if coin == 'BTC':
            print("btc")
            url1=BTC_TRANSACTION_URL
            doc=url1.replace("{{address}}",''+address+'')
            response_user_token = requests.get(url=doc)
            response = response_user_token.json()
            if 'statusCode' in response:
                status_code = response['statusCode']
            else:
                status_code = 0
            if status_code != 500:
                print(response)
                transaction = response['data']
                transactions = transaction['txs']
                frm = []
                to=[]
                for transaction in transactions:
                    frmm=transaction['inputs']
                    for trans in frmm:
                        fro=trans['address']
                        frm.append({"from":fro})
                    transac=transaction['outputs']
                    for too in transac:
                        addr = too['address'] 
                        to.append({"to":addr})
                for fund_trans in frm:
                    address=fund_trans['from']
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE addresses="'+str(address)+'"')
                    check = mycursor.fetchall()
                    if not check:
                        print("added_btc")
                        mycursor.execute('''SELECT MAX(id) FROM sws_heist_address''')
                        maxid = mycursor.fetchone()
                        check=maxid[0]
                        if check is None:
                            ids = 1
                        else:
                            ids=(maxid[0]+1)
                        print(ids)
                        name = ""
                        category = "heist_associated"
                        status = "Active"
                        url = ""
                        subcategory = ""
                        conversion = ""
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses,url,subcategory,description) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'")')
                        mydb.commit()
                    else:
                        print("already_exist")
                    
                for fund_reci in to:
                    address=fund_reci['to']
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE addresses="'+str(address)+'"')
                    check = mycursor.fetchall()
                    if not check:
                        print("to_added_btc")
                        mycursor.execute('''SELECT MAX(id) FROM sws_heist_address''')
                        maxid = mycursor.fetchone()
                        check=maxid[0]
                        if check is None:
                            ids = 1
                        else:
                            ids=(maxid[0]+1)
                        print(ids)
                        name = ""
                        category = "heist_associated"
                        status = "Active"
                        url = ""
                        subcategory = ""
                        conversion = ""
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses,url,subcategory,description) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'")')
                        mydb.commit()
                    else:
                        print("already_exist")



























    '''
    response_user_token = requests.get(url="https://bitcoinwhoswho.com/api/scam/api-key?address=your-bitcoin-address")
    response = response_user_token.json()
    result = response['result']                    
    '''
                
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


