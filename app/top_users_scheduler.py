from app.config import mydb,mycursor
from app import mongo



#-------Scheduler for calculating risk score by if receive fund from heist or heist associated address-------
                        
def Top_user_percentage():
    print("runnnnnn")
    mycursor.execute('SELECT address,address_risk_score FROM sws_address')
    check = mycursor.fetchall()
    print("line 150")
    all_records_count = len(check)
    print("all record count")
    print(all_records_count)
    for record in check:
        addresss = record[0]
        risk_score = record[1]
        mycursor.execute('SELECT address,address_risk_score FROM sws_address')
        record_check = mycursor.fetchall()
        count_riskscore = []
        for records in record_check:
            addre = records[0]
            risk_scor = records[1]
            if risk_score>=risk_scor:
                count_riskscore.append(risk_scor)
        print(count_riskscore)
        if count_riskscore:
            checking = len(count_riskscore)
            print(checking)
            print("risksore lenth")
            formula = all_records_count*checking/all_records_count
        mycursor.execute('UPDATE sws_address SET address_top_rate ="'+str(formula)+'" WHERE address = "'+str(addresss)+'"')
        mydb.commit()