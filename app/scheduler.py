import requests
from app.util import serialize_doc
from app import mongo
from datetime import datetime
import mysql.connector
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from app.config import ETH_SCAM_URL,ETH_TRANSACTION_URL,BTC_TRANSACTION_URL,BTC_TRANSACTION
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
#mydb = mysql.connector.connect(user="VsaqpBhCxL" , password="sW9BgYhqmG", host="remotemysql.com", database="VsaqpBhCxL")
mydb = mysql.connector.connect(host='198.38.93.150',user='dexter',password='cafe@wales1',database='db_safename',auth_plugin='mysql_native_password')
mycursor=mydb.cursor()
#dexter
#-------Scheduler for find ETHERNUM heist addresses-------

def auto_fetch():
    print("runing")
    response_user_token = requests.get(url=ETH_SCAM_URL)
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_heist_address` ( id INT,coin text,tag_name text,status text,address text,source text,subcategory text,description text,also_known_as text)""")
    response = response_user_token.json()
    result = response['result']
    if result:
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
                        mycursor.execute('INSERT INTO sws_heist_address (id,coin,tag_name,status,address,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(addresses)+'","https://etherscamdb.info/api/scams","'+str(subcategory)+'","'+str(conversion)+'","'+str(url)+'")')
                        mydb.commit()
    


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
            url1=BTC_TRANSACTION_URL
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
            

#-------Scheduler for calculating risk score by two year old tx or no transactions heist addresses-------

def tx_two_yearold():
    print("runnnnnn")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),tx_calculated TINYINT(1) NULL,risk_score_by_tx float(3) NULL,tx_cal_by_safename TINYINT(1) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,tx_cal_by_knownheist TINYINT(1) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
    mycursor.execute('SELECT address,type_id FROM sws_address')
    check = mycursor.fetchall()
    print("line 150")
    for a in check:
        address=a[0]
        type_id=a[1]
        print("line 153")
        mycursor.execute('SELECT * FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        if not check:
            mycursor.execute('INSERT INTO `sws_risk_score`(address,type_id) VALUES ("'+str(address)+'","'+str(type_id)+'")')
            mydb.commit()
            print("line 155")
    mycursor.execute('SELECT address,type_id FROM sws_risk_score WHERE (tx_calculated <> 1 OR tx_calculated is null)')
    check = mycursor.fetchall()
    print(check)
    for addrr in check:
        address=addrr[0]
        type_ids=addrr[1]
        print(type_ids)
        if type_ids == 1:
            print("asdddddddddddddddddddddddddddddddddddddddddddddddddd")
            Url = ETH_TRANSACTION_URL
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json()       
            transactions=res['result']
            count =0
            for transaction in transactions:
                if not transaction:
                    tx_formula = ((50*5)/100)
                    mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(tx_formula)+'" WHERE address = "'+str(address)+'"')
                    mycursor.execute('UPDATE sws_risk_score SET tx_calculated =1 WHERE address = "'+str(address)+'"')
                    print("updated_minus")
                    mydb.commit()
                else:
                    timestamp = transaction['timeStamp']
                    first_date=int(timestamp)
                    dt_object = datetime.datetime.fromtimestamp(first_date)
                    month = dt_object.strftime("%m/%d/%Y")
                    two_year_back = datetime.datetime.today() + relativedelta(months=-24)
                    back = two_year_back.strftime("%m/%d/%Y")
                    if month<back:
                        count=count+1
                        if count == 4:
                            formula = (50*10)/100
                            mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(formula)+'" WHERE address = "'+str(address)+'"')
                            mycursor.execute('UPDATE sws_risk_score SET tx_calculated =1 WHERE address = "'+str(address)+'"')
                            print("updated_plus")
                            mydb.commit()
                        else:
                            pass
                    else:
                        pass

        if type_ids == 2:
            print("BTCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            Url =BTC_TRANSACTION
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json()    
            transactions = res['txs']
            count =0
            for transaction in transactions:
                if not transaction:
                    tx_formula = ((50*5)/100)
                    mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(tx_formula)+'" WHERE address = "'+str(address)+'"')
                    mycursor.execute('UPDATE sws_risk_score SET tx_calculated =1 WHERE address = "'+str(address)+'"')
                    print("updated_minus")
                    mydb.commit()
                else:
                    timestamp = transaction['timestamp']
                    first_date=int(timestamp)
                    dt_object = datetime.datetime.fromtimestamp(first_date)
                    month = dt_object.strftime("%m/%d/%Y")
                    two_year_back = datetime.datetime.today() + relativedelta(months=-24)
                    back = two_year_back.strftime("%m/%d/%Y")
                    print(back)
                    print(month)
                    if month<back:
                        count=count+1
                        if count == 4:
                            formula = (50*10)/100
                            mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(formula)+'" WHERE address = "'+str(address)+'"')
                            mycursor.execute('UPDATE sws_risk_score SET tx_calculated =1 WHERE address = "'+str(address)+'"')
                            print("updated_plus")
                            mydb.commit()
                        else:
                            pass
                    else:
                        pass
    
    
    
    
    

#-------Scheduler for calculating risk score by if receive fund from safename or kyc swsuser heist addresses-------

def risk_score_by_safename():
    print("runnnnnn")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),tx_calculated TINYINT(1) NULL,risk_score_by_tx float(3) NULL,tx_cal_by_safename TINYINT(1) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,tx_cal_by_knownheist TINYINT(1) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
    mycursor.execute('SELECT address,type_id FROM sws_address')
    check = mycursor.fetchall()
    print("line 150")
    for a in check:
        address=a[0]
        type_id=a[1]
        print("line 153")
        mycursor.execute('SELECT * FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        if not check:
            mycursor.execute('INSERT INTO `sws_risk_score`(address,type_id) VALUES ("'+str(address)+'","'+str(type_id)+'")')
            mydb.commit()
            print("line 155")

    kyc_secure_users=[]
    mycursor.execute('SELECT username FROM sws_user WHERE (kyc_verified = 1 AND profile_status = "secure")')
    che = mycursor.fetchall()
    for addr in che:
        cms_name=addr[0]
        kyc_secure_users.append(cms_name)


    kyc_and_secure_addresses=[]
    for cms_user in kyc_secure_users:
        mycursor.execute('SELECT address FROM sws_address WHERE (cms_login_name = "'+str(cms_user)+'" AND type_id=1)')
        che = mycursor.fetchall()
        for addr in che:
            addres=addr[0]
            kyc_and_secure_addresses.append(addres)


    secure_users=[]
    mycursor.execute('SELECT username FROM sws_user WHERE profile_status = "secure" AND (kyc_verified <> 1 OR kyc_verified is null )')
    chek = mycursor.fetchall()
    for addr in chek:
        cms_name=addr[0]
        secure_users.append(cms_name)


    secure_addresses=[]
    for cms_user in secure_users:
        mycursor.execute('SELECT address FROM sws_address WHERE (cms_login_name = "'+str(cms_user)+'" AND type_id=1)')
        che = mycursor.fetchall()
        for addr in che:
            addres=addr[0]
            secure_addresses.append(addres)
    print(secure_addresses)

    mycursor.execute('SELECT address FROM sws_risk_score WHERE (tx_cal_by_safename <> 1 OR tx_cal_by_safename is null)')
    check = mycursor.fetchall()

    for addr in check:
        address=addr[0]
        Url = ETH_TRANSACTION_URL
        ret=Url.replace("{{address}}",''+address+'')
        response_user = requests.get(url=ret)
        res = response_user.json()       
        transactions=res['result']
        addresses=[]
        for transaction in transactions:
            fro =transaction['from']
            if fro not in addresses:
                addresses.append(fro)

        for checkk in addresses:
            if checkk in kyc_and_secure_addresses:
                tx_safe_name_formula = (50*10)/100
                mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'" WHERE address = "'+str(address)+'"')
                mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                print(checkk)
                print("updated_10%")
                mydb.commit()
            if checkk in secure_addresses:
                tx_safe_name_formula = (50*5)/100
                mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'" WHERE address = "'+str(address)+'"')
                mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                print(checkk)
                print("updated_5%")
                mydb.commit()
            else:
                pass


#-------Scheduler for calculating risk score by if receive fund from heist or heist associated address-------

                        
def risk_score_by_heist():
    print("runnnnnn")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),tx_calculated TINYINT(1) NULL,risk_score_by_tx float(3) NULL,tx_cal_by_safename TINYINT(1) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,tx_cal_by_knownheist TINYINT(1) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
    mycursor.execute('SELECT address,type_id FROM sws_address')
    check = mycursor.fetchall()
    print("line 150")
    for a in check:
        address=a[0]
        type_id=a[1]
        print("line 153")
        mycursor.execute('SELECT * FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        if not check:
            mycursor.execute('INSERT INTO `sws_risk_score`(address,type_id) VALUES ("'+str(address)+'","'+str(type_id)+'")')
            mydb.commit()
            print("line 155")

    heist_addresses=[]
    mycursor.execute('SELECT address FROM sws_heist_address WHERE (tag_name <> "heist_associated")')
    ret = mycursor.fetchall()
    for addres in ret:
        address=addres[0]
        heist_addresses.append(address)        
    print(len(heist_addresses))

    print("170")
    heist_associated_addresses=[]
    mycursor.execute('SELECT address FROM sws_heist_address WHERE (tag_name = "heist_associated")')
    ret = mycursor.fetchall()
    for add in ret:
        addres=add[0]
        heist_associated_addresses.append(addres)
    print("177")
    mycursor.execute('SELECT address FROM sws_risk_score WHERE (tx_cal_by_knownheist <> 1 OR tx_cal_by_knownheist is null)')
    check = mycursor.fetchall()

    for addr in check:
        address=addr[0]
        Url = ETH_TRANSACTION_URL
        ret=Url.replace("{{address}}",''+address+'')
        response_user = requests.get(url=ret)
        res = response_user.json() 
        print(res)      
        transactions=res['result']
        addresses=[]
        for transaction in transactions:
            fro =transaction['from']
            if fro not in addresses:
                addresses.append(fro)
        print("193")

        for checkk in addresses:
            print("checkkkk")
            if checkk in heist_addresses:
                tx_knownheist_formula =-((50*50)/100)
                mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_knownheist_formula)+'" WHERE address = "'+str(address)+'"')
                mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                print(checkk)
                print("updated_50%")
                mydb.commit()
            if checkk in heist_associated_addresses:
                tx_heistassosiated_formula = -((50*30)/100)
                mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_heistassosiated_formula)+'" WHERE address = "'+str(address)+'"')
                mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                print(checkk)
                print("updated_30%")
                mydb.commit()
            else:
                pass


#--------Scheduler for send new transactions notifications---------

def tx_notification():
    print("asdasndas,na")
    mycursor.execute('SELECT address FROM sws_address WHERE (tx_notification_preferred = 1)')
    sws_addresses = mycursor.fetchall()
    for addres in sws_addresses:
        address=addres
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchall()
        transactions_count=current_tx[0]
        mycursor.execute('SELECT type_id FROM sws_address WHERE address="'+str(address)+'"')
        address_type_id = mycursor.fetchall()
        typ=address_type_id[0]
        type_id = typ[0]
        if type_id == 1:
            total_current_tx = [] 
            Url = ETH_TRANSACTION_URL
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json()
            transactions=res['result']
            total_current_tx=len(transactions)
            new_transaction = transactions[-1]
            print(new_transaction)       
            fro =new_transaction['from']
            too=new_transaction['to']
            timestamp = new_transaction['timeStamp']
            first_date=int(timestamp)
            dt_object = datetime.fromtimestamp(first_date)
            value = new_transaction['value']
            converted_value = (int(value)/1000000000000000000)
            
            tx_count=transactions_count[0]
            print(tx_count)
            if tx_count is None or total_current_tx > tx_count:
                mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
                mycursor.execute('SELECT cms_login_name FROM sws_address WHERE address="'+str(address)+'"')
                cms_login = mycursor.fetchone()
                cms_name=cms_login[0]
                mycursor.execute('SELECT email FROM sws_user WHERE username="'+str(cms_name)+'"')
                email = mycursor.fetchone()
                email_id=email[0]
                print(email_id)
                if email_id is not None:
                    print("sendinnnnnngggggggg")
                    message = Mail(
                        from_email='notifications@safename.io',
                        to_emails=email_id,
                        subject='SafeName - New Transaction Notification In Your Account',
                        html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(fro) + ' </div><strong>To:</strong> ' + str(too) + ' </div><strong>Amount:</strong> ' + str(converted_value) + ' </div><strong>Coin Type:</strong> ''ETH'' ' )
                    sg = SendGridAPIClient('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')
                    response = sg.send(message)
                    print(response.status_code, response.body, response.headers)
            else:
                print("no new transaction")

        if type_id == 2: 
            Url = BTC_TRANSACTION
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json()
            transactions = res['txs']
            total_current_tx = len(transactions)
            for transaction in transactions:                       
                fr = []
                to = []
                timestamp = transaction['timestamp']
                first_date=int(timestamp)
                dt_object = datetime.fromtimestamp(first_date)
                frmm=transaction['inputs']
                for trans in frmm:
                    fro=trans['address']
                    fr.append(fro)
                transac=transaction['outputs']
                for too in transac:
                    t = too['address'] 
                    to.append(t)
            tx_count=transactions_count[0]
            print(tx_count)
            print(total_current_tx)
            if tx_count is None or total_current_tx > tx_count:
                mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
                mycursor.execute('SELECT cms_login_name FROM sws_address WHERE address="'+str(address)+'"')
                cms_login = mycursor.fetchone()
                cms_name=cms_login[0]
                mycursor.execute('SELECT email FROM sws_user WHERE username="'+str(cms_name)+'"')
                email = mycursor.fetchone()
                email_id=email[0]
                if email_id is not None:
                    print("sending")
                    message = Mail(
                        from_email='notifications@safename.io',
                        to_emails='aayushsaini000000@gmail.com',
                        subject='SafeName - New Transaction Notification In Your Account',
                        html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(fr) + ' </div><strong>To:</strong> ' + str(to) + ' </div><div><strong>Amount:</strong> ' + 'No Data' + ' </div><strong>Coin Type:</strong> ''BTC'' ' )
                    sg = SendGridAPIClient('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')
                    response = sg.send(message)
                    print(response.status_code, response.body, response.headers)
            else:
                print("no new transaction")






























































#-------scheduler for calculating overall riskscore from sws_risk_score table and update in sws_address table------- 
'''
def risk_score():
    mycursor.execute('SELECT address FROM sws_risk_score')
    check = mycursor.fetchall()
    for addr in check:
        address=addr[0]
        mycursor.execute('SELECT risk_score_by_tx,riskscore_by_safename,riskscore_by_knownheist FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        for record in check:
            print(record)
            score = 0
            for lst in record:
                if lst is not None:
                    score = lst+score
            risk_score = 50+score
            mycursor.execute('UPDATE sws_address SET address_risk_score="'+str(risk_score)+'" WHERE address = "'+str(address)+'"')
            print("updated")
            mydb.commit()
'''


















'''
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
                        mycursor.execute('SELECT MAX(id) FROM sws_heist_address'')
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
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category_tags,status,addresses,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'","related to heist_address")')
                        mydb.commit()
                    else:
                        print("already_exist")
                    
                for fund_reci in to:
                    address=fund_reci['to']
                    mycursor.execute('SELECT * FROM sws_heist_address WHERE addresses="'+str(address)+'"')
                    check = mycursor.fetchall()
                    if not check:
                        print("to_added_btc")
                        mycursor.execute(''SELECT MAX(id) FROM sws_heist_address'')
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
                        mycursor.execute('INSERT INTO sws_heist_address (id,name,coin,category_tags,status,addresses,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(name)+'","'+str(coin)+'","'+str(category)+'","'+str(status)+'","'+str(address)+'","'+str(url)+'","'+str(subcategory)+'","'+str(conversion)+'","related to heist_address")')
                        mydb.commit()
                    else:
                        print("already_exist")
'''


























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


