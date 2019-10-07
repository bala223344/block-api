from app.config import mydb,mycursor,ETH_TRANSACTION_URL,BTC_TRANSACTION



#-------Scheduler for calculating risk score by if receive fund from safename or kyc swsuser heist addresses-------

def risk_score_by_safename():
    print("runnnnnn")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),risk_score_by_tx float(3) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
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
    che = mycursor.fetchall()
    for addr in che:
        cms_name=addr[0]
        kyc_and_secure_addresses.append(cms_name)
    print("300")
    print("308")
    secure_addresses=[]
    mycursor.execute('SELECT u.address FROM db_safename.sws_user as a left join db_safename.sws_address as u on a.username = u.cms_login_name where profile_status = "secure" AND (kyc_verified <> 1 OR kyc_verified is null )') 
    chek = mycursor.fetchall()
    for addr in chek:
        cms_name=addr[0]
        secure_addresses.append(cms_name)
    print("315")
    print("323")
    mycursor.execute('SELECT address FROM sws_risk_score')
    check = mycursor.fetchall()
    for addr in check:
        address=addr[0]
        print(address)
        records = mongo.db.sws_history.find_one({"address":address})
        if records is not None:
            print("488888888888888888888")
            transactions=records['transactions']
            if transactions:
                print("asdasdasdffdasfdasfdfa51")
                addresses=[]
                for transaction in transactions:
                    fro=transaction['from']
                    for fromm in fro:
                        fr = fromm['send_amount']
                        addresses.append(fr)
                for checkk in addresses:
                    print("asdasdadd59")
                    if checkk in kyc_and_secure_addresses:
                        print("adasda")
                        tx_safe_name_formula = (50*10)/100
                        mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'" WHERE address = "'+str(address)+'"')
                        print(checkk)
                        print("updated_10%")
                        mydb.commit()
                    if checkk in secure_addresses:
                        tx_safe_name_formula = (50*5)/100
                        mycursor.execute('UPDATE sws_risk_score SET riskscore_by_safename ="'+str(tx_safe_name_formula)+'" WHERE address = "'+str(address)+'"')
                        print(checkk)
                        print("updated_5%")
                        mydb.commit()
                    else:
                        pass