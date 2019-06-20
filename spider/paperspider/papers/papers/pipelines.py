# -*- coding: utf-8 -*-

import time
from spider.paperspider.papers.papers.dbutils import dbs
from spider.paperspider.papers.papers.services.paperservices import paper_service
from spider.paperspider.papers.papers.items import *
from spider.paperspider.papers.papers.services.zhuanliservices import zhuanli_service
from spider.paperspider.papers.papers.services.cnkizhuanli_service import cnkizhuanli_service


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
            print(params)
            dbs.exe_sql(sql, params=params)
        return item


class AuthorPipeline(object):
    def process_item(self, item, spider):
        if type(item) == UpdateInstitutionItem:
            sql = "UPDATE paper_new SET author=%s WHERE _id=%s"
            params = (item["author"], item["_id"])

            dbs.exe_sql(sql, params=params)
        return item


class AbstractPipeline(object):
    def process_item(self, item, spider):
        if type(item) == UpdateAbstractItem:
            sql = "UPDATE paper_90_clean_1 SET name=%s,abstract=%s,org=%s,keyword=%s WHERE _id=%s"
            params = (item["name"], item["abstract"], item["org"], item["keyword"], item["_id"])
            dbs.exe_sql(sql, params=params)
            paper_service.abstract_search_list_update(item["_id"])
        return item


class CNKIZhuanliPipeline(object):
    def process_item(self, item, spider):
        if type(item) == CNKIZhuanliItem:
            sql = "INSERT INTO cnki_zhuanli(id,title,author_list,url,proposer,date1,date2,search_id) VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)"
            params = (item["title"], item["author_list"], item["url"], item["proposer"], item["date1"], item["date2"], item["search_id"])
            dbs.exe_sql(sql, params=params)
            cnkizhuanli_service.update_search_list_ing(item['search_id'])
        return item


class PSSZhuanliPipeline(object):
    def process_item(self, item, spider):
        if type(item) == PSSZhuanliItem:
            sql = "INSERT INTO pss_zhuanli(id, TIVIEW, ABSTRACT, INVIEW, PAVIEW, _ID, AP, APD, PN, PD, search_id) VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (item["TIVIEW"], item["ABSTRACT"], item["INVIEW"], item["PAVIEW"], item["_ID"], item["AP"], item["APD"], item["PN"], item["PD"], item["search_id"])
            dbs.exe_sql(sql, params=params)
            zhuanli_service.update_search_list_ing(item['search_id'])
        return item


class TermPipeline(object):
    def process_item(self, item, spider):
        if type(item) == TermItem:
            sql = "UPDATE paper_data SET term_doc=%s WHERE id=%s"
            params = (item["term"], item["id"])
            dbs.exe_sql(sql, params=params)
        return item


class JiechuPipeline(object):
    def process_item(self, item, spider):
        if type(item) == JiechuItem:
            print("*" * 6)
            print(item)
            sql = "INSERT INTO jiechu(id, name, year, detail, url, img_url) VALUES(NULL,%s,%s,%s,%s,%s)"
            params = (item["name"], item["year"], item["detail"], item["url"], item["img_url"])
            dbs.exe_sql(sql, params=params)
        return item


class CNKIABSTRACTPipeline(object):
    def process_item(self, item, spider):
        if type(item) == CNKIABSTRACTItem:
            print("*" * 6)
            sql = "UPDATE cnki_zhuanli SET abstract=%s, ip_content=%s WHERE id=%s"
            params = (item["abstract"], item["ip_content"], item["id"])
            dbs.exe_sql(sql, params=params)
        return item


