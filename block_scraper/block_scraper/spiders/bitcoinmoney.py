import scrapy
from .. items import BlockScraperItem

class BitcoinmoneySpider(scrapy.Spider):
    name = "bitcoinmoney"

    def start_requests(self):
        urls = [
            'https://bitcoinmoneynews.com/top100',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        items = BlockScraperItem()
        print(response.url)
        a=response.css(".txio-address::text").extract()
        b = len(a)
        for s in range(0,b):
            address = response.css(".txio-address::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            yield items     
