# -*- coding: utf-8 -*-
import scrapy
import os
import time
from spider.paperspider.papers.papers.items import *
from urllib import parse as pa
from spider.paperspider.papers.papers.services.cnkizhuanli_service import cnkizhuanli_service


class CNKIZhuanliSpider(scrapy.Spider):
    name = 'cnki_zhuanli'
    allowed_domains = []
    start_urls = ['http://kns.cnki.net/kns/index.html?code=SCOD']

    def parse(self, response):

        search_list = cnkizhuanli_service.get_search_list()
        print(len(search_list))

        for item in search_list:
            keyvalue = item['school']+item['name']
            loctime = time.strftime("%a %b %d %Y %H:%M:%S GMT+0800", time.localtime())
            url = "http://kns.cnki.net/kns/request/SearchHandler.ashx?action=&NaviCode=*&ua=1.11&PageName=ASP.brief_default_result_aspx&DbPrefix=SCOD&DbCatalog=中国学术文献网络出版总库&ConfigFile=SCDBINDEX.xml&db_opt=SCOD&txt_1_sel=FT$%%=|&txt_1_value1=%s&txt_1_special1=%%&his=0&parentdb=SCDB&__=%s" % (keyvalue, loctime)

            yield scrapy.Request(url=url,
                                 meta={"school": item['school'], "name": item['name'], "search_id": item['id']},
                                 callback=self.parse_start)
            # break

    # 目的：获取cookie
    def parse_start(self, response):
        print(response.body)
        school = response.meta.get("school", "")
        name = response.meta.get("name", "")
        search_id = response.meta.get("search_id", "")
        key = school + " " + name
        t = str(int(time.time()) * 1000)
        url = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCOD&dbCatalog=中国学术文献网络出版总库&ConfigFile=SCDBINDEX.xml&research=off&t=%s&keyValue=%s&S=1" % (t, key)

        try:
            yield scrapy.Request(url=url,
                                 meta={"school": school, "name": name, "search_id": search_id},
                                 callback=self.parse_list)
        except:
            cnkizhuanli_service.update_search_list_error(search_id)
            pass

    # 解析列表
    def parse_list(self, response):

        school = response.meta.get("school", "")
        name = response.meta.get("name", "")
        search_id = response.meta.get("search_id", "")

        tr_list = response.css(".GridTableContent tr[bgcolor^='#']")

        if not tr_list:
            cnkizhuanli_service.update_search_list_none(search_id)

        for tr in tr_list:
            p_name = self.my_strip("".join(tr.css("td:nth-child(2) ::text").extract()))
            a_url = tr.css("td:nth-child(2) a::attr(href)").extract_first("")
            author_list = self.my_strip("".join(tr.css("td:nth-child(3) ::text").extract()))
            proposer = self.my_strip("".join(tr.css("td:nth-child(4) ::text").extract()))
            date1 = self.my_strip(tr.css("td:nth-child(6) ::text").extract_first(""))
            date2 = self.my_strip(tr.css("td:nth-child(7) ::text").extract_first(""))

            item = CNKIZhuanliItem()
            item["title"] = p_name
            item["url"] = pa.urljoin(response.url, a_url)
            item["author_list"] = author_list
            item["proposer"] = proposer
            item["date1"] = date1
            item["date2"] = date2
            item["search_id"] = search_id

            yield item
            # print(item)

        # 获取下一页链接
        next_page = response.css(".TitleLeftCell a:last-child::attr(href)").extract_first("")

        # 最后一页，更新search_list
        if next_page == "":
            cnkizhuanli_service.update_search_list_all(search_id)
            # 爬完
            print("爬完")
            return

        next_page.rstrip("#J_ORDER&")

        url = "http://kns.cnki.net/kns/brief/brief.aspx%s" % next_page
        yield scrapy.Request(url=url,
                             meta={"school": school, "name": name, "search_id": search_id},
                             callback=self.parse_list)

    # 去除字符串中空格和其他字符
    def my_strip(self, text=""):
        import re
        text = re.sub(r'\u00a0', ' ', text)
        re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r', '《', '》', ',', '\\r', '\\n']
        while len(text) > 0 and text[0] in re_list:
            text = text.lstrip(text[0])
        while len(text) > 0 and text[-1] in re_list:
            text = text.rstrip(text[-1])
        return text
