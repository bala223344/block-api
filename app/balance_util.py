import requests



#----------Import balance Apis End points from Config file----------

from app.config import ETH_url,GPL_url,HT_url,GNT_url,ENJ_url,BTC_url,ERC_url,LTC_url,BCH_url,BNB_url,BSV_url,TRX_url,LEO_url,MIOTA_url,ZEC_url,ONT_url,BTG_url,XTZ_url,XRP_url,USDT_url,EOS_url,DASH_url,XLM_url,MKR_url,ELF_url,AE_url,REP_url,aoa_url,BAT_url,BSV_url,BTT_url,BTM_url,LINK_url,CCCX_url,MCO_url,CRO_url,ZRX_url,DAI_url,EKT_url,EGT_url,MATIC_url




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


#----------Function for return ETH balance----------

def ZRX_balance(address,cointype,type_id):
    ret=ZRX_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return ELF balance----------

def ELF_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=ELF_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return AE balance----------

def AE_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=AE_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return REP balance----------

def REP_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=REP_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return AOA_balance----------

def AOA_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=aoa_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return BAT_balance----------

def BAT_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=BAT_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


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


#----------Function for return BTG balance----------

def BTG_balance(address,cointype,type_id):
    ret=BTG_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    return str(balance)


#----------Function for return BSV balance----------

def BSV_balance(address,cointype,type_id):
    ret=BSV_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    respon = response_user_token.json()  
    response = respon['data']
    balance = response['balance']
    dat = ("{:f}".format(float(balance)))
    return str(dat)


#----------Function for return BTT_balance----------

def BTT_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=BTT_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    return str(balance)


#----------Function for return BTM_balance----------

def BTM_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=BTM_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return LINK balance----------

def LINK_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=LINK_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return CCCX_balance----------

def CCCX_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=CCCX_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



#----------Function for return MCO_balance----------

def MCO_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=MCO_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



#----------Function for return CRO_balance----------

def CRO_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=CRO_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return DAI_balance----------

def DAI_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=DAI_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return DASH balance----------

def DASH_balance(address,cointype,type_id):
    ret=DASH_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json() 
    data = response['data']
    addr =data[''+address+'']
    add =addr['address']
    balance =add['balance']
    bal = (balance/100000000)
    return str(bal)


#----------Function for return EKT_balance----------

def EKT_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=EKT_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



#----------Function for return EGT_balance----------

def EGT_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=EGT_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



#----------Function for return ENJ_balance----------

def ENJ_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=ENJ_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



#----------Function for return EOS balance----------

def EOS_balance(address,cointype,type_id):
    acouunt={"account_name":address}
    response_user_token = requests.post(url=EOS_url,json=acouunt)
    response = response_user_token.json()       
    balance=response['core_liquid_balance']
    print(balance)
    return str(balance)



#----------Function for return GNT_balance----------

def GNT_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=GNT_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return HT_balance----------

def HT_balance(address,cointype,type_id):
    print("linkeeeeeeee")
    ret=HT_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return MIOTA balance----------

def MIOTA_balance(address,cointype,type_id):
    ret=MIOTA_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()      
    balance = response['balance']
    ball =int(balance)/1000000000000000
    bal=float("{0:.2f}".format(ball))
    return str(bal)


#----------Function for return LTC balance----------

def LTC_balance(address,cointype,type_id):
    ret=LTC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    data = response['data']
    balance = data['balance']
    return str(balance)


#----------Function for return MKR balance----------

def MKR_balance(address,cointype,type_id):
    ret=MKR_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



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


#----------Function for return XRP balance----------

def XRP_balance(address,cointype,type_id):
    ret=XRP_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance=response['initial_balance']
    return str(balance)


#----------Function for return XLM balance----------

def XLM_balance(address,cointype,type_id):
    print("running XLM")
    ret=XLM_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json() 
    balance=response['balances']
    xlm_balance=balance[0]
    response = xlm_balance['balance']
    return str(response)


#----------Function for return USDT balance----------

def USDT_balance(address,cointype,type_id):
    print("running")
    print(USDT_url)
    response_user_token = requests.post(USDT_url ,data={"account_name":address})
    response = response_user_token.json()          
    print(response)
    balances = response['balance']
    return str(balances)


#----------Function for return XTZ balance----------

def XTZ_balance(address,cointype,type_id):
    ret=XTZ_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json() 
    balance=response['balance']
    return str(balance)


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


#----------Function for return ZEC balance----------

def ZEC_balance(address,cointype,type_id):
    ret=ZEC_url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['balance']
    return str(balance)


#----------Function for return GPL balance----------

def GPL_balance(address,cointype,type_id):
    ret=GPL_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)



#----------Function for return MATIC balance-----------

def MATIC_balance(address,cointype,type_id):
    ret=MATIC_url.replace("{{address}}",''+address+'')
    print(ret)
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    balance = response['result']
    ret=(int(balance)/1000000000000000000)
    return str(ret)


#----------Function for return XMR balance----------

def XMR_balance(address,cointype,type_id):
    return ("N/A")












    




















