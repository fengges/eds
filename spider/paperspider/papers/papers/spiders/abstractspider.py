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

        search_list = self.get_search_list()
        print(len(search_list))

        for s in search_list:
            paper = UpdateAbstractItem()
            paper["_id"] = s["_id"]
            paper["name"] = s["name"]
            paper["url"] = s["url"]
            paper["abstract"] = s["abstract"]
            paper["org"] = s["org"]
            paper["source_url"] = s["source_url"]
            paper["keyword"] = s["keyword"]
            if paper["source_url"] == "":
                yield scrapy.Request(url=paper["url"],
                                     meta={"paper": paper},
                                     callback=self.paser_detail)
            else:
                t = int(time.time() * 1000)
                request_url = "http://xueshu.baidu.com/usercenter/data/schinfo?url=%s&callback=jQuery1102016936626670962984_%s&sign=lkji&_=%s" % (paper["source_url"], t, t + 1)
                yield scrapy.Request(url=request_url,
                                     meta={"paper": paper},
                                     callback=super().parse_abstract)
            pass
        pass

    # 解析百度学术论文详情页
    def paser_detail(self, response):
        # 详情页面可解析 出版源：org、摘要：abstract
        # 摘要可能不全
        # 作者姓名可能是英文

        paper = response.meta.get("paper")
        paper["org"] = super().my_strip(response.css(".publish_text a::text").extract_first(""))

        sc_url_group = re.search(r'sc_vurl=(.*?)&', response.css(".source a::attr(href)").extract_first(""))
        sc_url = sc_url_group.group(1) if sc_url_group is not None else ""
        if sc_url != "":
            t = int(time.time() * 1000)
            request_url = "http://xueshu.baidu.com/usercenter/data/schinfo?url=%s&callback=jQuery1102016936626670962984_%s&sign=lkji&_=%s" % (sc_url, t, t + 1)
            paper["source_url"] = sc_url
            yield scrapy.Request(url=request_url,
                                 meta={"paper": paper},
                                 callback=super().parse_abstract)
        pass

    def get_search_list(self):
        search_list = paper_service.abstract_search_list_select()
        return search_list
