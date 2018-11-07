# -*- coding: utf-8 -*-
import scrapy
from urllib import parse as pa
from spider.paperspider.papers.papers.items import *

import re
import xlwt


class HonorSpider(scrapy.Spider):
    name = 'kejijiang'
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        yield scrapy.Request(url='file:///E:/eds/algorithm/li/other/qinghua/%E8%87%AA%E7%84%B6%E7%A7%91%E5%AD%A6/2002%E5%9B%BD%E5%AE%B6%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%A5%96%E5%8A%B1%E5%A4%A7%E4%BC%9A.html', callback=self.parse_detail)
        pass

    def parse_detail(self, response):

        wbk = xlwt.Workbook(encoding='utf-8')
        sheet = wbk.add_sheet('sheet1')

        year = 2004

        sum = 0

        file_name = "".join(response.css('body > center > table > tbody > tr:nth-child(2) > td > div > table > tbody > tr:nth-child(1) > td > div > font:nth-child(2) > p:nth-child(2) > b ::text').extract())

        print(file_name)

        code_list = []

        tr_node = response.css('body > center > table > tbody > tr:nth-child(2) > td > div > table > tbody > tr:nth-child(1) > td > div > table > tbody >tr')

        level = ""
        for node in tr_node:
            xx = node.css("td[colspan='6'] > p > span ::text").extract_first("")
            if xx == "":
                xx = node.css("td[width='567'] p ::text").extract_first("")
            if xx != "" and re.findall(r'等奖', xx):
                level = xx
            level = "二等奖"
            code = node.css("td[width='25'] ::text").extract()
            p_name = ''.join(node.css("td[width='208'] ::text").extract())
            name_list = node.css("td[width='217'] ::text").extract()
            name_list = ("".join(name_list)).split('、')
            if not code:
                code = node.css("td[width='79'] ::text").extract()

            if p_name == "":
                p_name = ''.join(node.css("td[width='223'] ::text").extract())

            if name_list == [''] or not name_list:
                name_list = node.css("td[width='169'] ::text").extract()
                name_list = ("".join(name_list)).split('、')

            # print("".join(code), p_name, name_list)

            if code and p_name and name_list and not re.findall('项目名称', str(p_name)) and not re.findall('编号', "".join(code)):
                print("".join(code), p_name, name_list)
                for n in name_list:
                    school = re.findall(r'\((.*?)\)', n)
                    if not school:
                        school = re.findall(r'（(.*?)）', n)
                    if not school:
                        school = re.findall(r'（(.*?)\)', n)
                    if not school:
                        school = re.findall(r'\((.*?)）', n)
                    if not school:
                        school = ""
                    else:
                        school = school[0]

                    level = level.strip()

                    code_list.append(self.my_sub("".join(code)))
                    p_name = self.my_sub(p_name)
                    print(level, self.my_sub("".join(code)), p_name, self.my_sub(n), self.my_sub(school))

                    sheet.write(sum, 0, level)
                    sheet.write(sum, 1, self.my_sub("".join(code)))
                    sheet.write(sum, 2, self.my_sub(p_name))
                    sheet.write(sum, 3, self.my_sub(n))
                    sheet.write(sum, 4, self.my_sub(school))

                    sum += 1

        print(len(list(set(code_list))))
        print(sum)
        # wbk.save('E:\\eds\\algorithm\\li\\other\\qinghua\\自然科学\\%s.xls' % file_name)
        wbk.save('E:\\eds\\algorithm\\li\\other\\qinghua\\技术发明\\%s.xls' % file_name)

    def my_sub(self, text=""):
        nn = re.sub(r'\(.*?\)', '', text)
        nn = re.sub(r'（(.*?)\)', '', nn)
        nn = re.sub(r'\((.*?)）', '', nn)
        nn = re.sub(r'（.*?）', '', nn)
        nn = re.sub(r'，', '', nn)
        nn = re.sub(r'\u3000', '', nn)
        nn = re.sub(r' ', '', nn)
        nn = re.sub(r'\xa0', '', nn)
        nn = re.sub(r'\\n', '', nn)
        nn = re.sub(r'\n', '', nn)
        return nn