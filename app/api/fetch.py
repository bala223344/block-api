import requests
from flask import (
    Blueprint,request,jsonify,abort
)
from datetime import datetime
from app.util import serialize_doc


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

    if type_id == "27":
        currency = dash_data(address,symbol,type_id)
        return currency

    if type_id == "98":
        currency = zcash_data(address,symbol,type_id)
        return currency
 
    if type_id == "55":
        currency = mkr_data(address,symbol,type_id)
        return currency

    if type_id == "21":
        currency = link_data(address,symbol,type_id)
        return currency

#-------ERC20 coin-----------

    if type_id == "3":
        currency = zrx_data(address,symbol,type_id)
        return currency

    if type_id == "5":
        currency = elf_data(address,symbol,type_id)
        return currency

    if type_id == "8":
        currency = rep_data(address,symbol,type_id)
        return currency

    if type_id == "9":
        currency = aoa_data(address,symbol,type_id)
        return currency

    if type_id == "10":
        currency = bat_data(address,symbol,type_id)
        return currency

    if type_id == "22":
        currency = cccx_data(address,symbol,type_id)
        return currency

    if type_id == "24":
        currency = mco_data(address,symbol,type_id)
        return currency

    if type_id == "25":
        currency = cro_data(address,symbol,type_id)
        return currency

    if type_id == "26":
        currency = dai_data(address,symbol,type_id)
        return currency

    if type_id == "31":
        currency = ekt_data(address,symbol,type_id)
        return currency

    if type_id == "32":
        currency = egt_data(address,symbol,type_id)
        return currency

    if type_id == "34":
        currency = enj_data(address,symbol,type_id)
        return currency

    if type_id == "38":
        currency = gnt_data(address,symbol,type_id)
        return currency

    if type_id == "42":
        currency = ht_data(address,symbol,type_id)
        return currency

    if type_id == "45":
        currency = inb_data(address,symbol,type_id)
        return currency


    if type_id == "50":
        currency = kcs_data(address,symbol,type_id)
        return currency


    if type_id == "51":
        currency = lamb_data(address,symbol,type_id)
        return currency

    if type_id == "35":  
        currency = eos_data(address,symbol,type_id)
        return currency
    


#-------ERC20 coin-----------


    if type_id == "53":
        currency = ltc_data(address,symbol,type_id)
        return currency

    if type_id == "12":
        currency = btc_cash_data(address,symbol,type_id)
        return currency

    if type_id == "11":
        currency = bnb_data(address,symbol,type_id)
        return currency

    if type_id == "15":
        currency = bitcoin_svs_data(address,symbol,type_id)
        return currency

    '''
    if symbol == "USDT":#Not working properly
        currency = tether_data(address,symbol,type_id)
        return currency
    '''
    
    if type_id == "87":
        currency = tron_data(address,symbol,type_id)
        return currency

    if type_id == "89":
        currency = unus_sed_leo_data(address,symbol,type_id)
        return currency

    if type_id == "47":
        currency = iota_data(address,symbol,type_id)
        return currency

    if type_id == "67":
        currency = ont_data(address,symbol,type_id)
        return currency

    if type_id == "84":
        currency = xtz_data(address,symbol,type_id)
        return currency

    if type_id == "14":
        currency = btc_gold_data(address,symbol,type_id)
        return currency

    if type_id == "70":
        currency = qtum_data(address,symbol,type_id)
        return currency

    if type_id == "91":
        currency = vet_data(address,symbol,type_id)
        return currency

    if type_id == "25":
        currency = cro_data(address,symbol,type_id)
        return currency

    if type_id == "10":
        currency = bat_data(address,symbol,type_id)
        return currency

    if type_id == "83":
        currency = usdc_data(address,symbol,type_id)
        return currency

    if type_id == "17":
        currency = btt_data(address,symbol,type_id)
        return currency

    if type_id == "75":
        currency = xrp_data(address,symbol,type_id)
        return currency
    
    if type_id == "44":
        currency = icx_data(address,symbol,type_id)
        return currency
    
    '''
    if type_id == "41":
        currency = erc_coin_data(address,symbol,type_id)
        return currency


    if type_id == "46":
        currency = erc_coin_data(address,symbol,type_id)
        return currency
    '''

    if type_id == "6":
        currency = ae_data(address,symbol,type_id)
        return currency

    if symbol == "19":     #Not done completely
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
    return jsonify(docs),200




