from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo
from app.config import ETH_url,BTC_url,ERC_url,LTC_url,BCH_url,BNB_url,BSV_url,TRX_url,LEO_url,MIOTA_url,ZEC_url,ONT_url


def ETH_balance(address,cointype,type_id):
    ret=ETH_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)

def BTC_balance(address,cointype,type_id):
    ret=BTC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    transaction = response_user_token.json()   
    balance =transaction['balance']
    dat=(int(balance)/100000000)
    ret=("{:f}".format(float(dat)))
    return str(ret)   

def ERC_balance(address,cointype,type_id):
    ret=ERC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    return str(int(balance)/1000000000000000000)

def LTC_balance(address,cointype,type_id):
    ret=LTC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    data = response['data']
    balance = data['balance']
    return str(balance)

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

def BSV_balance(address,cointype,type_id):
    ret=BSV_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    respon = response_user_token.json()  
    response = respon['data']
    balance = response['balance']
    dat = ("{:f}".format(float(balance)))
    return str(dat)

def TRX_balance(address,cointype,type_id):
    ret=TRX_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    balance = response['balance']
    ret=float(balance/1000000)
    dat = ("{:f}".format(float(ret)))
    return str(dat)

def LEO_balance(address,cointype,type_id):
    ret=LEO_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    dat=("{:f}".format(float(ret)))
    return str(dat)

def MIOTA_balance(address,cointype,type_id):
    ret=MIOTA_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()      
    balance = response['balance']
    ball =int(balance)/1000000000000000
    bal=float("{0:.2f}".format(ball))
    return str(bal)

def ZEC_balance(address,cointype,type_id):
    ret=ZEC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    return str(balance)

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