# -*- coding: utf-8 -*-
import scrapy
from urllib import parse as pa
import re
from spider.paperspider.papers.papers.items import *


class JournalSpider(scrapy.Spider):
    name = 'acadcnki'
    start_urls = ["http://acad.cnki.net/kns55/oldNavi/n_Navi.aspx?NaviID=1&Flg="]

    def parse(self, response):
        col_list = response.css("#lblNavi .col")
        for col in col_list:
            discipline = col.css("h5 a::text").extract_first("")
            discipline = re.sub(r'\(.*?\)', '', discipline)
            nodes = col.css("ul.list li")
            for node in nodes:
                request_url = node.css("a::attr(href)").extract_first("")
                subject = node.css("a::text").extract_first("")

                yield scrapy.Request(url=pa.urljoin(response.url, request_url + "&DisplayMode=%E8%AF%A6%E7%BB%86%E6%96%B9%E5%BC%8F"),
                                     meta={"discipline_subject": discipline + "-" + subject},
                                     callback=self.parse_list)

    def parse_list(self, response):
        nodes = response.css("#lblList .colPicDetail")

        for i in range(0, len(nodes)):
            p = nodes[i].css(".colPicText p").extract_first("")
            IF = re.findall("复合影响因子：(.*?)<br>", p)
            ave_if = re.findall("综合影响因子：(.*?)<br>", p)
            cn_name = re.findall("中文名称：(.*?)<br>", p)
            en_name = re.findall("英文名称：(.*?)<br>", p)
            former_name = re.findall("曾用刊名：(.*?)<br>", p)
            cited_num = re.findall("被引频次：(.*?)<br>", p)
            item = JournalItem()
            item["ISSN"] = ""
            item["IF"] = "" if len(IF) == 0 else IF[0]
            item["ave_if"] = "" if len(ave_if) == 0 else ave_if[0]
            item["cn_name"] = "" if len(cn_name) == 0 else cn_name[0]
            item["en_name"] = "" if len(en_name) == 0 else en_name[0]
            item["former_name"] = "" if len(former_name) == 0 else former_name[0]
            item["countryOrRegion"] = ""
            item["discipline_subject"] = response.meta.get("discipline_subject", "")
            item["self_cited_rate"] = ""
            item["url"] = nodes[i].css(".Pic a::attr(href)").extract_first("")
            item["cited_num"] = "" if len(cited_num) == 0 else cited_num[0].strip(' ')
            if item["url"] == "":
                print(item)
                yield item
            else:
                item["url"] = pa.urljoin(response.url, item["url"])
                yield scrapy.Request(url=item["url"], meta={"item": item}, callback=self.parse_detail)

        last_page = response.css("span#lblPageCount2::text").extract_first("")
        cur_page = response.css("input#txtPageGoTo::attr(value)").extract_first("")

        # 若有翻页
        if cur_page != last_page:
            VIEWSTATE = response.css("#__VIEWSTATE::attr(value)").extract_first("")

            url = response.url
            d = dict()
            d["__EVENTTARGET"] = "lbNextPage"
            d["__EVENTARGUMENT"] = ""
            d["__VIEWSTATE"] = VIEWSTATE
            d["__VIEWSTATEGENERATOR"] = "D3167B51"
            d["hidUID"] = ""
            d["hidType"] = "CJFD"
            d["drpField"] = "cykm$%'{0}'"
            d["txtValue"] = ""
            d["DisplayModeRadio"] = "详细方式"
            d["drpAttach"] = "order by idno"
            d["txtPageGoTo"] = cur_page
            d["DisplayModeRadio1"] = "详细方式"
            d["drpAttach"] = "order by idno"
            d["txtPageGoToBottom"] = cur_page
            yield scrapy.FormRequest(url=url,
                                     formdata=d,
                                     meta={"discipline_subject": response.meta.get("discipline_subject")},
                                     callback=self.parse_list)
        pass

    def parse_detail(self, response):
        item = response.meta.get("item")
        p = [i for i in response.css("#tdInfo p").extract() if re.search('刊名', i)]
        p = p[0]
        try:
            item["ISSN"] = re.findall('ISSN：</strong>\xa0(.*?)<br><strong>', p)[0]
        except:
            item["ISSN"] = ""
        try:
            item["countryOrRegion"] = re.findall('出版地：</strong>(.*?)<br><strong>', p)[0]
        except:
            item["countryOrRegion"] = ""
        print(item)
        yield item
