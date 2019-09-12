from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app.balance_util import ETH_balance,BTC_balance,ERC_balance,LTC_balance,BCH_balance,BNB_balance,BSV_balance,TRX_balance,LEO_balance,MIOTA_balance,ZEC_balance,ONT_balance,XTZ_balance,BTG_balance,XRP_balance,USDT_balance,EOS_balance,DASH_balance,XLM_balance,MKR_balance,LINK_balance

bp = Blueprint('balance', __name__, url_prefix='/')
from app import mongo


#---------Api only for balance for speed optimization direct hit apis end points---------

@bp.route("/transaction/balance",methods=['POST'])
def balance():
    if not request.json:
        abort(500)
    address=request.json.get("address", None)    
    cointype=request.json.get("cointype", None)
    type_id=request.json.get("type_id",None)
    if type_id == "1":
        balance = ETH_balance(address,cointype,type_id)
        return balance
    
    if type_id == "2":
        balance = BTC_balance(address,cointype,type_id) 
        return balance
    
    if type_id == "3":
        balance = ERC_balance(address,cointype,type_id)
        return balance
    
    if type_id == "53":
        balance = LTC_balance(address,cointype,type_id)
        return balance

    if type_id == "11":
        balance = BNB_balance(address,cointype,type_id)
        return balance

    if type_id == "12":
        balance = BCH_balance(address,cointype,type_id)
        return balance
    
    if type_id == "15":
        balance = BSV_balance(address,cointype,type_id)
        return balance

    if type_id == "87":
        balance = TRX_balance(address,cointype,type_id)
        return balance
    
    if type_id == "89":
        balance = LEO_balance(address,cointype,type_id)
        return balance
        
    if type_id == "47":
        balance = MIOTA_balance(address,cointype,type_id)
        return balance

    if type_id == "98":
        balance = ZEC_balance(address,cointype,type_id)
        return balance

    if type_id == "67":
        balance = ONT_balance(address,cointype,type_id)
        return balance
    
    if type_id == "84":
        balance = XTZ_balance(address,cointype,type_id)
        return balance
        
    if type_id == "14":
        balance = BTG_balance(address,cointype,type_id)
        return balance

    if type_id == "75":
        balance = XRP_balance(address,cointype,type_id)
        return balance

    if type_id == "83":
        balance = USDT_balance(address,cointype,type_id)
        return balance


    if type_id == "35":
        balance = EOS_balance(address,cointype,type_id)
        return balance

    if type_id == "27":
        balance = DASH_balance(address,cointype,type_id)
        return balance

    if type_id == "82":
        balance = XLM_balance(address,cointype,type_id)
        return balance

    if type_id == "55":
        balance = MKR_balance(address,cointype,type_id)
        return balance

    if type_id == "21":
        balance = LINK_balance(address,cointype,type_id)
        return balance



    '''
    if type_id == "4":
        balance = ABBC_balance(address,cointype,type_id)
        return balance
    
    if type_id == "5":
        balance = ELF_balance(address,cointype,type_id)
        return balance

    if type_id == "6":
        balance = AE_balance(address,cointype,type_id)
        return balance

    if type_id == "7":
        balance = ARDR_balance(address,cointype,type_id)
        return balance

    if type_id == "8":
        balance = REP_balance(address,cointype,type_id)
        return balance

    if type_id == "9":
        balance = AOA_balance(address,cointype,type_id)
        return balance

    if type_id == "10":
        balance = BAT_balance(address,cointype,type_id)
        return balance

    if type_id == "13":
        balance = BCD_balance(address,cointype,type_id)
        return balance


    if type_id == "15":
        balance = BSV_balance(address,cointype,type_id)
        return balance

    if type_id == "16":
        balance = BTS_balance(address,cointype,type_id)
        return balance

    if type_id == "17":
        balance = BTT_balance(address,cointype,type_id)
        return balance

    if type_id == "18":
        balance = BCN_balance(address,cointype,type_id)
        return balance

    if type_id == "19":
        balance = BTM_balance(address,cointype,type_id)
        return balance

    if type_id == "20":
        balance = ADA_balance(address,cointype,type_id)
        return balance

    if type_id == "21":
        balance = LINK_balance(address,cointype,type_id)
        return balance

    if type_id == "22":
        balance = CCCX_balance(address,cointype,type_id)
        return balance

    if type_id == "23":
        balance = ATOM_balance(address,cointype,type_id)
        return balance

    if type_id == "24":
        balance = MCO_balance(address,cointype,type_id)
        return balance

    if type_id == "25":
        balance = CRO_balance(address,cointype,type_id)
        return balance

    if type_id == "26":
        balance = DAI_balance(address,cointype,type_id)
        return balance

    if type_id == "27":
        balance = DASH_balance(address,cointype,type_id)
        return balance

    if type_id == "28":
        balance = DCR_balance(address,cointype,type_id)
        return balance

    if type_id == "29":
        balance = DGB_balance(address,cointype,type_id)
        return balance

    if type_id == "30":
        balance = DOGE_balance(address,cointype,type_id)
        return balance

    if type_id == "31":
        balance = EKT_balance(address,cointype,type_id)
        return balance

    if type_id == "32":
        balance = EGT_balance(address,cointype,type_id)
        return balance

    if type_id == "33":
        balance = NRG_balance(address,cointype,type_id)
        return balance

    if type_id == "34":
        balance = ENJ_balance(address,cointype,type_id)
        return balance

    if type_id == "35":
        balance = EOS_balance(address,cointype,type_id)
        return balance

    if type_id == "36":
        balance = ETC_balance(address,cointype,type_id)
        return balance

    if type_id == "37":
        balance = FXC_balance(address,cointype,type_id)
        return balance

    if type_id == "38":
        balance = GNT_balance(address,cointype,type_id)
        return balance

    if type_id == "39":
        balance = GXC_balance(address,cointype,type_id)
        return balance

    if type_id == "40":
        balance = HEDG_balance(address,cointype,type_id)
        return balance

    if type_id == "41":
        balance = HOT_balance(address,cointype,type_id)
        return balance

    if type_id == "42":
        balance = HT_balance(address,cointype,type_id)
        return balance
    '''
