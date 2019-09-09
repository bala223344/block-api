#----------Database MongoUri-----------

MongoUri="mongodb+srv://xmage:xmage@cluster0-xooqb.mongodb.net/crypto_app?retryWrites=true"




#----Urls which are using in Schedulers---------

ETH_SCAM_URL = "https://etherscamdb.info/api/scams"
ETH_TRANSACTION_URL = "http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BTC_TRANSACTION_URL = "https://blockchain.coinmarketcap.com/api/addresses?address={{address}}&symbol={{symbol}}&start=1&limit=50"
BTC_TRANSACTION="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start=1&limit=100"


#---------Schedulers running timings-------------

heist_addresses_fetch_scheduler_minute=11
heist_addresses_fetch_scheduler_seconds=15


heist_associated_fetch_scheduler_minute=12
heist_associated_fetch_scheduler_seconds=50


riskscore_by_tx_two_yearold_scheduler_minute=14
riskscore_by_tx_two_yearold_scheduler_seconds=30


risk_score_by_safename_scheduler_minute=15
risk_score_by_safename_scheduler_seconds=35


risk_score_by_heist_scheduler_minute=16
risk_score_by_heist_scheduler_seconds=30


tx_notification_scheduler_minute=20

risk_score_update_scheduler_minute=17
risk_score_update_scheduler_seconds=30

profile_risk_score_scheduler_minute=16
profile_risk_score_scheduler_seconds=42


#------Apis keys------

SendGridAPIClient_key='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'
Sendgrid_default_mail='notifications@safename.io'



#-------My sql connection details------

host = '198.38.93.150'
user = 'dexter'
password = 'cafe@wales1'
database = 'db_safename'
auth_plugin = 'mysql_native_password'


#--------PGP verificaion template----------

 
template='''
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512 


Login
Signup
Help
Coin
Auto-detects: BTC address / ETH address / Safe Name
Pay idon
Report User
Public Profile
Need Help? (Live Chat)
{{safename}}
SAFENAME IDENTITY
KYC VERIFIED
Fair
All public and private addresses associated with this identity have no known reported risks, login to get notifications if this changes.

PAYMENTS
You can send payments to idon through the following:
{{cointype}}
{{addresses}}
REFERRALS
Whitelist for SafeName (Beta) 
Available Now
Get me a page just like this one!
KEYBASE VERIFY
Want to verify the validity of this page?
Select All content + Copy + Visit keybase.io/verify + Paste All Content into the Modal + Click Verify.
{{PGP_sign_key}}
Copyright © 2019 safename.io
'''









#---------Urls for baance saprate apis----------

ETH_url="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BTC_url="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start=1&limit=100"
ERC_url="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LTC_url="https://explorer.viabtc.com/res/ltc/addresses/{{address}}"
BCH_url="https://api.blockchair.com/bitcoin-cash/dashboards/address/{{address}}?limit=10,0"
BNB_url="https://explorer.binance.org/api/v1/balances/{{address}}"
BSV_url="https://explorer.viabtc.com/res/bsv/addresses/{{address}}"
TRX_url="https://apilist.tronscan.org/api/account?address={{address}}"
LEO_url="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
MIOTA_url="https://api.thetangle.org/addresses/{{address}}"
ZEC_url="https://api.zcha.in/v2/mainnet/accounts/{{address}}"
ONT_url="https://explorer.ont.io/v2/addresses/{{address}}/native/balances"
XTZ_url="https://api2.tzscan.io/v1/node_account/{{address}}"
BTG_url="https://explorer.bitcoingold.org/insight-api/addr/{{address}}/?noTxList=1"