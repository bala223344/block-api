import time
import datetime
import dateutil.parser
from app import mongo
from app.config import mydb,mycursor,ETH_TRANSACTION_URL,BTC_TRANSACTION
from dateutil.relativedelta import relativedelta

#-------Scheduler for calculating risk score by two year old tx or no transactions heist addresses-------

def tx_two_yearold():
    print("runnnnnn")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `sws_risk_score` ( id INT NOT NULL AUTO_INCREMENT,address varchar(100),risk_score_by_tx float(3) NULL,type_id int(3) NULL,riskscore_by_safename float(3) NULL,riskscore_by_knownheist float(3) NULL,PRIMARY KEY (id))""")
    mycursor.execute('SELECT address,type_id FROM sws_address')
    check = mycursor.fetchall()
    for details in check:
        address=details[0]
        type_id=details[1]
        mycursor.execute('SELECT * FROM sws_risk_score WHERE address="'+str(address)+'"')
        check = mycursor.fetchall()
        if not check:
            mycursor.execute('INSERT INTO `sws_risk_score`(address,type_id) VALUES ("'+str(address)+'","'+str(type_id)+'")')
            mydb.commit()
    mycursor.execute('SELECT address FROM sws_risk_score')
    check = mycursor.fetchall()
    for addrr in check:
        address=addrr[0] 
        records = mongo.db.sws_history.find_one({"address":address})
        if records is not None:
            transactions=records['transactions']
            if transactions:
                count =0
                for transaction in transactions:
                    first_date = transaction['date']
                    date_time = dateutil.parser.parse(str(first_date))
                    month = date_time.strftime("%m/%d/%Y")
                    two_year_back = datetime.datetime.today() + relativedelta(months=-24)
                    back = two_year_back.strftime("%m/%d/%Y")
                    if month<back:
                        count=count+1
                        if count == 4:
                            formula = (50*10)/100
                            mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(formula)+'" WHERE address = "'+str(address)+'"')
                            print("updated_plus")
                            mydb.commit()
                        else:
                            pass
                    else:
                        pass
            else:
                tx_formula = ((50*5)/100)
                mycursor.execute('UPDATE sws_risk_score SET risk_score_by_tx ="'+str(tx_formula)+'" WHERE address = "'+str(address)+'"')
                print("updated_minus")
                mydb.commit()
        
