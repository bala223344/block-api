import scrapy
from .. items import HeistScraperItem

class QuotesSpider(scrapy.Spider):
    name = "btc_heistlist"
    custom_settings = {
        'ITEM_PIPELINES': {
            'block_scraper.pipelines.HeistBlockPipeline': 300
        }
    }

    def start_requests(self):
        urls = [
            'https://www.blockchain.com/btc/address/14BN8Qj43zebrSo58J8BxGoPFBHtw9t6Y2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
   
    
    def parse(self, response):
        items = HeistScraperItem()
        a=response.css("#tx_container .stack-mobile > a::text").extract()
        b = len(a)
        
        for s in range(0,b):
            address = response.css("#tx_container .stack-mobile > a::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            items['subcategory']='NA'
            items['tag_name']='NA'
            items['status']='Active'
            items['description']='NA'
            items['also_known_as']='NA'
            yield items     


