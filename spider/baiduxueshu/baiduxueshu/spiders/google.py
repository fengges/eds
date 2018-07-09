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
    name = 'google'
    allowed_domains = []
    start_urls = ['http://www.baidu.com/']
    db_li = mysql.DB("LiWei")
    db_localhost = mysql.DB("local")

    def parse(self, response):
        self.ctx = execjs.compile("""
            function TL(a) {
            var k = "";
            var b = 406644;
            var b1 = 3293161072;

            var jd = ".";
            var $b = "+-a^+6";
            var Zb = "+-3^+b+-f";

            for (var e = [], f = 0, g = 0; g < a.length; g++) {
                var m = a.charCodeAt(g);
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                e[f++] = m >> 18 | 240,
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                e[f++] = m >> 6 & 63 | 128),
                e[f++] = m & 63 | 128)
            }
            a = b;
            for (f = 0; f < e.length; f++) a += e[f],
            a = RL(a, $b);
            a = RL(a, Zb);
            a ^= b1 || 0;
            0 > a && (a = (a & 2147483647) + 2147483648);
            a %= 1E6;
            return a.toString() + jd + (a ^ b)
        };

        function RL(a, b) {
            var t = "a";
            var Yb = "+";
            for (var c = 0; c < b.length - 2; c += 3) {
                var d = b.charAt(c + 2),
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
            }
            return a
        }
        """)
        print("update db")
        # ids=self.db_li.getEnglishPaperSerach()
        # for i in ids:
        #     cn=self.db_localhost.getCnById(i["_id"])
        #     if len(cn)==0:
        #         self.db_li.updateEnglishPaper(i["_id"],0)
        while True:
            print("select ")
            paper = self.db_li.getEnglishPaper()
            if len(paper) != 0:
                for p in paper:
                    key = p["name"] + "." + p["abstract"]
                    url = self.getUrl(key)

                    id = p["_id"]
                    if len(url) >= 16000:
                        self.db_li.updateEnglishPaper(id, 1)
                        continue
                    else:
                        self.db_li.updateEnglishPaper(id, 1)
                        yield scrapy.Request(url, lambda arg1=response, arg2=id: self.PaperInfo(arg1, arg2),
                                              dont_filter=True)
            else:
                break


    def getUrl(self,q):
        url="https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=0&tsel=0&kc=0&tk="+self.getTk(q)+"&q="+q
        return url
    def getTk(self, text):
        return self.ctx.call("TL", text)

    def PaperInfo(self, response,id):
        s=str(response.body,encoding="utf-8")
        null=None
        true=True
        false=False
        if response.status==403:
            return
        list=eval(s)

        cn=""
        item={"id":id}
        for l in list[0]:
            if l[0]:
                cn+=l[0]
        item["cn"]=cn
        records = {"table": "englist_to_cn", "params": item}
        self.db_localhost.insertItem(records)
        print("save_id:"+str(id))






