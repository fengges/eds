# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeachersItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    info = scrapy.Field()
    html = scrapy.Field()
    pass


class ImgItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    homepage = scrapy.Field()
    pass
