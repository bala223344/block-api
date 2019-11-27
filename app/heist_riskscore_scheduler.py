from app.config import mydb,mycursor
from app import mongo



#-------Scheduler for calculating risk score by if receive fund from heist or heist associated address-------
                        
def risk_score_by_heist():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),risk_score_by_tx float(3) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
    mycursor.execute('SELECT address,type_id FROM sws_address')
    check = mycursor.fetchall()
    for check in check:
        address=check[0]
        type_id=check[1]
        mycursor.execute('SELECT * FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        if not check:
            mycursor.execute('INSERT INTO `sws_risk_score`(address,type_id) VALUES ("'+str(address)+'","'+str(type_id)+'")')
            mydb.commit()
        
    heist_addresses=[]
    mycursor.execute('SELECT address FROM sws_heist_address WHERE (tag_name <> "heist_associated")')
    ret = mycursor.fetchall()
    for addres in ret:
        address=addres[0]
        heist_addresses.append(address)        

    heist_associated_addresses=[]
    mycursor.execute('SELECT address FROM sws_heist_address WHERE (tag_name = "heist_associated")')
    ret = mycursor.fetchall()
    for add in ret:
        addres=add[0]
        heist_associated_addresses.append(addres)
    mycursor.execute('SELECT address FROM sws_risk_score')
    check = mycursor.fetchall()
    for addr in check:
        address=addr[0]
        records = mongo.db.sws_history.find_one({"address":address})
        if records is not None:
            transactions=records['transactions']
            addresses=[]
            for transaction in transactions:
                fro =transaction['from']
                for frmm in fro:
                    fr = frmm['send_amount']
                    addresses.append(fr)
            for checkk in addresses:
                if checkk in heist_addresses:
                    tx_knownheist_formula =-((50*50)/100)
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_knownheist_formula)+'" WHERE address = "'+str(address)+'"')
                    print("updated_50%")
                    mydb.commit()
                if checkk in heist_associated_addresses:
                    tx_heistassosiated_formula = -((50*30)/100)
                    mycursor.execute('UPDATE sws_risk_score SET riskscore_by_knownheist ="'+str(tx_heistassosiated_formula)+'" WHERE address = "'+str(address)+'"')
                    print("updated_30%")
                    mydb.commit()
                else:
                    pass
        