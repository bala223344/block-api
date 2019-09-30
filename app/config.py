#import mysql.connector
import pymysql
#----------Database MongoUri-----------

MongoUri="mongodb+srv://xmage:xmage@cluster0-xooqb.mongodb.net/crypto_app?retryWrites=true"


#----------MySql connection----------
#,auth_plugin='mysql_native_password'
mydb = pymysql.connect(host='198.38.93.150',user='dexter',password='cafe@wales1',database='db_safename')
#mydb = pymysql.connect(user="VsaqpBhCxL" , password="sW9BgYhqmG", host="remotemysql.com", database="VsaqpBhCxL")
#mydb = pymysql.connect(user="dexter" , password="cafe@wales1", host='localhost', port=3306, database="db_safename")
mycursor=mydb.cursor()



#-------Urls which are using in Schedulers--------

ETH_SCAM_URL = "https://etherscamdb.info/api/scams"
ETH_TRANSACTION_URL = "http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BTC_TRANSACTION_URL = "https://blockchain.coinmarketcap.com/api/addresses?address={{address}}&symbol={{symbol}}&start=1&limit=50"
BTC_TRANSACTION="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start=1&limit=100"




#---------Schedulers running timings-------------


heist_addresses_fetch_scheduler_minute=17
heist_addresses_fetch_scheduler_seconds=51


heist_associated_fetch_scheduler_minute=12
heist_associated_fetch_scheduler_seconds=58


riskscore_by_tx_two_yearold_scheduler_minute=16
riskscore_by_tx_two_yearold_scheduler_seconds=23


risk_score_by_safename_scheduler_minute=17
risk_score_by_safename_scheduler_seconds=4


risk_score_by_heist_scheduler_minute=17
risk_score_by_heist_scheduler_seconds=21


tx_notification_scheduler_minute=20

risk_score_update_scheduler_minute=13
risk_score_update_scheduler_seconds=21

profile_risk_score_scheduler_minute=13
profile_risk_score_scheduler_seconds=57


#------Apis keys------

SendGridAPIClient_key='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'
Sendgrid_default_mail='notifications@safename.io'


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




#---------Urls for balance saprate apis----------

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
XRP_url="https://api.xrpscan.com/api/v1/account/{{address}}" 
USDT_url="https://api.omniexplorer.info/v1/address/addr/details/"
EOS_url="https://eos.greymass.com/v1/chain/get_account"
DASH_url="https://api.blockchair.com/dash/dashboards/address/{{address}}?limit=10,0"
XLM_url = "https://horizon.stellar.org/accounts/{{address}}"
MKR_url = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LINK_url ="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x514910771af9ca656af840dff83e8264ecf986ca&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"





#---------Api endpoint for tx_history and notification apis----------

symbol="ETH"
ETH_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ETH_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
 
'''
symbol="BTC"
BTC_balance="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start=1&limit=100"
'''

symbol="BTC"
BTC_balance="https://api.blockchair.com/bitcoin/dashboards/address/{{address}}?limit=10,0" 
BTC_transactions="https://api.blockchair.com/bitcoin/dashboards/transactions/{{address}}"


symbol="DASH"
DASH_balance="https://api.blockchair.com/dash/dashboards/address/{{address}}?limit=10,0"
DASH_transactions="https://api.blockchair.com/dash/dashboards/transactions/{{address}}"


symbol="ZEC"
ZEC_balance="https://api.zcha.in/v2/mainnet/accounts/{{address}}"
ZEC_transactions="https://api.zcha.in/v2/mainnet/accounts/{{address}}/sent?limit=5&offset=0&sort=timestamp&direction=descending"


symbol="BCH"
BCH_balance="https://api.blockchair.com/bitcoin-cash/dashboards/address/{{address}}?limit=10,0"
BCH_transactions="https://api.blockchair.com/bitcoin-cash/dashboards/transactions/{{address}}"


symbol="MKR"
MKR_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
MKR_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
#"http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
#http://api.etherscan.io/api?module=account&action=tokentx&address=0x260c25f991171850f4c589eb9d8af11568d20c30&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ


symbol="LINK"
LINK_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x514910771af9ca656af840dff83e8264ecf986ca&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LINK_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ELF"
ELF_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xbf2179859fc6D5BEE9Bf9158632Dc51678a4100e&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ELF_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ZRX"
ZRX_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xe41d2489571d322189246dafa5ebde1f4699f498&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ZRX_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="DAI"
DAI_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
DAI_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="BAT"
BAT_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x0d8775f648430679a709e98d2b0cb6250d2887ef&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BAT_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"

symbol="CCCX"
CCCX_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x378903a03fb2c3ac76bb52773e3ce11340377a32&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
CCCX_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="MCO"
MCO_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xb63b606ac810a52cca15e44bb630fd42d8d1d83d&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
MCO_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="REP"
REP_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xe94327d07fc17907b4db788e5adf2ed424addff6&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
REP_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="AOA"
AOA_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x9ab165d795019b6d8b3e971dda91071421305e5a&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
AOA_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="XRP"
XRP_balance="https://api.xrpscan.com/api/v1/account/{{address}}"
XRP_transactions="https://api.xrpscan.com/api/v1/account/{{address}}/transactions"


symbol="LTC"
LTC_balance="https://explorer.viabtc.com/res/ltc/addresses/{{address}}"
LTC_transactions="https://explorer.viabtc.com/res/ltc/transactions/address?address={{address}}&page=1&limit=50"


symbol="USDT"
USDT_balance="https://api.omniexplorer.info/v1/address/addr/details/"
USDT_transactions="https://api.xrpscan.com/api/v1/account/{{address}}/transactions"


symbol="BNB"
BNB_balance="https://explorer.binance.org/api/v1/balances/{{address}}"
BNB_transactions="https://explorer.binance.org/api/v1/txs?page=1&rows=25&address={{address}}"


symbol="BSV"
BSV_balance="https://explorer.viabtc.com/res/bsv/addresses/{{address}}"
BSV_transactions="https://explorer.viabtc.com/res/bsv/transactions/address?address={{address}}&page=1&limit=50"


symbol="TRON"
TRON_balance="https://apilist.tronscan.org/api/account?address={{address}}"
TRON_transactions="https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start=0&total=0&start_timestamp=1529865000000&end_timestamp=1561787527899&address={{address}}"


symbol="UNUS_SED_LEO"
UNUS_SED_LEO_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
UNUS_SED_LEO_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="IOTA"
IOTA_balance="https://api.thetangle.org/addresses/{{address}}"



symbol="ONT"
ONT_balance="https://explorer.ont.io/v2/addresses/{{address}}/native/balances"
ONT_transactions="https://explorer.ont.io/v2/addresses/{{address}}/transactions?page_size=20&page_number=1"


symbol="BTC_GOLD"
BTC_GOLD_balance="https://explorer.bitcoingold.org/insight-api/addr/{{address}}/?noTxList=1"
BTC_GOLD_transactions="https://explorer.bitcoingold.org/insight-api/txs?address={{address}}&pageNum=0"


symbol="XTZ"
XTZ_balance="https://api2.tzscan.io/v1/node_account/{{address}}"
XTZ_transactions="https://api2.tzscan.io/v1/operations/{{address}}?type=Transaction&p=0&number=20"


symbol="EOS"
EOS_balance="https://eos.greymass.com/v1/chain/get_account"
EOS_transactions="https://eos.greymass.com/v1/history/get_actions"


symbol="QTUM"
QTUM_balance="https://qtum.info/api/address/{{address}}"
QTUM_transactions="https://qtum.info/api/address/{{address}}/txs?page=0&pageSize=20"
url_hash = "https://qtum.info/api/txs/{{hash}}"


symbol="BTM"
BTM_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BTM_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="CRO"
CRO_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
CRO_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="EKT"
EKT_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xbab165df9455aa0f2aed1f2565520b91ddadb4c8&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
EKT_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="EGT"
EGT_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x8e1b448ec7adfc7fa35fc2e885678bd323176e34&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
EGT_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ENJ"
ENJ_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xf0ee6b27b759c9893ce4f094b49ad28fd15a23e4&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ENJ_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="GNT"
GNT_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xa74476443119a942de498590fe1f2454d7d4ac0d&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
GNT_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="HOT"
HOT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
HOT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="HT"
HT_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x6f259637dcd74c767781e37bc6133cd6a68aa161&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
HT_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="INB"
INB_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x17aa18a4b64a55abed7fa543f2ba4e91f2dce482&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
INB_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="IOST"
IOST_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
IOST_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="KCS"
KCS_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x039b5649a59967e3e936d7471f9c3700100ee1ab&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
KCS_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="LAMB"
LAMB_balance="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x8971f9fd7196e5cee2c1032b50f656855af7dd26&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LAMB_transactions="http://api.etherscan.io/api?module=account&action=tokentx&address={{address}}&startblock=0&endblock=999999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ICX"
ICX_balance="https://tracker.icon.foundation/v3/address/info?address={{address}}"
ICX_transactions="https://tracker.icon.foundation/v3/address/txList?address={{address}}&page=1&count=10"


symbol="AE"
AE_balance="https://roma-net.mdw.aepps.com/v2/accounts/{{address}}"
AE_transactions="https://roma-net.mdw.aepps.com/middleware/transactions/account/{{address}}?limit=10&page=1"


symbol="BTM"
BTM_balance="https://blockmeta.com/api/v2/address-assets"
BTM_transactions="https://blockmeta.com/api/v2/address-asset-transactions"


symbol == "BTT"
BTT_balance = "https://apilist.tronscan.org/api/account?address={{address}}"
BTT_transactions = "https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=20&start=0&address={{address}}"


symbol == "VET":
VET_balance="https://explore.veforge.com/api/accounts/{{address}}"
VET_transactions="https://explore.veforge.com/api/transactions?address={{address}}&count=10&offset=0"