# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import XmlResponse
import re
from spider.paperspider.teachers.teachers.dbutils import dbs
from spider.paperspider.teachers.teachers.items import *


class KaoyanbangSpider(scrapy.Spider):
    name = 'teacherimage'
    allowed_domains = []
    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        sql = "select * from teacher where id >= 40146"
        info_list = dbs.getDics(sql)
        print(len(info_list))
        for info in info_list:
            teacher = ImgItem()
            teacher["id"] = info["id"]
            teacher["name"] = info["name"]
            teacher["homepage"] = info["homepage"]
            request_url = info["homepage"]
            try:
                yield scrapy.Request(url=request_url, meta={"teacher": teacher}, callback=self.parse_info)
            except:
                fw = open("id.txt", "a+", encoding="utf-8")
                fw.write("%s" % info["id"])
                fw.close()

    def parse_info(self, response):
        img_list = response.css("img::attr(src)").extract()
        if img_list:
            img_list = ["-link-" + i for i in img_list]
            teacher = response.meta.get("teacher", None)
            teacher["image"] = "".join(img_list)
            print(teacher)
            yield teacher

