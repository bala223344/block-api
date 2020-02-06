# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#import sqlite3
import mysql.connector



class BlockScraperPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()
    
#----------Function of sql connection----------  
    
    '''
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',#remotemysql.com
            user='root',#VsaqpBhCxL
            password='',#sW9BgYhqmG
            database='db_safename'#VsaqpBhCxL
        )
        self.curr = self.conn.cursor()
    '''
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='198.38.93.150',#remotemysql.com
            user='dexter',#VsaqpBhCxL
            password='cafe@wales1',#sW9BgYhqmG
            database='db_safename',#VsaqpBhCxL
            auth_plugin='mysql_native_password'
        )
        self.curr = self.conn.cursor()
    
    
#----------Function of create table if already not exists----------

    def create_table(self): 
        #self.curr.execute("""CREATE TABLE IF NOT EXISTS `sws_known_address` (address_id INT,address varchar(1000),type_id varchar(50),address_risk_score INT, coin varchar(100),tag_name varchar(1000),source varchar(1000),tx_count varchar(1000))""")


#----------Function which calling a function for store data----------

    def process_item(self, item, spider):
        self.store_db(item)
        return item


#----------Function for store data in database----------

    def store_db(self,item):
        address=item['address']
        coin=item['coin']
        url_coming_from=item['url_coming_from']
        tag_name=item['tag_name']
        Tx_count=item['Tx_count']
        type_id=item['type_id']
        address_risk_score=item['address_risk_score']
        self.curr.execute('SELECT * FROM sws_known_address WHERE address="'+str(address)+'"')
        check = self.curr.fetchall()
        if not check:
            self.curr.execute('''SELECT MAX(address_id) FROM sws_known_address''')
            maxid = self.curr.fetchone()
            check=maxid[0]
            if check is None:
                ids = 1
            else:
                ids=(maxid[0]+1)
            self.curr.execute('INSERT INTO sws_known_address(address_id,coin,address,type_id,address_risk_score,tag_name,source,tx_count) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(address)+'","'+str(type_id)+'","'+str(address_risk_score)+'","'+str(tag_name)+'","'+str(url_coming_from)+'","'+str(Tx_count)+'")')
            self.conn.commit()
        else:
            print("already_exist")


#----------Another class for heist addresses pipeline----------  

class HeistBlockPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
    

#----------Function of sql connection----------
    '''
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='remotemysql.com',#remotemysql.com
            user='VsaqpBhCxL',#VsaqpBhCxL
            password='sW9BgYhqmG',#sW9BgYhqmG
            database='VsaqpBhCxL'#VsaqpBhCxL
        )
        self.curr = self.conn.cursor()
    '''
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='198.38.93.150',#remotemysql.com
            user='cguser',#VsaqpBhCxL
            password='cafe@wales1',#sW9BgYhqmG
            database='db_safename',#VsaqpBhCxL
            auth_plugin='mysql_native_password'
        )
        self.curr = self.conn.cursor()
    

#----------Function of create table if already not exists----------

    def create_table(self): 
       # self.curr.execute("""CREATE TABLE IF NOT EXISTS `sws_heist_address` ( id INT,coin varchar(100),tag_name varchar(100),status varchar(100),address varchar(100),source varchar(1000),subcategory varchar(100),description varchar(1500),also_known_as varchar(1000))""")


#----------Function which calling a function for store data----------

    def process_item(self, item, spider):
        self.store_db(item)
        return item


#----------Function for store data in database----------

    def store_db(self,item):
        address=item['address']
        coin=item['coin']
        url_coming_from=item['url_coming_from']
        tag_name=item['tag_name']
        subcategory=item['subcategory']
        status=item['status']
        description=item['description']
        also_known_as=item['also_known_as']
        self.curr.execute('SELECT * FROM sws_known_address WHERE address="'+str(address)+'"')
        check = self.curr.fetchall()
        if not check:
            self.curr.execute('''SELECT MAX(id) FROM sws_known_address''')
            maxid = self.curr.fetchone()
            check=maxid[0]
            if check is None:
                ids = 1
            else:
                ids=(maxid[0]+1)
            self.curr.execute('INSERT INTO sws_heist_address (id,coin,tag_name,status,address,source,subcategory,description,also_known_as) VALUES ("'+str(ids)+'","'+str(coin)+'","'+str(tag_name)+'","'+str(status)+'","'+str(address)+'","'+str(url_coming_from)+'","'+str(subcategory)+'","'+str(description)+'","'+str(also_known_as)+'")')
            self.conn.commit()
        else:
            print("already_exist")

    
    
