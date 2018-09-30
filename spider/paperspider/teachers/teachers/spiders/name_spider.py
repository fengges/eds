# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import XmlResponse
import re
from spider.paperspider.teachers.teachers.dbutils import dbs
from spider.paperspider.teachers.teachers.items import *
from urllib import parse as pa


class NameSpider(scrapy.Spider):
    name = 'namespider'
    allowed_domains = []
    start_urls = ["http://www.manmankan.com/dy2013/mingxing/%s/" % i for i in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]]

    def parse(self, response):

        name_list = self.get_name(response.css(".i_cont "))

        the_file = open("name.txt", 'a', encoding='utf-8')
        the_file.write('\n'.join(name_list))
        the_file.close()

        categery = re.findall(r'mingxing/([A-Z])/', response.url)[0]
        next_url = response.css("a.next::attr(href)").extract_first("")

        count = 0
        if next_url != "":
            count = int(re.findall(r'index_(.*?)\.shtml', next_url)[0])
        response_url = ["http://www.manmankan.com/dy2013/mingxing/%s/index_%s.shtml" % (categery, str(i)) for i in range(2, count+1)]

        for url in response_url:
            yield scrapy.Request(url, callback=self.parse_next_page)

    def parse_next_page(self, response):
        name_list = self.get_name(response.css(".i_cont "))

        the_file = open("name.txt", 'a', encoding='utf-8')
        the_file.write('\n'.join(name_list))
        the_file.close()

        pass

    def get_name(self, node):
        name_list = node.css("a::attr(title)").extract()
        return name_list



