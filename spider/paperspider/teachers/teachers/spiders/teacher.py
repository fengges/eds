# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import XmlResponse
import re
from teachers.dbutils import dbs
from teachers.items import *


class KaoyanbangSpider(scrapy.Spider):
    name = 'teacherspider'
    allowed_domains = []
    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        sql = "SELECT * FROM eds_985teacher WHERE html IS NULL AND all_link IS NOT NULL AND all_link NOT LIKE '%.sdu.edu.cn%';"
        info_list = dbs.getDics(sql)
        print(len(info_list))
        for info in info_list:
            teacher = TeachersItem()
            teacher["id"] = info["id"]
            request_url = info["all_link"]
            try:
                yield scrapy.Request(url=request_url,
                                     meta={"teacher": teacher},
                                     callback=self.parse_info)
            except:
                fw = open("id.txt", "a+", encoding="utf-8")
                fw.write("%s\n" % info["id"])
                fw.close()
                pass

    def parse_info(self, response):
        teacher = response.meta.get("teacher", "")
        # 分别解析 考研网链接
        if re.search(r'yz\.kaoyan\.com', response.url) is not None:
            html = response.css(".articleCon").extract_first("")
            text = "\n".join([re.sub(r'[\t|\r|\n|\a]', '', i) for i in response.css(".articleCon ::text").extract() if i])
            di = dict()
            di["info"] = text
            teacher["info"] = str(di)
            teacher["html"] = html
        elif re.search(r'www\.chinakaoyan\.com', response.url) is not None:
            text_list = response.xpath("//div[@class='arc-body font14']")
            html = text_list[1].extract()
            html = html.replace('<strong>', '(strong)').replace('</strong>', '(estrong)')
            strInfo = html
            strInfo = re.sub("<script[^>]*?>.*?</script>", "\r\n", strInfo)
            strInfo = re.sub("<style[^>]*?>.*?</style>", "\r\n", strInfo)
            strInfo = re.sub("<[^>]*>", "\r\n", strInfo)
            strInfo = strInfo.replace("&nbsp;", " ")

            strhaha = strInfo.split('\r\n')
            out = ""
            for node in strhaha:
                if len(node.strip()) > 0:
                    out += node.strip() + '\n'

            strList = out.split('(strong)')

            infodic = {'info': ''}
            for strnode in strList:
                try:
                    strnodelist = strnode.split('(estrong)')
                    key = strnodelist[0]
                    value = strnodelist[1]
                    infodic[key] = value
                except:
                    infodic['info'] += strnode

            teacher["info"] = str(infodic)
            teacher["html"] = html
            pass
        elif re.search(r'cksp\.eol\.cn', response.url) is not None:
            t = dict()
            html = response.xpath("//body/table[5]/tr[1]/td[1]").extract_first("")
            print(response.css("body > table:nth-child(5) > tr > td:nth-child(1)").extract())
            if response.url.find("http://cksp.eol.cn/tutor_detail.php") < 0:
                info = self.getBody(response)[0].xpath('string(.)').extract()[0]
                info = self.replaceWhite(info)
                t['info'] = str({'info': info})
            else:
                sex = self.setValue(response.xpath("//table[@class='tab_02']/tr[1]/td[2]/text()"), ' ')
                birth = self.setValue(response.xpath("//table[@class='tab_02']/tr[1]/td[3]/text()"), ' ')
                zhicheng = self.setValue(response.xpath("//table[@class='tab_02']/tr[3]/td[1]/text()"), ' ')
                zhuanye = self.setValue(response.xpath("//table[@class='tab_02']/tr[3]/td[2]/a/text()"), ' ')
                field = self.setValue(response.xpath("//table[@class='tab_02']/tr[4]/td[1]/text()"), ' ')

                email = self.setValue(response.xpath("//table[@class='tab_01']/tr[1]/td[2]/text()"), ' ')
                phone = self.setValue(response.xpath("//table[@class='tab_01']/tr[1]/td[4]/text()"), ' ')
                youbian = self.setValue(response.xpath("//table[@class='tab_01']/tr[1]/td[6]/text()"), ' ')
                address = self.setValue(response.xpath("//table[@class='tab_01']/tr[2]/td[2]/text()"), ' ')

                biref = self.setValue(response.xpath("//div[@id='short_intro']/text()"), ' ')
                award = self.setValue(response.xpath("//div[@id='short_award']/text()"), ' ')
                thesis = self.setValue(response.xpath("//div[@id='short_thesis']/text()"), ' ')
                item = dict()
                item["性别"] = sex
                item["出生年月"] = birth
                item["职称"] = zhicheng
                item["招生专业"] = zhuanye
                item["研究领域"] = field
                item["E-mail"] = email
                item["电话"] = phone
                item["邮编"] = youbian
                item["地址"] = address
                item["个人简介"] = biref
                item["获得奖项"] = award
                item["著作及论文"] = thesis
                t['info'] = str(item)
            teacher["info"] = str(t)
            teacher["html"] = html
            pass
        else:
            teacher["info"] = "\n".join(response.css('body ::text').extract())
            teacher["html"] = response.css('body').extract()

        yield teacher
        pass

    def getBody(self, response):
        body = response.xpath("//html")
        if len(body) >= 2:
            return body
        body = response.xpath("//body")
        if len(body) == 0:
            if type(response) == XmlResponse:
                body = response.xpath("//Page")
                if len(body) == 0:
                    body = response.xpath("//resume")
                return body
            else:
                return response.xpath('//*')
        else:
            return body

    def replaceWhite(self, info):
        p1 = re.compile('\s+')

        new_string = re.sub(p1, ' ', info)
        return new_string

    def setValue(self, node, value):
        if len(node):
            return node.extract()[0]
        else:
            return value
