import requests
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BNB_balance
from app.config import mydb,mycursor

def bnb_notification(address,symbol,type_id):
    print("ashgajhghgggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
    ret=BNB_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()  
    total_current_tx=transaction['transactions'] 
    print('25')
    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchone()
    tx_count=current_tx[0]
    print('29')
    print("tx_count")
    print(tx_count)
    print("total_current_tx")
    print(total_current_tx)
    if tx_count is None or total_current_tx > tx_count:
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        email_id=email[0]
        print('35')
        if email_id is not None:
            message = Mail(
                from_email=Sendgrid_default_mail,
                to_emails=email_id,
                subject='SafeName - New Transaction Notification In Your Account',
                html_content= '<h3> You got a new transaction on your BNB address</h3>')
            sg = SendGridAPIClient(SendGridAPIClient_key)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
        else:
            print("email is none")
    else:
        print("no new transaction")
