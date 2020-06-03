from app.config import mydb,mycursor
from app.eth import eth_notification
from app.btc import btc_notification
from app.xrp import xrp_notification
from app.bch import bch_notification
from app.ltc import ltc_notification
from app.bnb import bnb_notification
from app.bsv import bsv_notification
from app.dash import dash_notification
from app.zcash import zcash_notification
from app.mkr import mkr_notification
from app.link import link_notification
from app.btg import btg_notification
from app.zrx import zrx_notification
from app.elf import elf_notification
from app.rep import rep_notification
from app.aoa import aoa_notification
from app.bat import bat_notification
from app.cccx import cccx_notification
from app.mco import mco_notification
from app.cro import cro_notification
from app.dai import dai_notification
from app.ekt import ekt_notification
from app.egt import egt_notification
from app.enj import enj_notification
from app.gnt import gnt_notification
from app.hot import hot_notification
from app.ht import ht_notification
from app.icx import icx_notification
from app.inb import inb_notification
from app.kcs import kcs_notification
from app.lamb import lamb_notification
from app.iost import iost_notification
from app.jct import jct_notification
from app.maid import maid_notification
from app.mxm import mxm_notification
from app.xin import xin_notification


def tx_notification1():
    tx_notification()

def tx_notification2():
    tx_notification()

#----------Function for new transaction notification----------

def tx_notification():
    mycursor.execute('SELECT address,type_id FROM sws_address WHERE tx_notification_preferred = "1"')
    sws_addresses = mycursor.fetchall()
    for addres in sws_addresses:
        try:
            address=addres[0]
            type_id = addres[1] 
            
            if type_id == 1:
                symbol = 'ETH'
                currency = eth_notification(address,symbol,type_id)        

            if type_id == 3:
                symbol = 'ZRX'
                currency = zrx_notification(address,symbol,type_id)

            if type_id == 2:
                symbol = 'BTC'
                currency = btc_notification(address,symbol,type_id)

            if type_id == 5:
                symbol = 'ELF'
                currency = elf_notification(address,symbol,type_id)
            
            if type_id == 27:
                symbol = 'DASH'
                currency = dash_notification(address,symbol,type_id)

            if type_id == 12:
                symbol = 'BCH'
                currency = bch_notification(address,symbol,type_id)

            if type_id == 98:
                symbol = 'ZEC'
                currency = zcash_notification(address,symbol,type_id)

            if type_id == 55:
                symbol = 'MKR'
                currency = mkr_notification(address,symbol,type_id)

            if type_id == 21:
                symbol = 'LINK'
                currency = link_notification(address,symbol,type_id)

            if type_id == 11:
                symbol = 'BNB'
                currency = bnb_notification(address,symbol,type_id)

            if type_id == 75:
                symbol = 'XRP'
                currency = xrp_notification(address,symbol,type_id)

            if type_id == 53:
                symbol = 'LTC'
                currency = ltc_notification(address,symbol,type_id)

            if type_id == 14:
                symbol = 'BTG'
                currency = btg_notification(address,symbol,type_id)

            if type_id == 15:
                symbol = 'BSV'
                currency = bsv_notification(address,symbol,type_id)

            if type_id == 8:
                symbol = 'REP'
                currency = rep_notification(address,symbol,type_id)

            if type_id == 9:
                symbol = 'AOA'
                currency = aoa_notification(address,symbol,type_id)

            if type_id == 10:
                symbol = 'BAT'
                currency = bat_notification(address,symbol,type_id)

            if type_id == 22:
                symbol = 'CCCX'
                currency = cccx_notification(address,symbol,type_id)

            if type_id == 24:
                symbol = 'MCO'
                currency = mco_notification(address,symbol,type_id)

            if type_id == 25:
                symbol = 'CRO'
                currency = cro_notification(address,symbol,type_id)

            if type_id == 26:
                symbol = 'DAI'
                currency = dai_notification(address,symbol,type_id)

            if type_id == 31:
                symbol = 'EKT'
                currency = ekt_notification(address,symbol,type_id)

            if type_id == 32:
                symbol = 'EGT'
                currency = egt_notification(address,symbol,type_id)

            if type_id == 34:
                symbol = 'ENJ'
                currency = enj_notification(address,symbol,type_id)

            if type_id == 38:
                symbol = 'GNT'
                currency = gnt_notification(address,symbol,type_id)

            if type_id == 41:
                symbol = 'HOT'
                currency = hot_notification(address,symbol,type_id)

            if type_id == 42:
                symbol = 'HT'
                currency = ht_notification(address,symbol,type_id)

            if type_id == 44:
                symbol = 'ICX'
                currency = icx_notification(address,symbol,type_id)

            if type_id == 45:
                symbol = 'INB'
                currency = inb_notification(address,symbol,type_id)

            if type_id == 50:
                symbol = 'KCS'
                currency = kcs_notification(address,symbol,type_id)

            if type_id == 51:
                symbol = 'LAMB'
                currency = lamb_notification(address,symbol,type_id)

            if type_id == 46:
                symbol = 'IOST'
                currency = iost_notification(address,symbol,type_id)

            if type_id == 48:
                symbol = 'JCT'
                currency = jct_notification(address,symbol,type_id)

            if type_id == 54:
                symbol = 'MAID'
                currency = maid_notification(address,symbol,type_id)

            if type_id == 56:
                symbol = 'MXM'
                currency = mxm_notification(address,symbol,type_id)

            if type_id == 58:
                symbol = 'XIN'
                currency = xin_notification(address,symbol,type_id)
        except Exception:
            pass

        '''
        if type_id == 75:
            symbol = 'XRP'
            currency = xrp_notification(address,symbol,type_id)
        

        if type_id == 12:
            symbol = 'BCH'
            currency = bch_notification(address,symbol,type_id)        
        

        if type_id == 53:
            symbol = 'LTC'
            currency = ltc_notification(address,symbol,type_id)        
    

        if type_id == 35:
            symbol = 'EOS'
            currency = eos_notification(address,symbol,type_id)        
        
        
        if type_id == 11:
            symbol = 'BNB'
            currency = bnb_notification(address,symbol,type_id)
        
        if type_id == 15:
            symbol = 'BSV'
            currency = bsv_notification(address,symbol,type_id)
        '''

        
        '''
        if type_id == 3:
            symbol = 'ZRX'
            currency = erc_coin_data(address,symbol,type_id)
        
        if type_id == 5:
            symbol = 'ELF'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 8:
            symbol = 'REP'
            currency = erc_coin_data(address,symbol,type_id)
           
        if type_id == 9:
            symbol = 'AOA'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 10:
            symbol = 'BAT'
            currency = erc_coin_data(address,symbol,type_id)
        
        if type_id == 21:
            symbol = 'LINK'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 22:
            symbol = 'CCCX'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 24:
            symbol = 'MCO'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 25:
            symbol = 'CRO'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 26:
            symbol = 'DAI'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 31:
            symbol = 'EKT'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 32:
            symbol = 'EGT'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 34:
            symbol = 'ENJ'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 38:
            symbol = 'GNT'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 42:
            symbol = 'HT'
            currency = erc_coin_data(address,symbol,type_id)
        
        if type_id == 45:
            symbol = 'INB'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 50:
            symbol = 'KCS'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 51:
            symbol = 'LAMB'
            currency = erc_coin_data(address,symbol,type_id)

        if type_id == 11:
            symbol = 'BNB'
            currency = erc_coin_data(address,symbol,type_id)
    
        
        if type_id == 46:
            symbol = 'IOST'
            currency = erc_coin_data(address,symbol,type_id)
        
    
        if type_id == 44:
            symbol = 'ICX'
            currency = erc_coin_data(address,symbol,type_id)
        
        
        if type_id == 41:
            symbol = 'HOT'
            currency = erc_coin_data(address,symbol,type_id)
                
        
        if type_id == 12:
            symbol = 'BCH'
            currency = bch_data(address,symbol,type_id)
    
    
        if type_id == 53:
            symbol = 'LTC'
            currency = ltc_data(address,symbol,type_id)
        '''


























'''
from app.btc import btc_data
from app.eth import eth_data,eth_data_internal
from app.bnb import bnb_data
from app.bch import btc_cash_data
from app.bsv import bitcoin_svs_data
from app.ltc import ltc_data
from app.tether import tether_data
from app.xtz import xtz_data
from app.qtum import qtum_data
from app.tron import tron_data
from app.mkr import mkr_data
from app.btt import btt_data
from app.vet import vet_data
from app.cro import cro_data
from app.xrp import xrp_data
from app.eos import eos_data
from app.dash import dash_data
from app.usdc import usdc_data
from app.ont import ont_data
from app.bat  import bat_data
from app.zcash import zcash_data
from app.btg import btc_gold_data
from app.iota import iota_data
from app.leo import unus_sed_leo_data
from app.icx import icx_data
from app.ae import ae_data
from app.btm import btm_data
from app.link import link_data
from app.zrx import zrx_data
from app.elf import elf_data
from app.rep import rep_data
from app.aoa import aoa_data
from app.cccx import cccx_data
from app.mco import mco_data
from app.cro import cro_data
from app.dai import dai_data
from app.ekt import ekt_data
from app.egt import egt_data
from app.enj import enj_data
from app.gnt import gnt_data
from app.ht import ht_data
from app.inb import inb_data
from app.kcs import kcs_data
from app.lamb import lamb_data
from app.gpl import gpl_data
from app import mongo
from app.util import serialize_doc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import SendGridAPIClient_key,Sendgrid_default_mail,BTC_balance



def first_tx_notification():
    print("first_tx_notification")
    mycursor.execute('SELECT address,type_id FROM sws_address WHERE tx_notification_preferred = "1"')
    sws_addresses = mycursor.fetchall()
    for addres in sws_addresses:
        address=addres[0]
        type_id = addres[1] 
        mycursor.execute('SELECT total_tx_calculated FROM sws_address WHERE address="'+str(address)+'"')
        current_tx = mycursor.fetchone()
        tx_count=current_tx[0]

        records = mongo.db.sws_history.find_one({"address":address})
        if records is not None:
            total_current_t = records['transactions']
            symbol = records['symbol']
            check_tx = int(len(total_current_t))
        else:
            check_tx = 0
        if tx_count is None:
            tx_count = 0
        else:
            pass
        if tx_count is not None or check_tx <= tx_count:
            print("added transactions")
                    
            if type_id == 1:
                print("ETHHHHHHHHHHHHHHHH")
                symbol = "ETH"
                currency = eth_data(address,symbol,type_id)

            if type_id == 2:
                print("BTCCCCCCCCCCCC")
                symbol = "BTC"
                currency = btc_data(address,symbol,type_id)
            
            
            if type_id == 3:
                symbol = "ZRX"
                currency = zrx_data(address,symbol,type_id)

            if type_id == 5:
                symbol = "ELF"
                currency = elf_data(address,symbol,type_id)

            if type_id == 6:
                symbol = "AE"
                currency = ae_data(address,symbol,type_id)

            if type_id == 8:
                symbol = "REP"
                currency = rep_data(address,symbol,type_id)

            if type_id == 9:
                symbol = "AOA"
                currency = aoa_data(address,symbol,type_id)

            if type_id == 10:
                symbol = "BAT"
                currency = bat_data(address,symbol,type_id)

            if type_id == 11:
                symbol = "BNB"
                currency = bnb_data(address,symbol,type_id)

            if type_id == 12:
                symbol = "BCH"
                currency = btc_cash_data(address,symbol,type_id)

            if type_id == 14:
                symbol = "BTG"
                currency = btc_gold_data(address,symbol,type_id)

            if type_id == 15:
                symbol = "BSV"
                currency = bitcoin_svs_data(address,symbol,type_id)

            if type_id == 17:
                symbol = "BTT"
                currency = btt_data(address,symbol,type_id)

            if symbol == 19:
                symbol = "BTM"     
                currency = btm_data(address,symbol,type_id)

            if type_id == 21:
                symbol = "LINK"
                currency = link_data(address,symbol,type_id)

            if type_id == 22:
                symbol = "CCCX"
                currency = cccx_data(address,symbol,type_id)

            if type_id == 24:
                symbol = "MCO"
                currency = mco_data(address,symbol,type_id)

            if type_id == 25:
                symbol = "CRO"
                currency = cro_data(address,symbol,type_id)

            if type_id == 26:
                symbol = "DAI"
                currency = dai_data(address,symbol,type_id)

            if type_id == 27:
                symbol = "DASH"
                currency = dash_data(address,symbol,type_id)

            if type_id == 31:
                symbol = "EKT"
                currency = ekt_data(address,symbol,type_id)

            if type_id == 32:
                symbol = "EGT"
                currency = egt_data(address,symbol,type_id)

            if type_id == 34:
                symbol = "ENJ"
                currency = enj_data(address,symbol,type_id)

            if type_id == 35:
                symbol = "EOS"  
                currency = eos_data(address,symbol,type_id)

            if type_id == 38:
                symbol = "GNT"
                currency = gnt_data(address,symbol,type_id)

            if type_id == 42:
                symbol = "HT"
                currency = ht_data(address,symbol,type_id)

            if type_id == 44:
                symbol = "ICX"
                currency = icx_data(address,symbol,type_id)

            if type_id == 45:
                symbol = "INB" 
                currency = inb_data(address,symbol,type_id)

            if type_id == 47:
                symbol = "IOTA"
                currency = iota_data(address,symbol,type_id)

            if type_id == 50:
                symbol = "KCS"
                currency = kcs_data(address,symbol,type_id)
            

            if type_id == 51:
                symbol = "LAMB"
                currency = lamb_data(address,symbol,type_id)
            

            if type_id == 53:
                symbol = "LTC"
                currency = ltc_data(address,symbol,type_id)
            

            if type_id == 55:
                symbol = "MKR"
                currency = mkr_data(address,symbol,type_id)
                

            if type_id == 67:
                symbol = "ONT"
                currency = ont_data(address,symbol,type_id)
            

            if type_id == 70:
                symbol = "QTUM"
                currency = qtum_data(address,symbol,type_id)
                

            if type_id == 75:
                symbol = "XRP"
                currency = xrp_data(address,symbol,type_id)
            

            if type_id == 83:
                symbol = "USDC" 
                currency = usdc_data(address,symbol,type_id)
        

            if type_id == 84:
                symbol = "XTZ"
                currency = xtz_data(address,symbol,type_id)


            if type_id == 87:
                symbol = "TRON"
                currency = tron_data(address,symbol,type_id)
            

            if type_id == 89:
                symbol = "LEO"
                currency = unus_sed_leo_data(address,symbol,type_id)
        

            if type_id == 91:
                symbol = "VET"
                currency = vet_data(address,symbol,type_id)
        

            if type_id == 98:
                symbol = "ZEC"
                currency = zcash_data(address,symbol,type_id)
        
        
            if type_id == 101:
                symbol = "GPL"
                currency = gpl_data(address,symbol,type_id)

        else:
            pass      

        docs = mongo.db.sws_history.find_one({"address":address})
        print(address)
        total_current_tx = docs['transactions']
        if tx_count is None or int(len(total_current_tx)) > tx_count:
            mycursor.execute('UPDATE sws_address SET total_tx_calculated ="'+str(total_current_tx)+'"  WHERE address = "'+str(address)+'"')
            mycursor.execute('SELECT u.email FROM db_safename.sws_address as a left join db_safename.sws_user as u on a.cms_login_name = u.username where a.address="'+str(address)+'"')
            email = mycursor.fetchone()
            email_id=email[0]
            if email_id is not None:
                message = Mail(
                    from_email=Sendgrid_default_mail,
                    to_emails="rasealex000000@gmail.com",
                    subject='SafeName - New Transaction Notification In Your Account',
                    html_content= '<h3> You got a new transaction on your ' + symbol + ' address </h3><strong>Address:</strong> ' + str(address) +'')
                sg = SendGridAPIClient(SendGridAPIClient_key)
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)
            else:
                pass
        else:
            pass

'''




