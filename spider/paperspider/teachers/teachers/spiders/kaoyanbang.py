# -*- coding: utf-8 -*-
import scrapy
import os
import re
import json
from spider.paperspider.teachers.teachers.dbutils import dbs
from spider.paperspider.teachers.teachers.items import *


class KaoyanbangSpider(scrapy.Spider):
    name = 'kaoyanbang'
    allowed_domains = []
    start_urls = ['http://www.kaoyan.com/']

    def parse(self, response):
        sql = "select * from teacherdata_info where id >= 118849 and url like '%http://yz.kaoyan.com/%'"
        info_list = dbs.getDics(sql)
        print(len(info_list))
        for info in info_list:
            teacher = TeachersItem()
            teacher["_id"] = info["id"]
            request_url = info["url"]
            yield scrapy.Request(url=request_url, meta={"teacher": teacher}, callback=self.parse_info)

    def parse_info(self, response):
        teacher = response.meta.get("teacher", "")

        html = response.css(".articleCon").extract_first("")
        ll = response.css(".articleCon ::text").extract()
        ll = [re.sub(r'[\t|\r|\n|\a]', '', i) for i in ll if i]
        text = "\n".join(ll)
        di = dict()
        di["info"] = text
        di["html"] = html
        teacher["info"] = json.dumps(di, ensure_ascii=False)

        yield teacher
        pass

    def parse_strong(self, response):
        re_list = response.css(".articleCon strong::text").extract()
        print("\n".join(re_list))
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        fw = open(root + "\\dicts\\strong_dict.txt", "a", encoding='utf8')
        fw.write("\n".join(re_list))
        pass
