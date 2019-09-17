import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import DASH_balance

#----------Function for fetching tx_history and balance storing in mongodb ----------

def dash_data(address,symbol,type_id):
    ret=DASH_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    total_current_tx = response['txApperances']

    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchall()
    transactions_count=current_tx[0]
    tx_count=transactions_count[0]
    print("tx_count")
    print(tx_count)
    print("total_current_tx")
    print(total_current_tx)
    if tx_count is None or int(total_current_tx) > tx_count:
        print("93")
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        print(address)
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        email_id=email[0]
        print(email_id) 
        
        if email_id is not None:    
            message = Mail(
                    from_email=Sendgrid_default_mail,
                    to_emails="rasealex000000@gmail.com",
                    subject='SafeName - New Transaction Notification In Your Account',
                    html_content= '<h3> You got a new transaction </h3><strong>Date:</strong> ' + str(dt_object) +' <div><strong>From:</strong> ' + str(frm_safename) + ' </div><strong>To:</strong> ' + str(to_safename) + ' </div><div><strong>Amount:</strong> ' + str(send_amount) + ' </div><div><strong>Tx_id:</strong> ' + str(tx_id) + ' </div><div><strong>Coin Type:</strong> ''ETH''  </div>' )
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
                print("email is not none")
        else:
            print("amount is 0")
    else:
        print("no new transaction")
else:
    print("no transcations")

return jsonify({"status":"success"})
