import scrapy
from .. items import BlockScraperItem


#----------Class for scraping btc popular addresses----------

class BtcblockchainSpider(scrapy.Spider):
    name = "btcblockchain"
    custom_settings = {
        'ITEM_PIPELINES': {
            'block_scraper.pipelines.BlockScraperPipeline': 300
        }
    }
    
    def start_requests(self):
        urls = [
            'https://www.blockchain.com/btc/popular-addresses',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        items = BlockScraperItem()
        print(response.url)
        a=response.css(".mobile-wrap > a::text").extract()
        b = len(a)
        for s in range(0,b):
            address = response.css(".mobile-wrap > a::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            
            items['address']=address
            items['tag_name']='NA'
            items['Tx_count']='NA'
            items['coin']=coin
            items['type_id']='2'
            items['url_coming_from']=url_coming_from
            items['address_risk_score']=0
            yield items     
