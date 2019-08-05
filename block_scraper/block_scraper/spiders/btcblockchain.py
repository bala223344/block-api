import scrapy
from .. items import BlockScraperItem

class BtcblockchainSpider(scrapy.Spider):
    name = "btcblockchain"

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
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            yield items     
