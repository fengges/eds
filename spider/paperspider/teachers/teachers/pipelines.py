# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.paperspider.teachers.teachers.dbutils import dbs
from spider.paperspider.teachers.teachers.items import *


class TeachersPipeline(object):
    def process_item(self, item, spider):
        if type(item) == TeacherListItem:
            sql = "INSERT teacher_url(name, school, ins, homepage) VALUES(%s, %s, %s, %s)"
            params = (item["name"], item["school"], item["ins"], item["homepage"])
            dbs.exe_sql(sql, params=params)
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


class NewTeacherPipeline(object):
    def process_item(self, item, spider):
        if type(item) == TeachersItem:
            sql = "update teacherdata_html set html=%s, pic_url=%s where id=%s"
            params = (item["html"], item["pic_url"], item["id"])
            print("========")
            dbs.exe_sql(sql, params=params)
        return item


class BaikePipeline(object):
    def process_item(self, item, spider):
        if type(item) == BaikeItem:
            sql = "UPDATE yuanshi SET baike= CONCAT(baike,%s)  WHERE id=%s"
            params = (item["baike"], item["id"])
            print("========")
            dbs.exe_sql(sql, params=params)
            u_sql = "UPDATE yuanshi SET status=1 WHERE id=%s"
            dbs.exe_sql(u_sql, item["id"])
        return item


class SamplesPipeline(object):
    def process_item(self, item, spider):
        if type(item) == SamplesItem:
            sql = "INSERT negative_samples(url, rank, t_title, c_abstract, detail, search_id) VALUES(%s,%s,%s,%s,%s,%s)"
            params = (item["url"], item["rank"], item["t_title"], item["c_abstract"], item["detail"], item["search_id"])
            dbs.exe_sql(sql, params)

            u_sql = "UPDATE neg_search SET status=1 WHERE id=%s"
            dbs.exe_sql(u_sql, item['search_id'])
        return item
