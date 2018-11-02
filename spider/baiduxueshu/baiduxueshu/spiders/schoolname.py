# -*- coding: utf-8 -*-
import scrapy,os
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
    name = 'schoolname'
    allowed_domains = []
    start_urls = ['http://www.baidu.com/']
    slx=mysql.DB("SLX")

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
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.file=open(root+'/data/school2en_dict.txt', 'w', encoding='utf8')
        sql = "select name,english_name from school_info"
        school = self.slx.exe_sql(sql)
        sql2="select school from eds_985teacher group by school"
        school2 = self.slx.exe_sql(sql2)
        dic=[s['school'] for s in school2]
        for s in school:
            if s['english_name'] and len(s['english_name']) > 0:
                name=s["name"]
                if name in dic:
                    print(name)
                    url = self.getUrl(name)
                    yield scrapy.Request(url, lambda arg1=response, arg2=name: self.PaperInfo(arg1, arg2),
                                         dont_filter=True)
            else:
                self.file.write(s['name']+":"+ s['english_name']+'\n')

    def getUrl(self,q):
        url="https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=3&kc=0&tk="+self.getTk(q)+"&q="+q
        return url

    def getTk(self, text):
        return self.ctx.call("TL", text)

    def PaperInfo(self, response,name):
        s=str(response.body,encoding="utf-8")
        null=None
        true=True
        false=False
        if response.status==403:
            return
        list=eval(s)
        cn=""
        for l in list[0]:
            if l[0]:
                cn+=l[0]
        self.file.write(name+":"+cn+'\n')





