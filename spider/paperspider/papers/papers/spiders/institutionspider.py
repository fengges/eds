# -*- coding: utf-8 -*-
import scrapy
import os
import re
from spider.paperspider.papers.papers.services.paperservices import paper_service
from spider.paperspider.papers.papers.spiders.super_spider import SuperSpider
from spider.paperspider.papers.papers.items import *

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class InstitutionSpider(SuperSpider):
    name = 'institutionspider'
    allowed_domains = []
    start_urls = ['http://xueshu.baidu.com/']

    def parse(self, response):
        search_list = self.get_search_list()
        for s in search_list:
            paper = UpdateInstitutionItem()
            paper["_id"] = s["_id"]
            paper["author"] = s["author"]
            request_url = s["url"]
            yield scrapy.Request(url=request_url,
                                 meta={"paper": paper},
                                 callback=self.parse_institution)

    # 解析百度学术论文详情页, 获取作者与机构
    def parse_institution(self, response):
        paper = response.meta.get("paper")
        paper_author_list = response.css(".author_wr .author_text a")
        author = super().get_author_org(paper_author_list)
        l = re.findall(r'"org":"(.*?)"', author)
        l = [i for i in l if i != '']
        if paper["author"] != author and len(l) > 0:
            paper["author"] = author
            yield paper
        try:
            paper_service.update_paper_search_list(paper["_id"])
            pass
        except Exception as e:
            print(e)
            print("更新searched错误……")

    def get_search_list(self):
        search_list = paper_service.institution_search_list_from_paper()

        return search_list
