
import requests
from app.config import mydb,mycursor,ETH_TRANSACTION_URL,BTC_TRANSACTION



#-------Scheduler for find ETHERNUM heist assosiated addresses-------

def heist_associated_fetch():
    print("runningggggg")
    mycursor.execute('select coin, address from `sws_heist_address`')
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
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE address="'+str(address)+'"')
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
                        category = "heist_associated"
                        status = "Active"
                        url = ""
                        subcategory = ""
                        conversion = ""
                        mycursor.execute('INSERT INTO sws_heist_address (id,coin,tag_name,status,address,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'","related to heist_address")')
                        mydb.commit()
                    else:
                        print("already_exist")
                for fund_reci in to:
                    address=fund_reci['to']
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE address="'+str(address)+'"')
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
                        mycursor.execute('INSERT INTO sws_heist_address (id,coin,tag_name,status,address,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'","related to heist_address")')
                        mydb.commit()
                    else:
                        print("already_exist")
        if coin == 'BTC':
            print("btc")
            url1=BTC_TRANSACTION
            doc=url1.replace("{{address}}",''+address+'')
            response_user = requests.get(url=doc)
            res = response_user.json()       
            transactions = res['txs']
            frm=[]
            for transaction in transactions:
                frmm=transaction['inputs']
                for trans in frmm:
                    fro=trans['address']
                    frm.append({"from":fro})
            for fund_trans in frm:
                address=fund_trans['from']
                mycursor.execute('SELECT * FROM sws_heist_address WHERE address="'+str(address)+'"')
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
                    category = "heist_associated"
                    status = "Active"
                    url = ""
                    subcategory = ""
                    conversion = ""
                    mycursor.execute('INSERT INTO sws_heist_address (id,coin,tag_name,status,address,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'","related to heist_address")')
                    mydb.commit()
                else:
                    print("already_exist")
