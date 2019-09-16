
import requests
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import mongo
from app.config import ETH_transactions
from app.config import mydb,mycursor,Sendgrid_default_mail,SendGridAPIClient_key


#----------Function for fetching tx_history and balance for ETH storing in mongodb also send notification if got new one----------

def eth_notification(address,symbol,type_id):    
    doc=ETH_transactions.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()  
    transactions=res['result']
    if transactions:
        total_current_tx=len(transactions)
        transaction = transactions[-1]

        timestamp = transaction['timeStamp']
        first_date=int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        fro =transaction['from']
        too=transaction['to']
        send_amount=(int(transaction['value'])/1000000000000000000)
        tx_id = transaction['hash']
        print("87")
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchall()
        transactions_count=current_tx[0]
        tx_count=transactions_count[0]
        if tx_count is None or total_current_tx > tx_count:
            print("93")
            if send_amount != 0:
                print("105")
                mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
                print(address)
                mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
                email = mycursor.fetchone()
                email_id=email[0]
                print(email_id) 
                
                if email_id is not None:
                    '''
                    print("sendinnnnnngggggggg")
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(fro)+'"')
                    from_safename_tx = mycursor.fetchall()
                    if from_safename_tx:
                        frm_safenames=from_safename_tx[0]
                        frm = frm_safenames[0]
                        frm_safename=fro+'(safename:'+frm+')'
                    else:
                        frm_safename=fro
                    mycursor.execute('SELECT address_safename FROM sws_address WHERE address="'+str(too)+'"')
                    too_safenames_tx = mycursor.fetchall()
                    if too_safenames_tx:
                        too_safenames=too_safenames_tx[0]
                        to = too_safenames[0]
                        to_safename=too+'(safename:'+to+')'
                    else:
                        to_safename=too
                    '''    
                    frm_safename=fro
                    to_safename=too
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

