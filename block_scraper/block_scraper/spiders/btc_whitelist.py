import scrapy
from .. items import BlockScraperItem


class QuotesSpider(scrapy.Spider):
    name = "btc_whitelist"

    def start_requests(self):
        urls = [
            'https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html',
        ]
        for url in urls:
            for count in range(1,100):
                if count == 1:
                    next_url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html'
                    yield scrapy.Request(url=next_url, callback=self.parse)
                else:
                    next_url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-'+str(count)+'.html'
                    yield scrapy.Request(url=next_url, callback=self.parse)
   
    
    def parse(self, response):
        items = BlockScraperItem()
        a=response.css("td > a::text").extract()
        b = len(a)
        for s in range(0,b):
            address = response.css("td > a::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            yield items     


