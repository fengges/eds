# -*- coding: utf-8 -*-
import scrapy
from urllib import parse as pa
from spider.paperspider.papers.papers.items import *


class JournalSpider(scrapy.Spider):
    name = 'zazhi'
    start_urls = ["https://www.zazhi.com.cn/qikan/s0l0l0l0l0l0l0l0l0l00%s.html" % str(i) for i in range(1, 387)]

    def parse(self, response):

        nodes = response.css("div.body-con-2-1-l > div.body-list-1 li.list-li")

        for i in range(0, len(nodes)):
            item = JournalItem()
            item["ISSN"] = nodes[i].css(".list-c li.list-param-item:nth-child(5)::text").extract_first("")
            item["IF"] = ""
            item["ave_if"] = nodes[i].css(".list-c li.list-param-item:nth-child(12)::text").extract_first("")
            item["cn_name"] = nodes[i].css(".list-c .title h4 ::text").extract_first("")
            item["en_name"] = ""
            item["former_name"] = ""
            item["countryOrRegion"] = nodes[i].css(".list-c li.list-param-item:nth-child(4) a::text").extract_first("")
            item["discipline_subject"] = "-".join(nodes[i].css(".list-c li.list-param-item:nth-child(3) a::text").extract())
            item["self_cited_rate"] = ""
            item["url"] = nodes[i].css(".list-c .title a::attr(href)").extract_first("")
            if item["url"] != "" and item["ave_if"] != "":
                item["url"] = pa.urljoin(response.url, item["url"])
                yield scrapy.Request(url=item["url"], meta={"item": item}, callback=self.parse_detail)
            elif item["IF"] != "" and item["en_name"] != "" and item["ave_if"] != "":
                # print(item)
                yield item

    def parse_detail(self, response):
        item = response.meta.get("item")
        item["IF"] = response.css('div.qk-buy > ul > li:nth-child(3) span::text').extract_first("")
        # print(item)
        yield item
