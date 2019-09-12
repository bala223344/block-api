from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import Sendgrid_default_mail,SendGridAPIClient_key

#-----Calling functions at the call of Transaction Api------

from app.btc import btc_data
from app.eth import eth_data
from app.bnb import bnb_data
from app.bitcoin_cash import btc_cash_data
from app.bitcoin_SV import bitcoin_svs_data
from app.litecoin import ltc_data
from app.tether import tether_data
from app.xtz import xtz_data
from app.qtum import qtum_data
from app.tron import tron_data
from app.mkr import mkr_data
from app.btt import btt_data
from app.vet import vet_data
from app.cro import cro_data
from app.xrp import xrp_data
from app.erc_coins import erc_coin_data
from app.eos import eos_data
from app.dash import dash_data
from app.usdc import usdc_data
from app.ont import ont_data
from app.bat  import bat_data
from app.zcash import zcash_data
from app.btcgold import btc_gold_data
from app.iota import iota_data
from app.unus_s_leo import unus_sed_leo_data
from app.icx import icx_data
from app.ae import ae_data
from app.btm import btm_data

bp = Blueprint('fetch', __name__, url_prefix='/')
from app import mongo

    
#------Main Api which is using a function for return details by post address and symbol------

@bp.route("/transaction",methods=["POST"])
def main():
    if not request.json:
        abort(500)
    address=request.json.get("address", None)    
    symbol=request.json.get("symbol", None)
    type_id=request.json.get("type_id","")

    if type_id == "2":
        currency = btc_data(address,symbol,type_id)
        return currency

    if type_id == "1":
        currency = eth_data(address,symbol,type_id)
        return currency

    if symbol == "LTC":
        currency = ltc_data(address,symbol,type_id)
        return currency

    if symbol == "BCH":
        currency = btc_cash_data(address,symbol,type_id)
        return currency

    if symbol == "BNB":
        currency = bnb_data(address,symbol,type_id)
        return currency

    if symbol == "BSV":
        currency = bitcoin_svs_data(address,symbol,type_id)
        return currency

    if symbol == "USDT":#Not working properly
        currency = tether_data(address,symbol,type_id)
        return currency

    if symbol == "TRON":
        currency = tron_data(address,symbol,type_id)
        return currency

    if symbol == "UNUS_SED_LEO":
        currency = unus_sed_leo_data(address,symbol,type_id)
        return currency

    if symbol == "IOTA":
        currency = iota_data(address,symbol,type_id)
        return currency

    if symbol == "Z_CASH":
        currency = zcash_data(address,symbol,type_id)
        return currency
    
    if symbol == "ONT":
        currency = ont_data(address,symbol,type_id)
        return currency

    if symbol == "XTZ":
        currency = xtz_data(address,symbol,type_id)
        return currency

    if symbol == "BTC_GOLD":
        currency = btc_gold_data(address,symbol,type_id)
        return currency

    if symbol == "QTUM":
        currency = qtum_data(address,symbol,type_id)
        return currency

    if symbol == "MKR":
        currency = mkr_data(address,symbol,type_id)
        return currency

    if symbol == "VET":
        currency = vet_data(address,symbol,type_id)
        return currency

    if symbol == "CRO":
        currency = cro_data(address,symbol,type_id)
        return currency

    if symbol == "BAT":
        currency = bat_data(address,symbol,type_id)
        return currency

    if symbol == "USDC":
        currency = usdc_data(address,symbol,type_id)
        return currency

    if symbol == "BTT":
        currency = btt_data(address,symbol,type_id)
        return currency

    if symbol == "XRP":
        currency = xrp_data(address,symbol,type_id)
        return currency

    if symbol == "DASH":
        currency = dash_data(address,symbol,type_id)
        return currency

    if symbol == "EOS":  
        currency = eos_data(address,symbol,type_id)
        return currency
    
    if symbol == "ZRX":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "ELF":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "REP":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "AOA":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "BAT":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "LINK":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "CCCX":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "MCO":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "CRO":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "DAI":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "EKT":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "EGT":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "ENJ":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "GNT":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "HT":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "ICX":
        currency = icx_data(address,symbol,type_id)
        return currency

    if symbol == "INB":
        currency = erc_coin_data(address,symbol,type_id)
        return currency
    
    if symbol == "KCS":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "LAMB":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "HOT":
        currency = erc_coin_data(address,symbol,type_id)
        return currency

    if symbol == "IOST":
        currency = erc_coin_data(address,symbol,type_id)
        return currency
    
    if symbol == "AE":
        currency = ae_data(address,symbol,type_id)
        return currency

    if symbol == "BTM":     #Not done completely
        currency = btm_data(address,symbol,type_id)
        return currency

#Not done for XMR,BTM,THerether

#-----Api for return currency symbols and urls--------

@bp.route("/currency_symbol",methods=['GET'])
def currency_symbol():
    urls = mongo.db.symbol_url.find({})
    urls = [serialize_doc(doc) for doc in urls]
    return jsonify(urls), 200



#-----Api for return tx_history and balance by address--------

@bp.route("/local_transaction/<string:address>",methods=['GET'])
def local_transaction(address):
    docs = mongo.db.sws_history.find({"address":address})
    docs = [serialize_doc(doc) for doc in docs]
    return jsonify(docs), 200




