# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FeedpriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # total = scrapy.Field()
    id = scrapy.Field()
    date = scrapy.Field()
    corn_tc = scrapy.Field()
    corn_k = scrapy.Field()
    soy_c = scrapy.Field()
    soy_b = scrapy.Field()
    cornFlour_b = scrapy.Field()
    soyFlour = scrapy.Field()