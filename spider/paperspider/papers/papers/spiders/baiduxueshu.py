# -*- coding: utf-8 -*-
import scrapy
import os
from spider.paperspider.papers.papers.services.paperservices import paper_service
from urllib import parse as pa
from spider.paperspider.papers.papers import cn2en
from spider.paperspider.papers.papers.spiders.super_spider import SuperSpider
from spider.paperspider.papers.papers.items import *

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

school_dict = eval(open(root + "\\dicts\\school2en_dict.txt", "r", encoding='utf8').read())
ins_dict = eval(open(root + "\\dicts\\institution2en_dict.txt", "r", encoding='utf8').read())

reREG = r'\r|\t|\v|\n|\\n|\\r'
reSPACE = r' '
reCOMM = r'<!--.*?-->'

# source_list = ["APS", "Springer", "Wiley", "IEEEXplore", "RSC publishing", "知网", "维普", "Elsevier", "万方"]


class BaiduxueshuSpider(SuperSpider):
    name = 'baiduxueshu'
    allowed_domains = []
    start_urls = ['http://xueshu.baidu.com/']
    source_list = ["APS", "Springer", "Wiley", "IEEEXplore", "RSC publishing", "知网", "维普", "Elsevier", "万方"]
    max_page = 10

    def parse(self, response):

        # 获取论文列表的url  http://xueshu.baidu.com/s?wd="精确词"+非精确词+author%%3A%%28作者名%%29
        # &tn=SE_baiduxueshu_c1gjeupa
        # &sc_f_para=sc_tasktypefirstAdvancedSearch
        # &sc_hit=1
        # &ie=utf-8
        # &sort=sc_cited 按被引量
        # &filter=sc_year%3D%7B2015%2C2016%7Dsc_la%3D%7B1%7D 搜索时间和英文结果

        request_url = "http://xueshu.baidu.com/s?wd=%s+author%%3A%%28%s%%29&tn=SE_baiduxueshu_c1gjeupa&sc_f_para=sc_tasktypefirstAdvancedSearch&sc_hit=1&ie=utf-8&filter=sc_year%%3D%%7B%s%%2C%s%%7Dsc_la%%3D%%7B1%%7D"

        info_list = paper_service.get_search_list()
        start_time = "2013"
        end_time = "2017"
        for info in info_list:
            ins = "\"" + info['school'] + "\"+\"" + info['institution'] + "\""
            url = request_url % (ins, info['name'], start_time, end_time)
            yield scrapy.Request(url=url,
                                 meta={"author": info['name'], "author_id": info['id'], "cn": "1"},
                                 callback=self.parse_list, headers={"Referer": None})

            try:
                ins_en = "\"" + school_dict.get(info['school'], "") + "\"+\"" + ins_dict.get(info['institution'],
                                                                                             "") + "\""
                url_en = request_url % (ins_en, cn2en.name2en(info['name']), start_time, end_time)
                yield scrapy.Request(url=url_en,
                                     meta={"author": info['name'], "author_id": info['id'], "cn": "2"},
                                     callback=self.parse_list, headers={"Referer": None})
                pass
            except:
                print("出错")
                paper_service.update_error(info["id"])
            pass

    # 获取论文列表
    def parse_list(self, response):
        # print("论文列表页")
        node_list = response.css(".sc_content")
        if not node_list:
            paper_service.update_searched(params=(response.meta.get("cn", "0"), response.meta.get("author_id", "")))
            return

        for node in node_list:
            # year = response.css(".sc_time ::attr(data-year)").extract_first("")
            # if not year == "2017":
            #     continue
            paper = PaperItem()
            paper["author_id"] = response.meta.get("author_id", "")
            paper["year"] = response.css("span.sc_time::attr(data-year)").extract_first("")
            # 论文列表页可解析 论文标题：name、百度学术详情链接：url、被引量：cited_num、关键词:keyword
            paper["name"] = node.css(".c_font a::text").extract_first("")
            paper["url"] = pa.urljoin(response.url, node.css(".c_font a::attr(href)").extract_first(""))
            paper["cited_num"] = super().my_strip(node.css(".sc_cite_cont ::text").extract_first("0"))
            yield scrapy.Request(url=paper["url"],
                                 meta={"paper": paper},
                                 callback=super().paser_detail, headers={"Referer": None})

        # 获取下一页链接
        page_list = response.css("#page .n")
        page_list = [page.css("::attr(href)").extract_first("") for page in page_list
                     if page.css("::text").extract_first("") == "下一页>"]
        cur_page = response.css("#page strong span.pc::text").extract_first("0").strip()
        if len(page_list) > 0 and int(cur_page) < self.max_page:
            # print(cur_page)
            yield scrapy.Request(url=pa.urljoin(response.url, page_list[0]),
                                 meta={"author": response.meta.get("author", ""), "author_id": response.meta.get("author_id", ""), "cn": response.meta.get("cn", "0")},
                                 callback=self.parse_list)
        else:
            # print("更新%s的searched状态……%s" % (response.meta.get("author_id", ""), response.meta.get("cn", "0")))
            paper_service.update_searched(params=(response.meta.get("cn", "0"), response.meta.get("author_id", "")))
