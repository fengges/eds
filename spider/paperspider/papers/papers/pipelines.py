# -*- coding: utf-8 -*-

import time
from spider.paperspider.papers.papers.dbutils import dbs
from spider.paperspider.papers.papers.services.paperservices import paper_service
from spider.paperspider.papers.papers.items import *


class PapersPipeline(object):
    def process_item(self, item, spider):
        if type(item) == PaperItem:
            sql = "insert into paper_new values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s)"
            params = (item["name"], item["url"], item["abstract"], item["org"], item["year"], item["cited_num"],
                      item["source"], item["source_url"], item["keyword"], item["author"], item["author_id"],
                      item["cited_url"], item["reference_url"], item["paper_md5"], "0")
            # try:
            dbs.exe_sql(sql, params=params)
            # except:
            #     print("mysql error")
            paper_service.update_searching(item["author_id"])
        return item


class JournalsPipeline(object):
    def process_item(self, item, spider):
        if type(item) == JournalItem:
            sql = "INSERT INTO journal VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (item["ISSN"], item["IF"], item["ave_if"], item["cn_name"], item["en_name"], item["former_name"],
                      item["countryOrRegion"], item["discipline_subject"], item["self_cited_rate"],
                      item["url"], item["cited_num"])
            dbs.exe_sql(sql, params=params)
        return item


