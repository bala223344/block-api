import requests
from flask import jsonify
from datetime import datetime
from app import mongo
from app.config import DASH_balance,DASH_transactions
from app.config import DASH_balance
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BTC_balance
from app.config import mydb,mycursor
from sendgrid import SendGridAPIClient



#----------Function for fetching tx_history and balance storing in mongodb ----------

def dash_data(address,symbol,type_id):
    ret=DASH_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    data = response['data']
    addr =data[''+address+'']
    add =addr['address']
    balance =add['balance']
    bal = (balance/100000000)
    receive_amount=add['received']
    send_amount=add['spent']
    transactions=addr['transactions']
    array=[]
    for tran in transactions:
        doc=DASH_transactions.replace("{{address}}",''+tran+'')
        response_user = requests.get(url=doc)
        res = response_user.json()       
        trs =res['data'][''+tran+'']
        inputs=trs['inputs']
        outputs=trs['outputs']
        transact=trs['transaction']
        fee =transact['fee']
        time =transact['time']

        frm=[]
        for inp in inputs:
            recipient = inp['recipient']
            value=inp['value']
            frm.append({"from":recipient,"send_amount":(value/100000000)})
        to=[]
        for out in outputs:
            recipient1 = out['recipient']
            value1=out['value']
            to.append({"to":recipient1,"receive_amount":(value1/100000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":time})

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{  
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "balance":bal,
                "transactions":array,
                "amountReceived":(receive_amount/100000000),
                "amountSent":(send_amount/100000000)
            }},upsert=True)
    return jsonify(bal)



#----------Function for send notification about transactions movement----------

def dash_data(address,symbol,type_id):
    ret=DASH_balance.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    total_current_tx = response['txApperances']

    mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
    current_tx = mycursor.fetchall()
    transactions_count=current_tx[0]
    tx_count=transactions_count[0]
    if tx_count is None or int(total_current_tx) > tx_count:
        mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
        mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
        email = mycursor.fetchone()
        email_id=email[0] 
        
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
        print("no new transaction")











