from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo
#----------Import balance Apis End points from Config file----------

from app.config import ETH_url,BTC_url,ERC_url,LTC_url,BCH_url,BNB_url,BSV_url,TRX_url,LEO_url,MIOTA_url,ZEC_url,ONT_url,BTG_url,XTZ_url


#----------Function for return ETH balance----------

def ETH_balance(address,cointype,type_id):
    ret=ETH_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return BTC balance----------

def BTC_balance(address,cointype,type_id):
    ret=BTC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()   
    balance =transaction['balance']
    dat=(int(balance)/100000000)
    ret=("{:f}".format(float(dat)))
    return str(ret)   


#----------Function for return ERC_coins balance----------

def ERC_balance(address,cointype,type_id):
    ret=ERC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    return str(int(balance)/1000000000000000000)


#----------Function for return LTC balance----------

def LTC_balance(address,cointype,type_id):
    ret=LTC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    data = response['data']
    balance = data['balance']
    return str(balance)


#----------Function for return BCH balance----------

def BCH_balance(address,cointype,type_id):
    ret=BCH_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    data = response['data']
    addr =data[''+address+'']
    add =addr['address']
    balance =add['balance']
    bal = (balance/100000000)
    return str(bal)


#----------Function for return BNB balance----------

def BNB_balance(address,cointype,type_id):
    ret=BNB_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    reslt = response['balance']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset']
            if asset_name == "BNB":
                balance = ress['free']
                ba = ("{:f}".format(float(balance)))
                return str(ba)   


#----------Function for return BSV balance----------

def BSV_balance(address,cointype,type_id):
    ret=BSV_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    respon = response_user_token.json()  
    response = respon['data']
    balance = response['balance']
    dat = ("{:f}".format(float(balance)))
    return str(dat)


#----------Function for return TRX balance----------

def TRX_balance(address,cointype,type_id):
    ret=TRX_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    balance = response['balance']
    ret=float(balance/1000000)
    dat = ("{:f}".format(float(ret)))
    return str(dat)


#----------Function for return LEO balance----------

def LEO_balance(address,cointype,type_id):
    ret=LEO_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    dat=("{:f}".format(float(ret)))
    return str(dat)


#----------Function for return MIOTA balance----------

def MIOTA_balance(address,cointype,type_id):
    ret=MIOTA_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()      
    balance = response['balance']
    ball =int(balance)/1000000000000000
    bal=float("{0:.2f}".format(ball))
    return str(bal)


#----------Function for return ZEC balance----------

def ZEC_balance(address,cointype,type_id):
    ret=ZEC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    return str(balance)


#----------Function for return ONT balance----------

def ONT_balance(address,cointype,type_id):
    ret=ONT_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    reslt = response['result']
    for ress in reslt:    
        if ress:
            asset_name=ress['asset_name']
            if asset_name == "ont":
                balance = ress['balance']
                ret=("{:f}".format(float(balance)))
                return str(ret)


#----------Function for return XTZ balance----------

def XTZ_balance(address,cointype,type_id):
    ret=XTZ_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json() 
    balance=response['balance']
    return str(balance)


#----------Function for return BTG balance----------

def BTG_balance(address,cointype,type_id):
    ret=BTG_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    return str(balance)
    