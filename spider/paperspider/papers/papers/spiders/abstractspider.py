# -*- coding: utf-8 -*-
import scrapy
import os
import re
import time
from spider.paperspider.papers.papers.services.paperservices import paper_service
from spider.paperspider.papers.papers.spiders.super_spider import SuperSpider
from spider.paperspider.papers.papers.items import *

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

school_dict = eval(open(root + "\\dicts\\school2en_dict.txt", "r", encoding='utf8').read())
ins_dict = eval(open(root + "\\dicts\\institution2en_dict.txt", "r", encoding='utf8').read())

reREG = r'\r|\t|\v|\n|\\n|\\r'
reSPACE = r' '
reCOMM = r'<!--.*?-->'


class AbstractSpider(SuperSpider):
    name = 'abstractspider'
    allowed_domains = []
    start_urls = ['http://xueshu.baidu.com/']

    def parse(self, response):
        search_list = paper_service.get_search_list_from_paper(0, 100)
        for s in search_list:
            paper = UpdateAbstractItem()
            paper["_id"] = s["_id"]
            paper["name"] = s["name"]
            paper["abstract"] = ""
            paper["keyword"] = s["keyword"]
            request_url = s["url"]
            yield scrapy.Request(url=request_url,
                                 meta={"paper": paper},
                                 callback=self.paser_detail)
            pass
        pass

    # 解析百度学术论文详情页
    def paser_detail(self, response):
        paper = response.meta.get("paper")

        # 详情页面可解析 出版源：org、作者：author、摘要：abstract
        # 摘要可能不全
        # 作者姓名可能是英文

        data_sign = self.my_strip(response.css(".abstract ::text").extract_first(""))
        sc_url_group = re.search(r'sc_vurl=(.*?)&', response.css(".source a::attr(href)").extract_first(""))
        sc_url = sc_url_group.group(1) if sc_url_group is not None else ""
        if data_sign != "" and sc_url != "":
            t = int(time.time() * 1000)
            request_url = "http://xueshu.baidu.com/usercenter/data/schinfo?url=%s&callback=jQuery1102016936626670962984_%s&sign=%s&_=%s" % (sc_url, t, data_sign, t + 1)
            yield scrapy.Request(url=request_url,
                                 meta={"paper": paper},
                                 callback=self.parse_abstract)
        pass
