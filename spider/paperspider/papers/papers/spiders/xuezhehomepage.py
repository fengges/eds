# -*- coding: utf-8 -*-
import scrapy
import difflib
import requests
import re
import time
import langid
from urllib import parse
import urllib
from spider.paperspider.papers.papers.spiders.super_spider import SuperSpider
from spider.paperspider.papers.papers.dbutils import dbs
from spider.paperspider.papers.papers.items import *


class XuezhehomepageSpider(SuperSpider):
    name = 'xuezhehomepage'
    start_urls = ['http://xueshu.baidu.com/']
    source_list = ["APS", "Springer", "Wiley", "IEEEXplore", "RSC publishing", "知网", "维普", "Elsevier", "万方"]

    def parse(self, response):
        # 获取学者列表的请求链接
        # https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=search_author
        # &author=姓名&affiliate=机构&curPageNum=1
        request_url = "http://xueshu.baidu.com/usercenter/data/authorchannel?cmd=search_author&author=%s&affiliate=%s&curPageNum=1"

        date = "2017"

        sql = "select * from teacher"
        info_list = dbs.getDics(sql)
        for info in info_list:
            ins = "" + info['school'] + info['institution']
            result = requests.get(request_url % (info["name"], ins))
            try:
                htmldata = result.json().get("htmldata")
                p_list = re.findall(r'<div class="searchResultItem.*?</div>', htmldata)
                for p in p_list:
                    name_and_url = re.search(r'<a class="personName" href="(.*?)".*?>(.*?)</a>', p)
                    org = re.search(r'<p class="personInstitution.*?>(.*?)</p>', p).group(1)
                    homepage_url = name_and_url.group(1)
                    name = name_and_url.group(2)
                    if name == info["name"] and difflib.SequenceMatcher(None, org, ins).quick_ratio() > 0.75:
                        yield scrapy.Request(urllib.parse.urljoin(response.url, homepage_url),
                                             meta={"author": info['name'], "author_id": info['id'], "date": date},
                                             callback=self.parse_list)
                        break
            except:
                print("skip")
        pass

    def parse_list(self, response):
        node_list = response.css(".result")

        if not re.findall(r'<html', str(response.body, "utf-8")):
            print("------")
            pass
        for node in node_list:
            year = response.css(".res_info .res_year::text").extract_first("")
            title = node.css(".res_t a::text").extract_first("")
            date = response.meta.get("date", "2017")
            if not (year == date and langid.classify(title)[0] == "en"):
                continue
            paper = PaperItem()
            # 学者主页列表姓名全称
            author_list = [i for i in node.css(".res_info a::text").extract() if len(re.findall(r'《', i)) == 0]
            paper["year"] = date
            paper["author_id"] = response.meta.get("author_id", "")
            # 论文列表页可解析 论文标题：name、百度学术详情链接：url、被引量：cited_num、作者：author
            paper["name"] = title
            paper["author"] = super().set_author_org(author_list, [])
            paper["url"] = urllib.parse.urljoin(response.url, node.css(".res_t a::attr(href)").extract_first("")).replace("https", "http")
            paper["cited_num"] = self.my_strip(node.css(".cite_cont::text").extract_first(""))

            yield scrapy.Request(paper["url"],
                                 meta={"paper": paper},
                                 callback=self.paser_detail,
                                 headers={"Referer": None})

        pages = response.css(".res-page span::attr(data-num)").extract()
        cur_page = response.css("span.res-page-number-now::attr(data-num)").extract_first("0")

        # 若有翻页，且当前页为第一页时，表单请求第2页至最后一页
        if pages and cur_page == "1":
            last = int(pages[-1])
            entity_id = re.search(r'entity_id=([a-z|A-Z|0-9]*)', str(response.body, "utf-8")).group(1)
            for i in range(1, last):
                url = 'https://xueshu.baidu.com/usercenter/data/author'
                d = dict()
                d["cmd"] = "academic_paper"
                d["entity_id"] = entity_id
                d["bsToken"] = "the fisrt two args should be string type:0,1!"
                d["sc_sort"] = "sc_time"
                d["curPageNum"] = str(i + 1)
                yield scrapy.FormRequest(url=url,
                                         formdata=d,
                                         meta={"author": response.meta.get("author", ""), "author_id": response.meta.get("author_id", ""), "date": response.meta.get("date", "")},
                                         callback=self.parse_list)
            pass

    # 解析百度学术论文详情页, 对于作者author处理与baiduxueshu不一样
    def paser_detail(self, response):
        print("homepage百度学术论文详情")
        paper = response.meta.get("paper")

        # 详情页面可解析 出版源：org、作者：author、摘要：abstract
        # 参考文献：reference_url、引证文献：cited_url
        # 来源：source、源链接：source_url、论文来源与链接：source、source_url
        # 摘要可能不全
        # 作者姓名可能是英文
        # 参考文献链接：http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_时间&wd=refpaperuri:(论文uri)&req_url=论文url&type=citation&rn=10&page_no=1&_=时间
        # 引证文献链接：http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_时间&wd=citepaperuri:(论文uri)&req_url=论文url&type=reference&rn=10&page_no=1&_=时间

        reference_url = "http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_%s&wd=refpaperuri:(%s)&req_url=%s&type=citation&rn=10&page_no=1&_=%s"
        cited_url = "http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_%s&wd=citepaperuri:(%s)&req_url=%surl&type=reference&rn=10&page_no=1&_=%s"

        paper["reference_url"] = ""
        paper["cited_url"] = ""
        paper_url = response.css("a.sc_collect ::attr(data-url)").extract_first("")
        try:
            paper_uri = re.search(r'paperuri:\((.*?)\)', str(response.body, "utf-8")).group(1)
        except:
            paper_uri = ""
        if not (paper_url == "" or paper_uri == ""):
            time_now = str(int(time.time()) * 1000)
            paper["reference_url"] = reference_url % (time_now, paper_uri, paper_url, time_now)
            paper["cited_url"] = cited_url % (time_now, paper_uri, paper_url, time_now)
        paper["paper_md5"] = paper_uri
        paper["keyword"] = ""
        paper["org"] = super().my_strip(response.css(".publish_text a::text").extract_first("")).strip("《").strip("》")
        paper["abstract"] = "".join(super().my_list_strip(response.css(".abstract ::text").extract()))
        paper["source"], paper["source_url"] = \
            super().set_source_url(response.css("#allversion_wr .allversion_content .dl_item_span"))
        if paper["source_url"] != "":
            if not paper["author"] == '{"author": []}':
                paper["author"] = super().set_author_org(response.css(".author_text a::text").extract(), [])
            yield scrapy.Request(url=paper["source_url"], meta={"paper": paper}, callback=super().paser_source)
            pass
        elif paper_uri != "":
            print("homepage百度学术")
            # print(paper)
            yield paper
            pass
        pass


