
#----Urls which are using in Schedulers---------

ETH_SCAM_URL = "https://etherscamdb.info/api/scams"
ETH_TRANSACTION_URL = "http://api.etherscan.io/api?module=account&action=txlist&address={{address}}&startblock=0&endblock=99999999&sort=asc&apikey=V9GBE7D675BBBSR7D8VEYGZE5DTQBD9RMJ"
BTC_TRANSACTION_URL = "https://blockchain.coinmarketcap.com/api/addresses?address={{address}}&symbol={{symbol}}&start=1&limit=50"
BTC_TRANSACTION="https://blockchain.coinmarketcap.com/api/address?address={{address}}&symbol=BTC&start=1&limit=100"


#---------Schedulers running timings-------------

heist_addresses_fetch_scheduler_minute=18
heist_addresses_fetch_scheduler_seconds=55


heist_associated_fetch_scheduler_minute=18
heist_associated_fetch_scheduler_seconds=59


riskscore_by_tx_two_yearold_scheduler_minute=19
riskscore_by_tx_two_yearold_scheduler_seconds=00


risk_score_by_safename_scheduler_minute=19
risk_score_by_safename_scheduler_seconds=2


risk_score_by_heist_scheduler_minute=19
risk_score_by_heist_scheduler_seconds=15


tx_notification_scheduler_minute=20

risk_score_update_scheduler_minute=16
risk_score_update_scheduler_seconds=1

profile_risk_score_scheduler_minute=17
profile_risk_score_scheduler_seconds=43


#------Apis keys------

SendGridAPIClient_key='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'
Sendgrid_default_mail='notifications@safename.io'