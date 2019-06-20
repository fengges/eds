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
    pic_url = scrapy.Field()
    pass


class ImgItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    homepage = scrapy.Field()
    pass


class TeacherListItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    school = scrapy.Field()
    ins = scrapy.Field()
    homepage = scrapy.Field()
    pass


class BaikeItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    baike = scrapy.Field()
    pass


class SamplesItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    rank = scrapy.Field()
    t_title = scrapy.Field()
    c_abstract = scrapy.Field()
    detail = scrapy.Field()
    search_id = scrapy.Field()
    pass
