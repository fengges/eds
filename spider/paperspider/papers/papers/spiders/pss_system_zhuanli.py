# -*- coding: utf-8 -*-
import scrapy
import os
import time
from spider.paperspider.papers.papers.items import *
from urllib import parse as pa
from spider.paperspider.papers.papers.services.zhuanliservices import zhuanli_service
from spider.paperspider.papers.papers.settings import DEFAULT_REQUEST_HEADERS
import json

class PSSZhuanliSpider(scrapy.Spider):
    name = 'pss_zhuanli'
    allowed_domains = []
    start_urls = ['http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml']

    def parse(self, response):

        search_list = zhuanli_service.get_search_list()
        print(len(search_list))

        url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0529-executeCommandSearch.shtml'

        for item in search_list:
            data_dict = dict()
            data_dict["searchCondition.searchExp"] = "((申请（专利权）人=(%s) AND 发明人=(%s)))" % (item["school"], item["name"])
            data_dict["searchCondition.dbId"] = "VDB"
            data_dict["searchCondition.searchType"] = "Sino_foreign"
            data_dict["searchCondition.extendInfo['MODE']"] = "MODE_TABLE"
            data_dict["searchCondition.extendInfo['STRATEGY']"] = "STRATEGY_CALCULATE"
            data_dict["searchCondition.originalLanguage"] = ""
            data_dict["searchCondition.targetLanguage"] = ""
            data_dict["wee.bizlog.modulelevel"] = "0200201"
            data_dict["resultPagination.limit"] = "12"

            cookie_dict = dict()
            cookie_dict["WEE_SID"] = "q28n0KcOs0JHEz7fYUV6mSWQmApfA652DsMWiHVQ2ov58iGNfYKu!-2068312840!-1672688675!1538266277646"
            cookie_dict["IS_LOGIN"] = "true"
            cookie_dict["JSESSIONID"] = "q28n0KcOs0JHEz7fYUV6mSWQmApfA652DsMWiHVQ2ov58iGNfYKu!-2068312840!-1672688675"

            yield scrapy.FormRequest(url=url,
                                     meta={"search_id": item["id"]},
                                     formdata=data_dict,
                                     callback=self.parse_list,
                                     cookies=cookie_dict)

    def parse_list(self, response):
        search_id = response.meta.get("search_id", -1)
        print(str(response.body, 'utf8'))
        if search_id == -1:
            zhuanli_service.update_search_list_none(search_id)
            print("更新status……-1", search_id)
            return

        try:
            result_dict = json.loads(str(response.body, 'utf8'))
            searchResultDTO = result_dict.get("searchResultDTO", {})

            # 获得item list数据
            searchResultRecord = searchResultDTO.get("searchResultRecord", [])
            if not searchResultRecord:
                zhuanli_service.update_search_list_none(search_id)
                print("更新status……-1", search_id)
                return
            for item_dict in searchResultRecord:
                fieldMap = item_dict.get("fieldMap", {})
                if fieldMap:
                    item = PSSZhuanliItem()
                    item["INVIEW"] = self.my_strip(fieldMap["INVIEW"])
                    item["PAVIEW"] = self.my_strip(fieldMap["PAVIEW"])
                    item["TIVIEW"] = fieldMap["TIVIEW"]
                    item["APD"] = fieldMap["APD"]
                    item["AP"] = fieldMap["AP"]
                    item["PD"] = fieldMap["PD"]
                    item["PN"] = fieldMap["PN"]
                    item["search_id"] = search_id
                    print(item)
                    yield item

            # 下一页
            resultPagination = result_dict["resultPagination"]
            totalCount = resultPagination["totalCount"]  # item总数
            limit = resultPagination["limit"]  # 一页显示多少item
            start = resultPagination["start"]  # 开始
            sumLimit = resultPagination["sumLimit"]

            if start + limit >= totalCount:
                zhuanli_service.update_search_list(search_id)
                print("更新status……1", search_id)
                return

            # FormData重要数据
            dealSearchKeywords = searchResultDTO.get("dealSearchKeywords", [])
            literatureSF = searchResultDTO.get("literatureSF", [])
            executableSearchExp = searchResultDTO.get("executableSearchExp", "")

            data_dict = dict()
            data_dict["resultPagination.limit"] = str(limit)
            data_dict["resultPagination.sumLimit"] = str(sumLimit)
            data_dict["resultPagination.start"] = str(start + limit)
            data_dict["resultPagination.totalCount"] = str(totalCount)
            data_dict["searchCondition.sortFields"] = "-APD,+PD"
            data_dict["searchCondition.searchType"] = "Sino_foreign"
            data_dict["searchCondition.originalLanguage"] = ""
            data_dict["searchCondition.extendInfo['MODE']"] = "MODE_TABLE"
            data_dict["searchCondition.extendInfo['STRATEGY']"] = "STRATEGY_CALCULATE"
            data_dict["searchCondition.searchExp"] = literatureSF
            data_dict["searchCondition.executableSearchExp"] = executableSearchExp
            data_dict["searchCondition.dbId"] = ""
            data_dict["searchCondition.literatureSF"] = literatureSF
            data_dict["searchCondition.targetLanguage"] = ""
            data_dict["searchCondition.resultMode"] = "SEARCH_MODE"
            data_dict["searchCondition.strategy"] = ""
            data_dict["searchCondition.searchKeywords"] = ",".join(dealSearchKeywords)

            next_url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml"

            yield scrapy.FormRequest(url=next_url,
                                     meta={"search_id": search_id},
                                     formdata=data_dict,
                                     callback=self.parse_list)
        except:
            zhuanli_service.update_search_list_none(search_id)
            print("更新status……-1", search_id)

    # 去除字符串中空格和其他字符
    def my_strip(self, text=""):
        if text == "":
            return
        text = text.replace("<FONT>", "")
        text = text.replace("</FONT>", "")
        import re
        text = re.sub(r'\u00a0', ' ', text)
        # re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r', '《', '》', ',', '\\r', '\\n', ';', '</FONT>', '<FONT>']
        re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r', ';']
        while len(text) > 0 and text[0] in re_list:
            text = text.lstrip(text[0])
        while len(text) > 0 and text[-1] in re_list:
            text = text.rstrip(text[-1])
        return text