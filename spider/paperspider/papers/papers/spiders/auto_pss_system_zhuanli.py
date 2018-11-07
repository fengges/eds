# -*- coding: utf-8 -*-
import scrapy
import os
import time
import re
from spider.paperspider.papers.papers.items import *
from urllib import parse as pa
from spider.paperspider.papers.papers.services.zhuanliservices import zhuanli_service
from spider.paperspider.papers.papers.settings import DEFAULT_REQUEST_HEADERS
import json

class PSSZhuanliSpider(scrapy.Spider):
    name = 'auto_pss_zhuanli'
    allowed_domains = []
    # start_urls = ['http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml']
    start_urls = ['http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml']

    def parse(self, response):
        """
        模拟登陆，获取cookie
        :param response:
        :return:
        """

        # 获取验证码图片
        img_url = "http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml"

        code = self.get_codeResult(url=img_url)
        if not code:
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

        f_data = dict()
        f_data["j_loginsuccess_url"] = ""
        f_data["j_validation_code"] = "64"
        f_data["j_username"] = "cHBwcGxhbnRf"
        f_data["j_password"] = "emh1YW5saWppYW5zdW8uMTIzNDU="

        date = time.localtime()
        year = date.tm_year
        mon = "0" + str(date.tm_mon) if date.tm_mon < 10 else str(date.tm_mon)
        day = "0" + str(date.tm_mday) if date.tm_mday < 10 else str(date.tm_mday)
        check_url = "http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check?v=%s" % year+mon+day

        yield scrapy.FormRequest(url=check_url,
                                 formdata=f_data,
                                 callback=self.after_login)


        pass

    def after_login(self, response):
        print("after-login")
        print(response)
        # with open('C:\\Users\\Administrator\\Desktop\\teacher.txt', 'r', encoding='utf-8') as f:
        #     search_list = [_.strip() for _ in f.readlines()]
        # # search_list = zhuanli_service.get_search_list()
        # # search_list = ["庄大明"]
        # print(len(search_list))
        #
        # url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0529-executeCommandSearch.shtml'
        #
        # for item in search_list:
        #     data_dict = dict()
        #     # name = item["name"]
        #     # school = item["school"]
        #     name = item
        #     school = "清华大学"
        #     data_dict["searchCondition.searchExp"] = "((申请（专利权）人=(%s) AND 发明人=(%s)))" % (school, name)
        #     data_dict["searchCondition.dbId"] = "VDB"
        #     data_dict["searchCondition.searchType"] = "Sino_foreign"
        #     data_dict["searchCondition.extendInfo['MODE']"] = "MODE_TABLE"
        #     data_dict["searchCondition.extendInfo['STRATEGY']"] = "STRATEGY_CALCULATE"
        #     data_dict["searchCondition.originalLanguage"] = ""
        #     data_dict["searchCondition.targetLanguage"] = ""
        #     data_dict["wee.bizlog.modulelevel"] = "0200201"
        #     data_dict["resultPagination.limit"] = "12"
        #
        #     cookie_dict = dict()
        #     '''
        #     最新cookie
        #     WEE_SID=wxrsGKYgXk5d6xiebNdCqqjMWgW3U2G1wmLlA5SdegWHvS_fYSaD!773455524!164610502!1541559330336;
        #     IS_LOGIN=true;
        #     JSESSIONID=wxrsGKYgXk5d6xiebNdCqqjMWgW3U2G1wmLlA5SdegWHvS_fYSaD!773455524!164610502
        #     '''
        #
        #     cookie_dict["WEE_SID"] = "wxrsGKYgXk5d6xiebNdCqqjMWgW3U2G1wmLlA5SdegWHvS_fYSaD!773455524!164610502!1541559330336"
        #     cookie_dict["IS_LOGIN"] = "true"
        #     cookie_dict["JSESSIONID"] = "wxrsGKYgXk5d6xiebNdCqqjMWgW3U2G1wmLlA5SdegWHvS_fYSaD!773455524!164610502"
        #
        #     # yield scrapy.FormRequest(url=url,
        #     #                          meta={"search_id": item["id"]},
        #     #                          formdata=data_dict,
        #     #                          callback=self.parse_list,
        #     #                          cookies=cookie_dict)
        #     yield scrapy.FormRequest(url=url,
        #                              formdata=data_dict,
        #                              callback=self.parse_list,
        #                              cookies=cookie_dict)

    # def parse_list(self, response):
    #     search_id = response.meta.get("search_id", -1)
    #     print(str(response.body, 'utf8'))
    #     if search_id == -1:
    #         # zhuanli_service.update_search_list_none(search_id)
    #         print("更新status……-1", search_id)
    #         return
    #
    #     try:
    #         result_dict = json.loads(str(response.body, 'utf8'))
    #         searchResultDTO = result_dict.get("searchResultDTO", {})
    #
    #         # 获得item list数据
    #         searchResultRecord = searchResultDTO.get("searchResultRecord", [])
    #         if not searchResultRecord:
    #             # zhuanli_service.update_search_list_none(search_id)
    #             print("更新status……-1", search_id)
    #             return
    #         for item_dict in searchResultRecord:
    #             fieldMap = item_dict.get("fieldMap", {})
    #             if fieldMap:
    #                 item = PSSZhuanliItem()
    #                 item["INVIEW"] = self.my_strip(fieldMap["INVIEW"])
    #                 item["PAVIEW"] = self.my_strip(fieldMap["PAVIEW"])
    #                 item["TIVIEW"] = fieldMap["TIVIEW"]
    #                 item["APD"] = fieldMap["APD"]
    #                 item["AP"] = fieldMap["AP"]
    #                 item["PD"] = fieldMap["PD"]
    #                 item["PN"] = fieldMap["PN"]
    #                 item["search_id"] = search_id
    #                 print(item)
    #                 yield item
    #
    #         # 下一页
    #         resultPagination = result_dict["resultPagination"]
    #         totalCount = resultPagination["totalCount"]  # item总数
    #         limit = resultPagination["limit"]  # 一页显示多少item
    #         start = resultPagination["start"]  # 开始
    #         sumLimit = resultPagination["sumLimit"]
    #
    #         if start + limit >= totalCount:
    #             # zhuanli_service.update_search_list(search_id)
    #             print("更新status……1", search_id)
    #             return
    #
    #         # FormData重要数据
    #         dealSearchKeywords = searchResultDTO.get("dealSearchKeywords", [])
    #         literatureSF = searchResultDTO.get("literatureSF", [])
    #         executableSearchExp = searchResultDTO.get("executableSearchExp", "")
    #
    #         data_dict = dict()
    #         data_dict["resultPagination.limit"] = str(limit)
    #         data_dict["resultPagination.sumLimit"] = str(sumLimit)
    #         data_dict["resultPagination.start"] = str(start + limit)
    #         data_dict["resultPagination.totalCount"] = str(totalCount)
    #         data_dict["searchCondition.sortFields"] = "-APD,+PD"
    #         data_dict["searchCondition.searchType"] = "Sino_foreign"
    #         data_dict["searchCondition.originalLanguage"] = ""
    #         data_dict["searchCondition.extendInfo['MODE']"] = "MODE_TABLE"
    #         data_dict["searchCondition.extendInfo['STRATEGY']"] = "STRATEGY_CALCULATE"
    #         data_dict["searchCondition.searchExp"] = literatureSF
    #         data_dict["searchCondition.executableSearchExp"] = executableSearchExp
    #         data_dict["searchCondition.dbId"] = ""
    #         data_dict["searchCondition.literatureSF"] = literatureSF
    #         data_dict["searchCondition.targetLanguage"] = ""
    #         data_dict["searchCondition.resultMode"] = "SEARCH_MODE"
    #         data_dict["searchCondition.strategy"] = ""
    #         data_dict["searchCondition.searchKeywords"] = ",".join(dealSearchKeywords)
    #
    #         next_url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml"
    #
    #         yield scrapy.FormRequest(url=next_url,
    #                                  meta={"search_id": search_id},
    #                                  formdata=data_dict,
    #                                  callback=self.parse_list)
    #     except:
    #         # zhuanli_service.update_search_list_none(search_id)
    #         print("更新status……-1", search_id)

    def parse_list(self, response):

        try:
            result_dict = json.loads(str(response.body, 'utf8'))
            searchResultDTO = result_dict.get("searchResultDTO", {})

            # 获得item list数据
            searchResultRecord = searchResultDTO.get("searchResultRecord", [])
            if not searchResultRecord:
                print("更新status……-1")
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
                    item["ABSTRACT"] = ""

                    # 跳转-->爬取摘要
                    ID = fieldMap["ID"]

                    f_data = dict()
                    f_data["nrdAn"] = fieldMap["AP"]
                    f_data["cid"] = ID
                    f_data["sid"] = ID
                    f_data["wee.bizlog.modulelevel"] = "0201101"

                    # yield item
                    yield scrapy.FormRequest(url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/viewAbstractInfo0529-viewAbstractInfo.shtml",
                                             formdata=f_data,
                                             meta={"item": item},
                                             callback=self.parse_abstract)

            # 下一页
            resultPagination = result_dict["resultPagination"]
            totalCount = resultPagination["totalCount"]  # item总数
            limit = resultPagination["limit"]  # 一页显示多少item
            start = resultPagination["start"]  # 开始
            sumLimit = resultPagination["sumLimit"]

            if start + limit >= totalCount:
                print("更新status……1")
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
                                     formdata=data_dict,
                                     callback=self.parse_list)
        except:
            # zhuanli_service.update_search_list_none(search_id)
            print("更新status……-1")

    def parse_abstract(self, response):
        item = response.meta.get("item")
        try:
            result_dict = json.loads(str(response.body, 'utf8'))
            abstractInfoDTO = result_dict.get("abstractInfoDTO", {})
            abIndexList = abstractInfoDTO.get("abIndexList", [])
            ab_list = []
            for ab in abIndexList:
                ab_value = ab.get("value", "")
                '''<base:Paragraphs xmlns:base="http://www.sipo.gov.cn/XMLSchema/base" num="0001">本发明公开了一种凝胶聚合电解质膜片的制备方法，制备方法包括以下步骤：步骤A凝胶聚合物电解质前驱液的制备；步骤B凝胶聚合物电解质的配制；步骤C凝胶聚合电解质膜片的制备。优点是：本发明制备出的凝胶电解质膜片双面有离型膜保护，这使得其适用于模切，分条等多种加工过程，有利于高效率的工业化生产；本发明将凝胶电解质膜片化，所制备电池无需隔膜，亦无需注液，凝胶等过程，简化了凝胶聚合物电解质电池的装配工艺，提高了生产效率。</base:Paragraphs>'''
                '''<RESULT><table><tr><td class="content" id="sipoabs_content_5">Abstract：The invention relates to a copper indium gallium selenide film solar battery and a preparation method thereof. The solar battery comprises a substrate, a back electrode layer arranged on the substrate, a light absorption layer arranged on the back electrode layer, a buffer layer arranged on the light absorption layer and a window layer arranged on the buffer layer, and is characterized in that the light absorption layer comprises a copper element (Cu), an indium element (In), a gallium element (Ga) and a selenium element (Se), the light absorption layer is formed by doping the Se element in the original position of Cu&lt;y&gt;(In&lt;1-x&gt;Ga&lt;x&gt;)Se2, and the mol ratio among the elements Se:(Cu+In+Ga) is greater than 1.0 and smaller than and equal to 1.5. The invention further relates to a preparation method of a copper indium gallium selenide film solar battery.</td></tr></table></RESULT>'''
                '''去除标签<>'''
                ab_list.append(re.sub(r'<.*?>', "", ab_value))
            # ab_text = ab_list[0]
            ab_text = "".join(ab_list)
            item["ABSTRACT"] = self.my_strip(ab_text)
            # print(item)
            yield item

        except:
            print("错误")
        pass

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

    # 返回验证码结果
    def get_codeResult(self, url=''):
        import re
        r_s = self.get_BaiDuPicExtract(url=url)

        number_list = re.findall(r'[0-9]+', r_s)
        if len(number_list) == 2:

            op = re.findall(r'{0}(.*?){1}'.format(number_list[0], number_list[1]), r_s)[0]

            if op == "+":
                return str(int(number_list[0]) + int(number_list[1]))
            elif op == "-":
                return str(int(number_list[0]) + int(number_list[1]))
            elif op == "*":
                return str(int(number_list[0]) * int(number_list[1]))
            elif op == "/":
                if number_list[1] == 0:
                    return
                return str(int(number_list[0]) / int(number_list[1]))

        return

    def get_BaiDuPicExtract(self, url):
        from aip import AipOcr
        """ 你的 APPID AK SK """
        APP_ID = '14709450'
        API_KEY = '0zw6HYjooiU1kmkynNGqSn4T'
        SECRET_KEY = 'u2Qag7hW2DnUkFz96on3FrDzLtVmwCDH'

        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        """读取本地图片函数"""

        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                return fp.read()

        """ 如果有可选参数 """
        options = dict()
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        """ 带参数调用通用文字识别, 图片参数为远程url图片 """
        r_json = client.basicGeneralUrl(url, options)

        """识别成功返回的json
        {'log_id': 1551369869026631207, 
        'direction': 0, 
        'words_result_num': 1, 
        'words_result': 
            [{  'words': '82-8=', 
                'probability': {'variance': 0.007439, 'average': 0.91145, 'min': 0.806046}
            }], 
        'language': -1}
        """
        print(r_json)
        words_result = r_json.get("words_result", [])
        words = None
        if words_result:
            words = words_result[0].get("words", "")
        return words

