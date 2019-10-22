import os
from app.config import template
from app.config import mydb,mycursor,SendGridAPIClient_key,Sendgrid_default_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



#-----------scheduler for Pages PGP Verification------------

def pgp_verification():
    mycursor.execute('SELECT username FROM sws_user')
    usernames = mycursor.fetchall()
    for username in usernames:
        user=username[0]
        mycursor.execute('SELECT public_profile_safename,keybase_string FROM sws_user where username=''"' + str(user) + '"''')
        check = mycursor.fetchall()
        details = check[0]
        public_safename = details[0]
        keybase = details[1]
        if not None in (public_safename,keybase):
            changes=template.replace('{{safename}}',''+public_safename+'')
            keybase_changes =changes.replace('{{PGP_sign_key}}',''+keybase+'')
            mycursor.execute('SELECT address,type_id FROM sws_address where cms_login_name=''"' + str(user) + '"''')
            check = mycursor.fetchall()
            no_of_addresses=len(check)
            template_array=[]
            for addr in range(0,no_of_addresses):
                address_details=check[addr]
                addres = address_details[0]
                type_id = address_details[1]
                if type_id == 1:
                    typee = 'Ethereum'
                if type_id == 2:
                    typee = 'Bitcoin'
                if no_of_addresses !=1:
                    if addr == 0:         
                        change=keybase_changes.replace('{{cointype}}',''+typee+'')
                        final_template=change.replace('{{addresses}}',''+addres+'\n' + '{{cointype}}'+'\n' + '{{addresses}}')
                        template_array.append(final_template)
                    elif addr == no_of_addresses-1:
                        tempp=template_array[0]
                        del template_array[0]
                        chan=tempp.replace('{{cointype}}',''+typee+'')
                        template_used=chan.replace('{{addresses}}',''+addres+'')        
                        template_array.append(template_used)
                    else:
                        temp=template_array[0]
                        del template_array[0]
                        changed=temp.replace('{{cointype}}',''+typee+'')
                        final_template=changed.replace('{{addresses}}',''+addres+'\n' + '{{cointype}}'+'\n' + '{{addresses}}')
                        template_array.append(final_template)
                else:
                    change=keybase_changes.replace('{{cointype}}',''+typee+'')
                    final_template=change.replace('{{addresses}}',''+addres+'')
                    template_array.append(final_template)
            template_for_used=template_array[0]
            text=open(r'C:\Users\etech\Desktop\guru99.txt', 'r+')
            text.write(template_for_used)
            text.truncate()
            erification_cammand=os.system(r'''keybase pgp verify -i C:\Users\etech\Desktop\guru99.txt ''')
            print(erification_cammand)
            split_string = str(erification_cammand).split()
            checking_response = str(split_string)
            if "['0']" in checking_response:
                print("success")
            else:
                message = Mail(
                        from_email=Sendgrid_default_mail,
                        to_emails='rasealex000000@gmail.com',
                        subject='SafeName - Invoice Notification In Your Account',
                        html_content= '<h3> Your invoice is not clear please accept the request</h3>' )
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)            
