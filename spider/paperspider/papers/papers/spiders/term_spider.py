# -*- coding: utf-8 -*-
import scrapy
import os
import time
from spider.paperspider.papers.papers.items import *

from spider.paperspider.papers.papers.services.term_service import term_service

class PSSZhuanliSpider(scrapy.Spider):
    name = 'term_spider'
    allowed_domains = []
    start_urls = ['http://www.termonline.cn/index.htm']

    def parse(self, response):
        info_list = term_service.get_search_list(('0812', 'doc'))

        for info in info_list:
            text = info["abstract"]
            cookie_dict = dict()
            cookie_dict["CNZZDATA1259716300"] = "1048795864-1540193641-%7C1540256990"
            cookie_dict["UM_distinctid"] = "1669afce4ade6-0f994e473e6fb1-5c10301c-1fa400-1669afce4af4f1"
            cookie_dict["JSESSIONID"] = "77C7BCC7CD5C98520D7671C20A970BA5"

            data_dict = dict()
            data_dict['content'] = text
            data_dict['single'] = 'Y'

            yield scrapy.FormRequest(url='http://www.termonline.cn/extract.jhtm',
                                     formdata=data_dict,
                                     cookies=cookie_dict,
                                     callback=self.parse_detail,
                                     meta={"id": info["id"]})

    def parse_detail(self, response):
        id = response.meta.get("id")
        data = eval(response.body, {'true': 0, 'false': 1})
        result = data.get('result', [])
        if not result:
            return
        term_list = []
        for item in result:
            k = item.get("k", "")
            datas = item.get("datas", [])
            info_list = []
            for d in datas:
                cn = d.get("cn", "")
                en = d.get("en", "")
                discipline = d.get("subject_name_l1", "")

                di = dict()
                di["cn"] = cn
                di["en"] = en
                di["discipline"] = discipline
                info_list.append(di)

            term_dict = dict()
            term_dict["k"] = k
            term_dict["datas"] = info_list

            term_list.append(term_dict)

        item = TermItem()
        item["id"] = id
        item["term"] = str(term_list)

        print(id)

        yield item
