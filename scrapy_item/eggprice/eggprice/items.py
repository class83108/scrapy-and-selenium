# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EggpriceItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    date = scrapy.Field()
    meat_ab2 = scrapy.Field()
    meat_l2 = scrapy.Field()
    meat_south = scrapy.Field()
    egg = scrapy.Field()

