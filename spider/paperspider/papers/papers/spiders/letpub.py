# -*- coding: utf-8 -*-
import scrapy
from urllib import parse as pa
from spider.paperspider.papers.papers.items import *


class JournalSpider(scrapy.Spider):
    name = 'letpub'
    start_urls = ["http://www.letpub.com.cn/index.php?page=journalapp&view=search&searchname=&searchissn=&searchfield=&searchimpactlow=&searchimpacthigh=&searchimpacttrend=&searchscitype=SCI&searchcategory1=&searchcategory2=&searchjcrkind=&searchopenaccess=&searchsort=relevance&searchsortorder=desc&currentsearchpage=%s#journallisttable" % str(i) for i in range(1, 380)]

    def parse(self, response):
        nodes = response.css("#yxyz_content > table.table_yjfx tr")
        for i in range(2, len(nodes)):
            item = JournalItem()
            item["ISSN"] = nodes[i].css("tr>td:nth-child(1)::text").extract_first("")
            item["IF"] = nodes[i].css("tr>td:nth-child(3)::text").extract_first("")
            item["ave_if"] = nodes[i].css("tr>td:nth-child(4)::text").extract_first("")
            item["cn_name"] = ""
            item["en_name"] = nodes[i].css("tr>td:nth-child(2) font::text").extract_first("")
            item["former_name"] = ""
            item["countryOrRegion"] = ""
            item["discipline_subject"] = ""
            item["self_cited_rate"] = ""
            item["url"] = nodes[i].css("tr>td:nth-child(2) a::attr(href)").extract_first("")
            if not item["url"] == "":
                item["url"] = pa.urljoin(response.url, item["url"])
                yield scrapy.Request(url=item["url"], meta={"item": item}, callback=self.parse_detail)
            elif item["IF"] != "" and item["en_name"] != "":
                yield item

    def parse_detail(self, response):
        item = response.meta.get("item")
        main_table = response.css('#yxyz_content > table:nth-child(12) > tbody')
        item["countryOrRegion"] = main_table.css('tr:nth-child(11) > td:nth-child(2)::text').extract_first("")
        item["discipline_subject"] = main_table.css('tr:nth-child(10) > td:nth-child(2)::text').extract_first("")
        item["self_cited_rate"] = main_table.css('tr:nth-child(5) > td:nth-child(2)::text').extract_first("")
        yield item
