import scrapy
from .. items import BlockScraperItem

class BtcSpider(scrapy.Spider):
    name = "btc_99coins"

    def start_requests(self):
        urls = [
            'https://99bitcoins.com/bitcoin/rich-list/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        items = BlockScraperItem()
        print(response.url)
        a=response.css(".t99btc-rl-address .external::text").extract()
        b = len(a)
        for s in range(0,b):
            address = response.css(".t99btc-rl-address .external::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            yield items     
