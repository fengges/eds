# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import XmlResponse
import re
from spider.paperspider.teachers.teachers.dbutils import dbs
from spider.paperspider.teachers.teachers.items import *


class KaoyanbangSpider(scrapy.Spider):
    name = 'schoollogo'
    allowed_domains = []
    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        sql = "select * from school_info"
        school_list = dbs.getDics(sql)
        for school in school_list:
            url = school["logo"]
            if url:
                yield scrapy.Request(url=url, meta={"id": school["id"]}, callback=self.parse_info)

    def parse_info(self, response):
        id_ = response.meta.get("id", "0")
        try:
            fq = open("E:\\shixi\\img\\%s.jpg" % id_, 'wb')
            fq.write(response.body)
            fq.close()
        except Exception as e:
            print(id_)
            print(e)
        pass


