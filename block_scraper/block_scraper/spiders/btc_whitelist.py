import scrapy
from .. items import BlockScraperItem


#----------Class for scraping btc popular 100000 addresses----------

class QuotesSpider(scrapy.Spider):
    name = "btc_whitelist"
    custom_settings = {
        'ITEM_PIPELINES': {
            'block_scraper.pipelines.BlockScraperPipeline': 300
        }
    }

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
        #data = []
        for s in range(0,b):
            v = s+1 
            address = response.css("td > a::text")[s].extract()
            coin = "BTC"
            url_coming_from = response.url
            Tx_count = "NA"
            tag_name = response.css("#tblOne tr:nth-child("+str(v)+") small a::text").get()
            
            items['address']=address
            items['coin']=coin
            items['url_coming_from']=url_coming_from
            items['Tx_count']=Tx_count
            items['tag_name']=tag_name
            items['type_id']='2'
            items['address_risk_score']=50
            yield items     


