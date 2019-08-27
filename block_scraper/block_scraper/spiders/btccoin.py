import scrapy
from .. items import BlockScraperItem


#----------Class for scraping btc popular addresses----------

class Btccom(scrapy.Spider):
    name = "btc_com"
    custom_settings = {
        'ITEM_PIPELINES': {
            'block_scraper.pipelines.BlockScraperPipeline': 300
        }
    }

    def start_requests(self):
        urls = [
            'https://steemit.com/bitcoin/@advexon/top-100-richest-bitcoin-address',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        items = BlockScraperItem()
        a=response.css(".Markdown a::text").extract()
        print(a)
        
        b = len(a)
        for s in range(0,b):
            address = response.css(".Markdown a::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            items['tag_name']='NA'
            items['Tx_count']='NA'
            items['type_id']='2'
            items['address_risk_score']=0
            yield items     
        