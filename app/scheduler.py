import requests
from app.util import serialize_doc
from app import mongo
from flask import (
    Blueprint,request,jsonify,abort
)
import time
import mysql.connector
from dateutil.relativedelta import relativedelta
import datetime
from app.config import ETH_SCAM_URL,ETH_TRANSACTION_URL,BTC_TRANSACTION_URL,BTC_TRANSACTION,SendGridAPIClient_key,Sendgrid_default_mail,template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import numpy as np


#-----calling functions from app----
from app.eth_notification import eth_notification
from app.btc import btc_data
from app.erc_coins import erc_coin_data




#-------Sql connection informations----------

#mydb = mysql.connector.connect(user="VsaqpBhCxL" , password="sW9BgYhqmG", host="remotemysql.com", database="VsaqpBhCxL")
mydb = mysql.connector.connect(host='198.38.93.150',user='dexter',password='cafe@wales1',database='db_safename',auth_plugin='mysql_native_password')
mycursor=mydb.cursor()
#dexter



#-------Scheduler for find ETHERNUM heist addresses-------

def auto_fetch():
    print("runing")
    response_user_token = requests.get(url=ETH_SCAM_URL)
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_heist_address` ( id INT,coin varchar(100),tag_name varchar(100),status varchar(100),address varchar(100),source varchar(1000),subcategory varchar(100),description varchar(1500),also_known_as varchar(1000))""")
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
                    else:
                        print("already_exist")


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
            


#-------Scheduler for calculating risk score by two year old tx or no transactions heist addresses-------

def tx_two_yearold():
    print("runnnnnn")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),tx_calculated TINYINT(1) NULL,risk_score_by_tx float(3) NULL,tx_cal_by_safename TINYINT(1) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,tx_cal_by_knownheist TINYINT(1) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
    mycursor.execute('SELECT address,type_id FROM sws_address')
    check = mycursor.fetchall()
    print("line 150")
    for details in check:
        address=details[0]
        type_id=details[1]
        print("line 153")
        mycursor.execute('SELECT * FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        if not check:
            mycursor.execute('INSERT INTO `sws_risk_score`(address,type_id) VALUES ("'+str(address)+'","'+str(type_id)+'")')
            mydb.commit()
            print("line 155")
    mycursor.execute('SELECT address,type_id FROM sws_risk_score WHERE (tx_calculated <> 1 OR tx_calculated is null)')
    check = mycursor.fetchall()
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
                    mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(tx_formula)+'",tx_calculated =1 WHERE address = "'+str(address)+'"')
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
                            mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(formula)+'",tx_calculated =1 WHERE address = "'+str(address)+'"')
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
                    mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(tx_formula)+'",tx_calculated =1 WHERE address = "'+str(address)+'"')
                    #mycursor.execute('UPDATE sws_risk_score SET tx_calculated =1 WHERE address = "'+str(address)+'"')
                    print("updated_minus")
                    mydb.commit()
                else:
                    timestamp = transaction['timestamp']
                    print(timestamp)
                    first_date=int(timestamp)
                    print(first_date)
                    dt_object = datetime.datetime.fromtimestamp(first_date)
                    print(dt_object)
                    month = dt_object.strftime("%m/%d/%Y")
                    two_year_back = datetime.datetime.today() + relativedelta(months=-24)
                    back = two_year_back.strftime("%m/%d/%Y")
                    print(back)
                    print(month)
                    if month<back:
                        count=count+1
                        if count == 4:
                            formula = (50*10)/100
                            mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(formula)+'",tx_calculated =1 WHERE address = "'+str(address)+'"')
                            #mycursor.execute('UPDATE sws_risk_score SET tx_calculated =1 WHERE address = "'+str(address)+'"')
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
    kyc_and_secure_addresses=[]
    mycursor.execute('SELECT u.address FROM db_safename.sws_user as a left join db_safename.sws_address as u on a.username = u.cms_login_name where (kyc_verified = 1 AND profile_status = "secure")')
    #SELECT u.address FROM db_safename.sws_user as a left join db_safename.sws_address as u on a.username = u.cms_login_name where (kyc_verified = 1 AND profile_status = "secure"); 
    che = mycursor.fetchall()
    for addr in che:
        cms_name=addr[0]
        kyc_and_secure_addresses.append(cms_name)
    print("300")
    print("308")
    secure_addresses=[]
    mycursor.execute('SELECT u.address FROM db_safename.sws_user as a left join db_safename.sws_address as u on a.username = u.cms_login_name where profile_status = "secure" AND (kyc_verified <> 1 OR kyc_verified is null )')
    #SELECT u.address FROM db_safename.sws_user as a left join db_safename.sws_address as u on a.username = u.cms_login_name where profile_status = "secure" AND (kyc_verified <> 1 OR kyc_verified is null ); 
    chek = mycursor.fetchall()
    for addr in chek:
        cms_name=addr[0]
        secure_addresses.append(cms_name)
    print("315")
    print("323")
    print(secure_addresses)
    mycursor.execute('SELECT address,type_id FROM sws_risk_score WHERE (tx_cal_by_safename <> 1 OR tx_cal_by_safename is null)')
    check = mycursor.fetchall()
    for addr in check:
        address=addr[0]
        type_id=addr[1]
        print(address)
        print(type_id)
        if type_id==1:
            Url = ETH_TRANSACTION_URL
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json()       
            transactions=res['result']
            print("339")
            addresses=[]
            for transaction in transactions:
                fro =transaction['from']
                if fro not in addresses:
                    addresses.append(fro)
            print("345")
            for checkk in addresses:
                if checkk in kyc_and_secure_addresses:
                    print("adasda")
                    tx_safe_name_formula = (50*10)/100
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'",tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                   # mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                    print(checkk)
                    print("updated_10%")
                    mydb.commit()
                if checkk in secure_addresses:
                    tx_safe_name_formula = (50*5)/100
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'",tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                  #  mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                    print(checkk)
                    print("updated_5%")
                    mydb.commit()
                else:
                    pass
        if type_id==2:
            print("type_id 2")
            Url = BTC_TRANSACTION
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json()       
            transactions = res['txs']
            addresses=[]
            for transaction in transactions:
                frmm=transaction['inputs']
                for trans in frmm:
                    fro=trans['address']
                    if fro not in addresses:
                        addresses.append(fro)
            for checkk in addresses:
                if checkk in kyc_and_secure_addresses:
                    tx_safe_name_formula = (50*10)/100
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'",tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                    #mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                    print(checkk)
                    print("updated_10%")
                    mydb.commit()
                if checkk in secure_addresses:
                    tx_safe_name_formula = (50*5)/100
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'",tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
                    #mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_safename =1 WHERE address = "'+str(address)+'"')
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
    for check in check:
        address=check[0]
        type_id=check[1]
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
    mycursor.execute('SELECT address,type_id FROM sws_risk_score WHERE(tx_cal_by_knownheist <> 1 OR tx_cal_by_knownheist is null)')
    check = mycursor.fetchall()
    for addr in check:
        address=addr[0]
        type_id=addr[1]
        if type_id==1:
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
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_knownheist_formula)+'",tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                    #mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                    print("updated_50%")
                    mydb.commit()
                if checkk in heist_associated_addresses:
                    tx_heistassosiated_formula = -((50*30)/100)
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_heistassosiated_formula)+'",tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                    #mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                    print("updated_30%")
                    mydb.commit()
                else:
                    pass
        if type_id==2:
            Url = BTC_TRANSACTION
            ret=Url.replace("{{address}}",''+address+'')
            response_user = requests.get(url=ret)
            res = response_user.json() 
            transactions = res['txs']
            addresses=[]
            for transaction in transactions:
                frmm=transaction['inputs']
                for trans in frmm:
                    fro=trans['address']
                    if fro not in addresses:
                        addresses.append(fro)
            print("193")
            for checkk in addresses:
                print("checkkkk")
                if checkk in heist_addresses:
                    tx_knownheist_formula =-((50*50)/100)
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_knownheist_formula)+'",tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                #    mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                    print(checkk)
                    print("updated_50%")
                    mydb.commit()
                if checkk in heist_associated_addresses:
                    tx_heistassosiated_formula = -((50*30)/100)
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_heistassosiated_formula)+'",tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                #    mycursor.execute('UPDATE sws_risk_score SET tx_cal_by_knownheist =1 WHERE address = "'+str(address)+'"')
                    print(checkk)
                    print("updated_30%")
                    mydb.commit()
                else:
                    pass



#-------scheduler for calculating overall riskscore from sws_risk_score table and update in sws_address table------- 

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



#-------scheduler for calculating overall profile riskscore------- 

def profile_risk_score():
    print("asdasndas,na")
    mycursor.execute('SELECT username FROM sws_user')
    sws_users = mycursor.fetchall()
    for user in sws_users:
        user_name=user[0]
        mycursor.execute('SELECT address_risk_score FROM sws_address WHERE cms_login_name="'+str(user_name)+'"')
        risk_scores = mycursor.fetchall()
        list_of_scores=[]
        for risk_score in risk_scores:
            score = risk_score[0]
            list_of_scores.append(score)
        if list_of_scores:
            avrage = np.mean(list_of_scores)
            mycursor.execute('SELECT profile_risk_score_by_kyc_options FROM sws_user WHERE username="'+str(user_name)+'"')
            risk_scores = mycursor.fetchone()
            risk_score_kyc = risk_scores[0]
            final_profile_riskscore=risk_score_kyc+avrage
            mycursor.execute('UPDATE sws_user SET profile_risk_score="'+str(final_profile_riskscore)+'" WHERE username = "'+str(user_name)+'"')


#-----------scheduler for send email notification------------

def invoice_notification():
    print("asdasndas,na")
    dab = mongo.db.sws_pending_txs_from_app.find({
        "type":"invoice"})
    dab = [serialize_doc(doc) for doc in dab]
    for data in dab:
        frm=data['from']
        to = data['to']
        symbol = data['symbol']
        amount=data['amount']
        notes = data['notes']
        
        dabb = mongo.db.sws_history.find({
            "address": to,
            "transactions": {'$elemMatch': {"from":{'$elemMatch':{"from":to,"send_amount":amount}}, "to":{'$elemMatch':{"to":frm}}}}
        },{"transactions.$": 1 })
        dabb=[serialize_doc(doc) for doc in dabb]

        if dabb:
            for data in dabb:
                trans = data['transactions']
                for tx_id in trans:
                    transaction_id = tx_id['Tx_id']
            docs = mongo.db.sws_pending_txs_from_app.remove({
                "from": frm,
                "to": to,
                "amount": amount,
                "type":"invoice"
            })            
            report = mongo.db.sws_notes.insert_one({
                "tx_id": transaction_id,
                "notes": notes
            }).inserted_id
        else:
            mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(to)+'"')
            email = mycursor.fetchone()
            print(email)
            if email is not None:
                email_id=email[0]
                print(email_id)
                message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - Invoice Notification In Your Account',
                        html_content= '<h3> Your invoice is not clear please accept the request</h3>' )
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)



#-----------scheduler for Pages PGP Verification------------

def pgp_verification():
    mycursor.execute('SELECT username FROM sws_user')
    usernames = mycursor.fetchall()
    for username in usernames:
        user=username[0]
        mycursor.execute('SELECT public_profile_safename,keybase_string FROM sws_user where username=''"' + str(user) + '"''')
        check = mycursor.fetchall()
        details = check[0]
        public_safename = details[0]
        keybase = details[1]
        if not None in (public_safename,keybase):
            changes=template.replace('{{safename}}',''+public_safename+'')
            keybase_changes =changes.replace('{{PGP_sign_key}}',''+keybase+'')
            mycursor.execute('SELECT address,type_id FROM sws_address where cms_login_name=''"' + str(user) + '"''')
            check = mycursor.fetchall()
            no_of_addresses=len(check)
            print(no_of_addresses)
            template_array=[]
            for addr in range(0,no_of_addresses):
                address_details=check[addr]
                addres = address_details[0]
                type_id = address_details[1]
                if type_id == 1:
                    typee = 'Ethereum'
                if type_id == 2:
                    typee = 'Bitcoin'
                if no_of_addresses !=1:
                    if addr == 0:
                        print("if")            
                        change=keybase_changes.replace('{{cointype}}',''+typee+'')
                        final_template=change.replace('{{addresses}}',''+addres+'\n' + '{{cointype}}'+'\n' + '{{addresses}}')
                        template_array.append(final_template)
                    elif addr == no_of_addresses-1:
                        print("elif")
                        tempp=template_array[0]
                        del template_array[0]
                        chan=tempp.replace('{{cointype}}',''+typee+'')
                        template_used=chan.replace('{{addresses}}',''+addres+'')        
                        template_array.append(template_used)
                    else:
                        print("else")
                        temp=template_array[0]
                        del template_array[0]
                        changed=temp.replace('{{cointype}}',''+typee+'')
                        final_template=changed.replace('{{addresses}}',''+addres+'\n' + '{{cointype}}'+'\n' + '{{addresses}}')
                        template_array.append(final_template)
                else:
                    change=keybase_changes.replace('{{cointype}}',''+typee+'')
                    final_template=change.replace('{{addresses}}',''+addres+'')
                    template_array.append(final_template)
            template_for_used=template_array[0]
            text=open(r'C:\Users\etech\Desktop\guru99.txt', 'r+')
            text.write(template_for_used)
            text.truncate()
            erification_cammand=os.system(r'''keybase pgp verify -i C:\Users\etech\Desktop\guru99.txt ''')
            print(erification_cammand)
            split_string = str(erification_cammand).split()
            checking_response = str(split_string)
            if "['0']" in checking_response:
                print("success")
            else:
                message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - Invoice Notification In Your Account',
                        html_content= '<h3> Your invoice is not clear please accept the request</h3>' )
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)            



#--------Scheduler for fthcing tx_history and update db and send msg notification if got a new one--------

def tx_notification():
    print("asdasndas,na")
    mycursor.execute('SELECT address,type_id FROM sws_address WHERE tx_notification_preferred = "1" AND (address_status = "verified" OR address_status = "secure")')
    sws_addresses = mycursor.fetchall()
    print(sws_addresses)
    for addres in sws_addresses:
        address=addres[0]
        type_id = addres[1] 
        
        if type_id == 1:
            symbol = 'ETH'
            currency = eth_notification(address,symbol,type_id)        
        '''
        if type_id == 2:
            symbol = 'BTC'
            currency = btc_data(address,symbol,type_id)
        
        if type_id == 3:
            symbol = 'ZRX'
            currency = erc_coin_data(address,symbol,type_id)
        
        if type_id == 5:
            symbol = 'ELF'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 8:
            symbol = 'REP'
            currency = erc_coin_data(address,symbol,type_id)
           
        if type_id == 9:
            symbol = 'AOA'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 10:
            symbol = 'BAT'
            currency = erc_coin_data(address,symbol,type_id)
        
        if type_id == 21:
            symbol = 'LINK'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 22:
            symbol = 'CCCX'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 24:
            symbol = 'MCO'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 25:
            symbol = 'CRO'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 26:
            symbol = 'DAI'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 31:
            symbol = 'EKT'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 32:
            symbol = 'EGT'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 34:
            symbol = 'ENJ'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 38:
            symbol = 'GNT'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 42:
            symbol = 'HT'
            currency = erc_coin_data(address,symbol,type_id)
        
        if type_id == 45:
            symbol = 'INB'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 50:
            symbol = 'KCS'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 51:
            symbol = 'LAMB'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 11:
            symbol = 'BNB'
            currency = erc_coin_data(address,symbol,type_id)
    
        
        if type_id == 46:
            symbol = 'IOST'
            currency = erc_coin_data(address,symbol,type_id)
        
    
        if type_id == 44:
            symbol = 'ICX'
            currency = erc_coin_data(address,symbol,type_id)
        
        
        if type_id == 41:
            symbol = 'HOT'
            currency = erc_coin_data(address,symbol,type_id)
        

        if type_id == 75:
            symbol = 'XRP'
            currency = xrp_data(address,symbol,type_id)
        
        
        if type_id == 12:
            symbol = 'BCH'
            currency = bch_data(address,symbol,type_id)
    
    
        if type_id == 53:
            symbol = 'LTC'
            currency = ltc_data(address,symbol,type_id)

        '''
    
    
    
    
    
    
    
    























#-----------------Dummy code But not trash----------------------------



#--------Scheduler for send new transactions notifications---------

'''
from datetime import datetime
def tx_notification():
    print("asdasndas,na")
    mycursor.execute('SELECT address FROM sws_address WHERE (tx_notification_preferred = 1)')
    sws_addresses = mycursor.fetchall()
    for addres in sws_addresses:
        address=addres[0]
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchall()
        print(current_tx)
        transactions_count=current_tx[0]
        mycursor.execute('SELECT type_id FROM sws_address WHERE address="'+str(address)+'"')
        address_type_id = mycursor.fetchall()
        typ=address_type_id[0]
        type_id = typ[0]
        print(type_id)
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
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - New Transaction Notification In Your Account',
                        html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(fro) + ' </div><strong>To:</strong> ' + str(too) + ' </div><strong>Amount:</strong> ' + str(converted_value) + ' </div><strong>Coin Type:</strong> ''ETH'' ' )
                    sg = SendGridAPIClient(SendGridAPIClient_key)
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
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - New Transaction Notification In Your Account',
                        html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(fr) + ' </div><strong>To:</strong> ' + str(to) + ' </div><div><strong>Amount:</strong> ' + 'No Data' + ' </div><strong>Coin Type:</strong> ''BTC'' ' )
                    sg = SendGridAPIClient(SendGridAPIClient_key)
                    response = sg.send(message)
                    print(response.status_code, response.body, response.headers)
            else:
                print("no new transaction")
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


'''
    kyc_and_secure_addresses=[]
    for cms_user in kyc_secure_users:
        mycursor.execute('SELECT address FROM sws_address WHERE (cms_login_name = "'+str(cms_user)+'")')
        che = mycursor.fetchall()
        for addr in che:
            addres=addr[0]
            kyc_and_secure_addresses.append(addres)
'''
'''
    secure_addresses=[]
    for cms_user in secure_users:
        mycursor.execute('SELECT address FROM sws_address WHERE (cms_login_name = "'+str(cms_user)+'")')
        che = mycursor.fetchall()
        for addr in che:
            addres=addr[0]
            secure_addresses.append(addres)
'''