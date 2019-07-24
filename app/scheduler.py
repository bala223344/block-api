import requests
from app.util import serialize_doc
from app import mongo
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect( user="cguser" , password="cafe@wales1", host="198.38.93.150", database="db_safename")
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
                        print("adsasdas")
                        mycursor.execute('''SELECT MAX(id) FROM sws_heist_address''')
                        maxid = mycursor.fetchone()
                        ids=maxid[0]+1
                        print(ids)
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category,status,addresses) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(addresses)+'")')
                        mydb.commit()
                        
                






