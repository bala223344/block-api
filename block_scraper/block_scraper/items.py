# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlockScraperItem(scrapy.Item):
    address = scrapy.Field()
    coin = scrapy.Field()
    url_coming_from = scrapy.Field()
    tag_name = scrapy.Field()
    Tx_count = scrapy.Field()
    type_id = scrapy.Field()
    address_risk_score = scrapy.Field()
    pass


class HeistScraperItem(scrapy.Item):
    print("asdasdasfdasfsdfdsfdsfdfdsfdsfdasfad")
    address = scrapy.Field()
    coin = scrapy.Field()
    url_coming_from = scrapy.Field()
    tag_name = scrapy.Field()
    subcategory = scrapy.Field()
    status = scrapy.Field()
    description = scrapy.Field()
    also_known_as = scrapy.Field()
    pass
