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
    pass
