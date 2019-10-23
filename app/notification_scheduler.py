from app.config import mydb,mycursor
from app.eth_notification import eth_notification
from app.btc_notification import btc_notification
from app.xrp_notification import xrp_notification
from app.bch_notification import bch_notification
from app.ltc_notification import ltc_notification
from app.eos_notification import eos_notification
from app.bnb_notification import bnb_notification
from app.bsv_notification import bsv_notification



#----------Function for new transaction notification----------

def tx_notification():
    print("tx_notification_running")
    mycursor.execute('SELECT address,type_id FROM sws_address WHERE tx_notification_preferred = "1"')
    sws_addresses = mycursor.fetchall()
    for addres in sws_addresses:
        address=addres[0]
        type_id = addres[1] 
        
        if type_id == 1:
            symbol = 'ETH'
            currency = eth_notification(address,symbol,type_id)        
        
        if type_id == 2:
            symbol = 'BTC'
            currency = btc_notification(address,symbol,type_id)
        
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