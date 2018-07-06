# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.baiduxueshu.baiduxueshu.items import *
from spider.baiduxueshu.baiduxueshu.spiders import mysql

class BaiduxueshuPipeline(object):
    # db = mysql.LocalDB()
    # db_test = mysql.TestDB()

    def process_item(self, item, spider):
        if type(item)==PaperItem:
            self.Paper(item)
        # elif type(item)==CitedAndRefItem:
        #     self.CRPaper(item)
        return item

    def Paper(self,item):
        self.db.InsertPaper(item)
        # self.db_test.InsertPaper(item)
        pass
