from app.config import mydb,mycursor
import numpy as np

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
