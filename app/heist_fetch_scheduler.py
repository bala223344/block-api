import requests
from app.config import ETH_SCAM_URL
from app.config import mydb



#-------Scheduler for find ETHERNUM heist addresses-------

def auto_fetch():
    response_user_token = requests.get(url=ETH_SCAM_URL)
    #mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_heist_address` ( id INT,coin varchar(100),tag_name varchar(100),status varchar(100),address varchar(100),source varchar(1000),subcategory varchar(100),description varchar(1500),also_known_as varchar(1000))""")
    response = response_user_token.json()
    result = response['result']
    if result:
        mycur = mydb()
        mycursor = mycur.cursor()
        for record in result:
            if "addresses" in record:
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
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE address="'+str(addresses)+'"')
                    check = mycursor.fetchall()
                    if not check:
                        mycursor.execute('''SELECT MAX(id) FROM sws_heist_address''')
                        maxid = mycursor.fetchone()
                        check=maxid[0]
                        if check is None:
                            ids = 1
                        else:
                            ids=(maxid[0]+1)
                        conversion =description.replace('"','')
                        mycursor.execute('INSERT INTO sws_heist_address (id,coin,tag_name,status,address,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(addresses)+'","https://etherscamdb.info/api/scams","'+str(subcategory)+'","'+str(conversion)+'","'+str(url)+'")')
                        mydb.commit()
                    else:
                        print("already_exist")












































































































