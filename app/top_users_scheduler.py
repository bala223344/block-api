from app.config import mydb,mycursor
from app import mongo
import numpy as np

#-------Scheduler for calculating risk score by if receive fund from heist or heist associated address-------
                        
def Top_user_percentage():
    print("runnnnnn")
    mycursor.execute('SELECT address,address_risk_score FROM sws_address')
    check = mycursor.fetchall()
    all_records_count = len(check)
    data = []
    for record in check:
        risk_score = record[1]
        data.append(risk_score)
    for score in check:
        r_address = score[0]
        r_score = score[1]
        count = 1
        for scr in data:
            if r_score<scr:
                count = count + 1
        calculating = all_records_count*count/all_records_count
        print(r_address)
        print(calculating)
        mycursor.execute('UPDATE sws_address SET address_top_rate ="'+str(calculating)+'" WHERE address = "'+str(r_address)+'"')
        mydb.commit()


        '''
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
        '''
'''
def Top_user_percentage():
    print("runnnnnn")
    mycursor.execute('SELECT address,address_risk_score FROM sws_address')
    check = mycursor.fetchall()
    print("line 150")
100.*len(numpy.where(score>=data)[0])/len(data)
'''
