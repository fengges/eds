# -*- coding: utf-8 -*-
import scrapy
from urllib import parse as pa
from spider.paperspider.papers.papers.items import *


class SchoolSpider(scrapy.Spider):
    name = 'school'
    start_urls = ["https://www.university-list.net/rank1.htm", "https://www.university-list.net/rank1-a.htm",
                  "https://www.university-list.net/rank1-b.htm", "https://www.university-list.net/rank1-c.htm",
                  "https://www.university-list.net/rank1-d.htm"]

    def parse(self, response):
        school_list = response.css("#content > table > tbody > tr > td:nth-child(2)::text").extract()
        school_list = [i.split(' ')[-1] for i in school_list]
        print(len(school_list))
        fw = open("schoolx.txt", "a+", encoding="utf-8")
        fw.write("%s\n" % "\n".join(school_list))
        fw.close()
        pass

