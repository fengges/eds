# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
import uuid
import execjs
from urllib import parse
from spider.baiduxueshu.baiduxueshu.items import *
from spider.baiduxueshu.baiduxueshu.spiders import mysql
from spider.baiduxueshu.baiduxueshu import settings


class PaperSpider(scrapy.Spider):
    handle_httpstatus_list = [403]
    name = 'bing'
    allowed_domains = []
    start_urls = ['https://cn.bing.com/']
    db_li = mysql.DB("LiWei")
    db_localhost = mysql.DB("feng3")

    def parse(self, response):
        url = "https://cn.bing.com/ttranslate?&category=&IG=3B442D438944493185D9CAED09391880&IID=translator.5036.10"
        while True:
            print("select ")
            paper = self.db_li.getEnglishPaper()
            if len(paper) != 0:
                for p in paper:
                    key = p["name"] + "." + p["abstract"]
                    id = p["_id"]
                    print(id)
                    self.db_li.updateEnglishPaper(id, 1)
                    data = {"from": "en", "to": "zh-CHS", "text": key}

                    yield scrapy.FormRequest(
                        url=url,
                        formdata=data,
                        callback=lambda arg1=response, arg2=id: self.parse2(arg1, arg2)
                    )
            else:
                break

    def parse2(self, response,id):
        dict_ret = json.loads(response.body.decode())
        try:
            ret = dict_ret['translationResponse']
        except:
            print(dict_ret)
            return
        if response.status==403:
            return

        item={"id":id,"wh":1}
        item["cn"]=ret
        records = {"table": "englist_to_cn", "params": item}
        self.db_localhost.insertItem(records)
        print("save_id:"+str(id))




