import scrapy
from .. items import BlockScraperItem


class EthSpider(scrapy.Spider):
    name = "eth_whitelist"

    def start_requests(self):
        urls = [
            'https://etherscan.io/accounts/?ps=100',
        ]
        for url in urls:
            for count in range(1,100):
                next_url = 'https://etherscan.io/accounts/'+str(count)+'?ps=100'
                yield scrapy.Request(url=next_url, callback=self.parse)
            
    
    def parse(self, response):
        items = BlockScraperItem()
        a=response.css(".table-hover a::text").extract()
        b = len(a)
        for s in range(0,b):
            address = response.css(".table-hover a::text")[s].extract()
            coin = "ETH"
            url_coming_from = response.url
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            yield items     


