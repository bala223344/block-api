import scrapy
from .. items import BlockScraperItem


#----------Class for scraping ETH wallets and cloud addresses----------

class EthSpider(scrapy.Spider):
    name = "eth_whitelist"
    custom_settings = {
        'ITEM_PIPELINES': {
            'block_scraper.pipelines.BlockScraperPipeline': 300
        }
    }

    def start_requests(self):
        urls = [
            'https://etherscan.io/labelcloud',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
       # items = BlockScraperItem()
        a=response.css(".dropdown-toggle > span::text").extract()
        for b in a:
            b = b.strip()
            url1='https://etherscan.io/accounts/label/'+b+""
            url_correct= url1.replace(" ","-")
            yield scrapy.Request(url=url_correct, callback=self.parse_deep)

    def parse_deep(self, response):
        items = BlockScraperItem()
        c = response.css("td a::text").extract()
        d = response.css("td:nth-child(2)::text").extract()
        #e = response.css("td:nth-child(3)::text").extract()
        #f = response.css("td:nth-child(4)::text").extract()
        if len(c)==len(d):
            b = len(c)
            for s in range(0,b):
                address = response.css("td a::text")[s].extract()
                tag_name = response.css("td:nth-child(2)::text")[s].extract()
                Tx_count = response.css("td:nth-child(4)::text")[s].extract()
                coin = "ETH"
                url_coming_from = response.url

                items['address']=address
                items['tag_name']=tag_name
                items['Tx_count']=Tx_count
                items['coin']=coin
                items['type_id']='1'
                items['url_coming_from']=url_coming_from
                items['address_risk_score']=50
                yield items
        else:
            print("Tags not equal")
