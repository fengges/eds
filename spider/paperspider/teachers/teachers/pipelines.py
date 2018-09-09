# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from teachers.dbutils import dbs


class TeachersPipeline(object):
    def process_item(self, item, spider):
        return item


class TeacherDataPipeline(object):
    def process_item(self, item, spider):
        sql = "update eds_985teacher set html = %s where id = %s"
        params = (item["html"], item["id"])
        dbs.exe_sql(sql, params=params)
        return item


class TeacherImgPipeline(object):
    def process_item(self, item, spider):
        sql = "insert teacher_img values(%s,%s,%s,%s)"
        params = (item["id"], item["name"], item["image"], item["homepage"])
        dbs.exe_sql(sql, params=params)
        return item
