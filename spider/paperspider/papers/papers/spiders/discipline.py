# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse as pa
from spider.paperspider.papers.papers.items import *


class JournalSpider(scrapy.Spider):
    name = 'discipline'
    start_urls = [
        "http://www.gaokao.com/z2015/zdxk/"
        ]

    def parse(self, response):
        request_url_list = response.css(".cdcy tr>td[width='19%'] p a::attr(href)").extract()
        print(len(request_url_list))
        for request_url in request_url_list:
            url = pa.urljoin(response.url, request_url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        # yield scrapy.Request(url="http://www.cdgdc.edu.cn/xwyyjsjyxx/xwbl/zdjs/zdxk/zdxkmd/lsx/266612.shtml", callback=self.parse_detail)
        pass

    def parse_detail(self, response):
        h2 = response.css("h2[style='text-align: center'] span::text").extract_first("")
        if not h2 == "国家重点学科名单":
            return
        tr_list = response.css("div.cdcy > table > tr > td:nth-child(3) > div > div:nth-child(4) > table tr")
        if not tr_list:
            return

        school_list = list()
        for i in range(1, len(tr_list)):
            school = tr_list[i].css("td[valign='top'] span::text").extract_first("")
            school_list.append(school)

        flag = 0
        for school in school_list:
            if school == "" or re.findall(r'[0-9]+', school):
                flag = 1
        if flag == 1:
            print("===url=== %s" % response.url)
            return
        num_list = []
        n_list = response.css("div.cdcy > table >tr > td:nth-child(3) > div > div:nth-child(4) > table tr td[style*='background-color: #e3f0f6']")
        for n in n_list:
            num = n.css("::attr(rowspan)").extract_first("")
            if num != "":
                num_list.append(int(num))
            else:
                num_list.append(1)

        discipline_node = response.css("div.cdcy > table >tr > td:nth-child(3) > div > div:nth-child(4) > table tr td[style*='background-color: #e3f0f6']")

        discipline_list = []
        for i in range(0, len(discipline_node)):
            spans = discipline_node[i].css("span::text").extract()
            code = spans[0]
            name = spans[1]
            for time in range(0, num_list[i]):
                discipline_list.append((code, name))

        insert_list = list()
        for i in range(0, len(school_list)):
            insert_list.append((school_list[i], discipline_list[i][1], discipline_list[i][0]))
        print(len(insert_list))
        print(insert_list)


