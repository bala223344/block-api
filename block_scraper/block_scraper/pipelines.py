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
        


    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='remotemysql.com',
            user='VsaqpBhCxL',
            password='sW9BgYhqmG',
            database='VsaqpBhCxL'
        )
        self.curr = self.conn.cursor()

    def create_table(self): 
        self.curr.execute("""CREATE TABLE IF NOT EXISTS `sws_known_address` ( id INT,address text, coin text, also_known_as text,category_tags text,source text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        a=item['address']
        b=item['coin']
        c=item['url_coming_from']
        self.curr.execute('SELECT * FROM sws_known_address WHERE address="'+str(a)+'"')
        check = self.curr.fetchall()
        if not check:
            self.curr.execute('''SELECT MAX(id) FROM sws_known_address''')
            maxid = self.curr.fetchone()
            check=maxid[0]
            if check is None:
                ids = 1
            else:
                ids=(maxid[0]+1)
            self.curr.execute('INSERT INTO sws_known_address (id,coin,address,also_known_as,category_tags,source) VALUES ("'+str(ids)+'","'+str(b)+'","'+str(a)+'","'+str(c)+'","pool","'+str(c)+'")')
            self.conn.commit()
        else:
            print("already_exist")
        
        

        
    
    
