from app.config import mydb,mycursor
from app import mongo
import numpy as np



#-------Scheduler for calculating risk score by if receive fund from heist or heist associated address-------
                        
def Top_user_percentage():
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
        mycursor.execute('UPDATE sws_address SET address_top_rate ="'+str(calculating)+'" WHERE address = "'+str(r_address)+'"')
        mydb.commit()


