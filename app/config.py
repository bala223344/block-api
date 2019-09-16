import mysql.connector
#----------Database MongoUri-----------

MongoUri="mongodb+srv://xmage:xmage@cluster0-xooqb.mongodb.net/crypto_app?retryWrites=true"


#----------MySql connection----------

#mydb = mysql.connector.connect(host='198.38.93.150',user='dexter',password='cafe@wales1',database='db_safename',auth_plugin='mysql_native_password')
#mydb = mysql.connector.connect(user="VsaqpBhCxL" , password="sW9BgYhqmG", host="remotemysql.com", database="VsaqpBhCxL")
mydb = mysql.connector.connect(user="dexter" , password="cafe@wales1", host="localhost", port='3306', database="db_safename")
mycursor=mydb.cursor()




#-------Urls which are using in Schedulers---------

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
DASH_url="https://dashradar.com/insight-api/addr/{{address}}?from=0&to=1000"
XLM_url = "https://horizon.stellar.org/accounts/{{address}}"
MKR_url = "https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LINK_url = "https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"







#---------Api endpoint for tx_history and notification apis----------

symbol="ETH"
ETH_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ETH_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
 

symbol="BTC"
BTC_balance="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start=1&limit=100"


symbol="DASH"
DASH_balance="https://dashradar.com/insight-api/addr/{{address}}?from=0&to=1000"
DASH_transactions="https://dashradar.com/insight-api/txs?address={{address}}&pageNum=0"


symbol="ZEC"
ZEC_balance="https://api.zcha.in/v2/mainnet/accounts/{{address}}"
ZEC_transactions="https://api.zcha.in/v2/mainnet/accounts/{{address}}/sent?limit=5&offset=0&sort=timestamp&direction=descending"


symbol="BCH"
BCH_balance="https://api.blockchair.com/bitcoin-cash/dashboards/address/{{address}}?limit=10,0"
BCH_transactions="https://api.blockchair.com/bitcoin-cash/dashboards/transactions/{{address}}"


symbol="MKR"
MKR_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
MKR_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


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


symbol="ZRX"
ZRX_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ZRX_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ELF"
ELF_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ELF_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="BAT"
BAT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BAT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="MCO"
MCO_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
MCO_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="REP"
REP_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
REP_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="AOA"
AOA_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
AOA_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="BTM"
BTM_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BTM_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="LINK"
LINK_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LINK_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="CRO"
CRO_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
CRO_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="EKT"
EKT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
EKT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="EGT"
EGT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
EGT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ENJ"
ENJ_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
ENJ_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="GNT"
GNT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
GNT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="HOT"
HOT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
HOT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="HT"
HT_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
HT_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="INB"
INB_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
INB_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="IOST"
IOST_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
IOST_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="KCS"
KCS_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
KCS_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="LAMB"
LAMB_balance="https://api.etherscan.io/api?module=account&action=balance&address={{address}}&tag=latest&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
LAMB_transactions="http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"


symbol="ICX"
ICX_balance="https://tracker.icon.foundation/v3/address/info?address={{address}}"
ICX_transactions="https://tracker.icon.foundation/v3/address/txList?address={{address}}&page=1&count=10"



symbol="AE"
AE_balance="https://roma-net.mdw.aepps.com/v2/accounts/{{address}}"
AE_transactions="https://roma-net.mdw.aepps.com/middleware/transactions/account/{{address}}?limit=10&page=1"



symbol="BTM"
BTM_balance="https://blockmeta.com/api/v2/address-assets"
BTM_transactions="https://blockmeta.com/api/v2/address-asset-transactions"
