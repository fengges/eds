# -*- coding: utf-8 -*-
import scrapy
import os
import re
import json
import time
from spider.paperspider.papers.papers.items import *
from urllib import parse as pa

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

school_dict = eval(open(root + "\\dicts\\school2en_dict.txt", "r", encoding='utf8').read())
ins_dict = eval(open(root + "\\dicts\\institution2en_dict.txt", "r", encoding='utf8').read())

reREG = r'\r|\t|\v|\n|\\n|\\r'
reSPACE = r' '
reCOMM = r'<!--.*?-->'


class SuperSpider(scrapy.Spider):

    allowed_domains = []
    source_list = ["Springer"]

    # 解析百度学术论文详情页
    def paser_detail(self, response):
        paper = response.meta.get("paper")

        # 详情页面可解析 出版源：org、作者：author、摘要：abstract
        # 参考文献：reference_url、引证文献：cited_url
        # 来源：source、源链接：source_url、论文来源与链接：source、source_url
        # 摘要可能不全
        # 作者姓名可能是英文
        # 参考文献链接：http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_时间&wd=refpaperuri:(论文uri)&req_url=论文url&type=citation&rn=10&page_no=1&_=时间
        # 引证文献链接：http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_时间&wd=citepaperuri:(论文uri)&req_url=论文url&type=reference&rn=10&page_no=1&_=时间

        reference_url = "http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_%s&wd=refpaperuri:(%s)&req_url=%s&type=citation&rn=10&page_no=1&_=%s"
        cited_url = "http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery1102016936626670962984_%s&wd=citepaperuri:(%s)&req_url=%surl&type=reference&rn=10&page_no=1&_=%s"

        paper["reference_url"] = ""
        paper["cited_url"] = ""
        paper_url = response.css("a.sc_collect ::attr(data-url)").extract_first("")
        try:
            paper_uri = re.search(r'paperuri:\((.*?)\)', str(response.body, "utf-8")).group(1)
        except:
            paper_uri = ""
        if not (paper_url == "" or paper_uri == ""):
            time_now = str(int(time.time())*1000)
            paper["reference_url"] = reference_url % (time_now, paper_uri, paper_url, time_now)
            paper["cited_url"] = cited_url % (time_now, paper_uri, paper_url, time_now)
        paper["paper_md5"] = paper_uri
        paper["keyword"] = ""
        paper["org"] = self.my_strip(response.css(".publish_text a::text").extract_first("")).strip("《").strip("》")
        paper_author_list = response.xpath("//div[@class='author_wr']/p[2]/a")
        paper["author"] = self.get_author_org(paper_author_list)
        paper["abstract"] = "".join(self.my_list_strip(response.css(".abstract ::text").extract()))
        paper["source"], paper["source_url"] = \
            self.set_source_url(response.css("#allversion_wr .allversion_content .dl_item_span"))
        if paper["year"] == "":
            span_list = response.css(".publish_text span::text").extract()
            span_list = [i for i in span_list if re.search(r'20[0-9]{2}', i)]
            paper["year"] = "" if len(span_list) == 0 else span_list[0]

        if paper["source_url"] != "":
            # yield scrapy.Request(url=paper["source_url"],
            #                      meta={"paper": paper},
            #                      callback=self.paser_source)
            pass
        else:
            # 拼接请求url
            data_sign = self.my_strip(response.css(".abstract ::text").extract_first(""))
            sc_url_group = re.search(r'sc_vurl=(.*?)&', response.css(".source a::attr(href)").extract_first(""))
            sc_url = sc_url_group.group(1) if sc_url_group is not None else ""
            if data_sign != "" and sc_url != "":
                t = int(time.time() * 1000)
                request_url = "http://xueshu.baidu.com/usercenter/data/schinfo?url=%s&callback=jQuery1102016936626670962984_%s&sign=%s&_=%s" % (sc_url, t, data_sign, t + 1)
                yield scrapy.Request(url=request_url,
                                     meta={"paper": paper},
                                     callback=self.parse_abstract)
        pass

    # 解析json文件
    def parse_abstract(self, response):
        paper = response.meta.get("paper")
        info_text = response.text.strip(')')
        di = eval(re.sub(r'jQuery.*?\(', '', info_text))
        meta_di_info = di["meta_di_info"]
        abstract = "".join(meta_di_info.get("sc_abstract", []))
        title = "".join(meta_di_info.get("sc_title", []))
        paper["keyword"] = ";".join(meta_di_info.get("sc_keyword", []))
        paper["abstract"] = abstract
        paper["name"] = title
        if not abstract[-3:] == "...":
            paper["source_url"] = ""
            paper["source"] = ""
            # print(paper)
            print("百度学术")
            yield paper
        pass

    def paser_source(self, response):
        paper = response.meta.get("paper")
        # 知网链接
        if paper["source"] == "知网":
            a_text = ""
            # 知网空间-1
            if re.search(r'en\.cnki\.com\.cn', paper["source_url"]) is not None:
                a_text = self.my_strip("".join(response.css("#content > div:nth-child(1) > div:nth-child(4) ::text").extract()))
                title = " ".join(self.my_list_strip(response.css("#content h2 ::text").extract()))
                if not title == "":
                    paper["name"] = title
                # 解析源页面的author和author_org
                author_list = self.my_list_strip(response.css("#content > div:nth-child(1) > div:nth-child(3) > strong ::text").extract_first("").split(';'))
                if len(author_list) > 0:
                    paper["author"] = self.set_author_org(author_list, [])
            # 知网空间-2,可以解析author,author_org,abstract,title,
            if re.search(r'cpfd\.cnki\.com\.cn', paper["source_url"]) is not None:
                # ==========================
                t_list = response.css("div.xx_font::text").extract()
                t_list = [self.my_strip(i) for i in t_list]
                t_list = [i for i in t_list if len(i) > 0]
                len_list = [len(i) for i in t_list]
                a_text = self.my_strip(t_list[len_list.index(max(len_list))])
                title = " ".join(self.my_list_strip(response.css(".xx_title ::text").extract()))
                if len(title) > len(paper["name"]):
                    paper["name"] = title

                author_list = self.my_list_strip(response.css('#content div[style="text-align:center; width:740px; height:30px;"] a::text').extract())

                org_list = response.css("div.xx_font a::text").extract()
                if len(author_list) > 0:
                    paper["author"] = self.set_author_org(author_list, org_list)

                pass
            # 知网
            if re.search(r'kns\.cnki\.net', paper["source_url"]) is not None:
                a_text = self.my_strip(" ".join(self.my_list_strip(response.css("#ChDivSummary ::text").extract())))
                paper["keyword"] = ";".join(self.my_list_strip(response.css("#catalog_KEYWORD ::text").extract()))
                title = self.my_strip(response.css(".wxTitle .title::text").extract_first(""))
                if len(title) > 0:
                    paper["name"] = title
                # 解析源页面的author和author_org
                author_list = self.my_list_strip(response.css(".author a::text").extract())
                if len(author_list) > 0:
                    paper["author"] = self.set_author_org(author_list, [])

            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text
            # print("知网====")
            pass

        # 维普链接 abstract、keyword、author
        if paper["source"] == "维普":
            a_text = self.my_strip("".join(response.css(".sum::text").extract()))
            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text
            title = self.my_strip(response.css(".detailtitle ::text").extract_first(""))
            if len(title) > len(paper["name"]):
                paper["name"] = title
            author_list = self.my_list_strip(response.css(".detailtitle a[href*='aspx\?w='] ::text").extract())
            if len(author_list) > 0:
                paper["author"] = self.set_author_org(author_list, [])
            paper["keyword"] = ";".join(self.my_list_strip(response.css(".detailinfo > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2) a::text").extract()))
            # print("维普")
            pass

        # 万方链接 title, abstract, author, keyword
        if paper['source'] == "万方":
            # 两种类型链接，分开处理
            if len(re.findall('http://d\.old\.', response.url)) > 0:
                a_list = self.my_strip(" ".join(response.css("div.abstract .text::text").extract()))
                if len(a_list) > len(paper["abstract"]):
                    paper["abstract"] = a_list
                title = response.css("title::text").extract_first("")
                if len(title) > 0:
                    paper["name"] = title
                paper["keyword"] = ";".join(self.my_list_strip(response.css(".row-keyword .text ::text").extract()))
                author_list = self.my_list_strip(response.css(".row-author span.text span::text").extract())
                if len(author_list) > 0:
                    paper['author'] = self.set_author_org(author_list, [])
            else:
                title = self.my_strip(response.css(".title::text").extract_first(""))
                if len(title) > 0:
                    paper["name"] = title
                abstract = self.my_strip(response.css(".abstract textarea::text").extract_first(""))
                if len(abstract) > len(paper["abstract"]):
                    paper["abstract"] = abstract
                paper["keyword"] = ";".join(self.my_list_strip(response.css(".info_right a[onclick*='关键词']::text").extract()))
                author_list = self.my_list_strip(response.css(".info_right a[id*='card']::text").extract())
                if len(author_list) > 0:
                    paper['author'] = self.set_author_org(author_list, [])
            # print("万方")
            pass

        # Springer Link链接 abstract、title、keyword、author、author_org
        if paper["source"] == "Springer":
            try:
                a_text = self.my_strip("".join(response.css(".Para ::text").extract()))
                if len(a_text) > len(paper["abstract"]):
                    paper["abstract"] = a_text
                title = " ".join(self.my_list_strip(response.css(".ArticleTitle ::text").extract()))
                if not title == "":
                    paper["name"] = title
                paper["keyword"] = ";".join(self.my_list_strip(response.css(".Keyword ::text").extract()))

                author_list = response.css("meta[name='citation_author']::attr(content)").extract()
                org_list = []
                for a in author_list:
                    selector = "meta[name='citation_author'][content='%s']+meta[name='citation_author_institution']::attr(content)" % a
                    org = response.css(selector).extract_first("")
                    org_list.append(org)
                if len(author_list) > 0:
                    paper["author"] = self.set_author_org(author_list, org_list)
            except:
                paper["source"] = ""
                paper["source_url"] = ""
                print("pdf页面无法解析")
            # print("Springer")
            pass

        # Wiley Online Library链接 abstract、author、author_org、keyword、title
        if paper["source"] == "Wiley":
            try:
                a_text = self.my_strip("".join(response.css(".article-section__content p::text").extract()))
                if len(a_text) > len(paper["abstract"]):
                    paper["abstract"] = a_text
                keyword_list = response.css("meta[name='citation_keywords']::attr(content)").extract()
                paper["keyword"] = ";".join(self.my_list_strip([i.strip('\n') for i in keyword_list]))
                title = " ".join(self.my_list_strip(response.css(".citation__title ::text").extract()))
                if len(title) > 0:
                    paper["name"] = title
                author_list = response.css("meta[name='citation_author'] ::attr(content)").extract()
                org_list = response.css("meta[name='citation_author']+meta ::attr(content)").extract()
                if len(author_list) > 0:
                    paper["author"] = self.set_author_org(author_list, org_list)
            except:
                paper["source"] = ""
                paper["source_url"] = ""
                print("pdf页面无法解析")
            # print("Wiley")
            pass

        # ResearchGate链接 abstract、author、author_org
        if paper["source"] == "ResearchGate":
            a_text = self.my_strip("".join(response.css(".nova-e-text.nova-e-text--size-m.nova-e-text--family-sans-serif.nova-e-text--spacing-auto.nova-e-text--color-inherit ::text").extract()))
            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text

            author_list = self.my_list_strip(response.css("div.nova-v-person-list-item__align-content a::text").extract())
            org_list = response.css("div.nova-v-person-list-item__align-content li:nth-child(2) ::text").extract()
            if len(author_list) > 0:
                paper["author"] = self.set_author_org(author_list, org_list)
            # print("ResearchGate")
            pass

        # Elsevier链接 abstract、author、keyword、title
        if paper["source"] == "Elsevier":
            a_text = self.my_strip("".join(response.css(".Abstracts div > div p ::text").extract()))
            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text
            t_text = response.css("h1.Head ::text").extract_first("")
            if len(t_text) > len(paper["name"]):
                paper["name"] = t_text
            author_name = response.css(".AuthorGroups .content")
            author_list = self.my_list_strip([" ".join(i.css(".text ::text").extract()) for i in author_name])
            if len(author_list) > 0:
                paper["author"] = self.set_author_org(author_list, [])
            paper["keyword"] = ";".join(self.my_list_strip(response.css(".Keywords .keyword ::text").extract()))
            # print("Elsevier")
            pass

        # IEEEXplore链接 abstract、title、keyword、author、author_org
        if paper["source"] == "IEEEXplore":
            try:
                s = re.search(r"global\.document\.metadata=(.*?);\n", response.text).group(1)
                d = json.loads(s)
                a_text = d.get("abstract", "")
                if len(a_text) > len(paper["abstract"]):
                    paper["abstract"] = a_text
                title = d.get("title", "")
                if len(title) > len(paper["name"]):
                    paper["name"] = title
                paper["keyword"] = ";".join([";".join(i.get("kwd", [])) for i in d.get("keywords", []) if i.get("type", "") == "Author Keywords "])
                author_list = []
                org_list = []
                for i in d.get("authors", []):
                    author_list.append(i.get("name", ""))
                    org_list.append(i.get("affiliation", ""))
                if author_list:
                    paper["author"] = self.set_author_org(author_list, org_list)
            except:
                paper["source"] = ""
                paper["source_url"] = ""

            # print("IEEEXplore")
            pass

        # RSC publishing链接
        if paper["source"] == "RSC publishing":
            a_text = self.my_strip(response.css("meta[name='citation_abstract']::attr(content)").extract_first(""))
            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text

            title = response.css("meta[name='citation_title']::attr(content)").extract_first("")
            if len(title) > 0:
                paper["name"] = title

            author_list = response.css("meta[name='citation_author']::attr(content)").extract()
            org_list = []
            for a in author_list:
                selector = "meta[name='citation_author'][content='%s']+meta[name='citation_author_institution']::attr(content)" % a
                org_list.append(response.css(selector).extract_first(""))
            if len(author_list) > 0:
                paper["author"] = self.set_author_org(author_list, org_list)

            # print("RSC publishing")
            pass

        # Europe PMC链接 abstract、title、keyword、author、author_org
        if paper["source"] == "Europe PMC":
            a_text = " ".join(response.css('div[id*="abstract"] ::text').extract())
            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text
            title = response.css("meta[name='citation_title']::attr(content)").extract_first("")
            if len(title) > len(paper["name"]):
                paper["name"] = title
            paper["keyword"] = ";".join(response.css(".kwd-text ::text").extract_first("").split(','))
            org_dict = dict()
            org_node = response.css('.fm-affl')
            for node in org_node:
                name = node.css("::text").extract_first("")
                if name.isdigit():
                    text = re.sub('<sup>.*?</sup>', '', node.extract())
                    org_dict[name] = re.search(r'<div.*?>(.*?)</div>', text).group(1)

            name_list = re.findall(r'(<a.*?>.*?)<a', response.css('.fm-author').extract_first(""))
            author_list = []
            org_list = []
            for node in name_list:
                try:
                    name = re.search(r'<a.*?>(.*?)</a>', node).group(1)
                    author_list.append(name)
                except:
                    continue
                sup_list = re.findall(r'<sup>(.*?)</sup>', node)
                org_name = []
                for sup in sup_list:
                    org_name.append(org_dict.get(sup, ''))
                org_name = [i for i in org_name if not i == '']
                org_list.append(";".join(org_name))
            if author_list:
                paper["author"] = self.set_author_org(author_list, org_list)
            # print("Europe PMC")
            pass

        # APS链接 abstract、author、author_org、title
        if paper["source"] == "APS":
            a_text = self.my_strip(response.css("meta[name='description']::attr(content)").extract_first(""))
            if len(a_text) > len(paper["abstract"]):
                paper["abstract"] = a_text

            title = response.css("meta[name='citation_title']::attr(content)").extract_first("")
            if len(title) > 0:
                paper["name"] = title

            author_list = response.css("meta[name='citation_author']::attr(content)").extract()
            org_list = []
            for a in author_list:
                selector = "meta[name='citation_author'][content='%s']+meta[name='citation_author_institution']::attr(content)" % a
                org = response.css(selector).extract_first("")
                org_list.append(org)
            if len(author_list) > 0:
                paper["author"] = self.set_author_org(author_list, org_list)
            # print("APS")
            pass
        if paper["author"] != "":
            # print(paper)
            yield paper
        pass

    # 设置作者author和机构author_org
    def set_author_org(self, author_list, org_list):
        author_list = self.my_list_strip(author_list)
        org_list = self.my_list_strip(org_list)
        di = dict()
        di["author"] = []
        ol = len(org_list)
        for i in range(len(author_list)):
            if len(author_list[i]) > 30:
                continue
            di["author"].append({"name": author_list[i], "org": "" if i >= ol else org_list[i]})

        if di:
            return json.dumps(di)
        return ""

    # 在百度学术页面获取作者和机构信息
    def get_author_org(self, paper_author_list):
        name_list = paper_author_list.xpath("./text()").extract()
        url_list = paper_author_list.xpath("./@href").extract()
        if len(name_list) == len(url_list) and len(name_list) < 6:
            paper_author_out = "["
            for i in range(0, len(url_list)):
                t = re.findall(r'[\u4E00-\u9FA5]+', pa.unquote(url_list[i]))
                if len(t) == 2:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (t[0], t[1])
                elif len(t) == 1:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (t[0], "")
                elif len(t) == 0:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (name_list[i].replace("\r\n        ", ""), "")
                else:
                    return ""
            return paper_author_out.rstrip(',') + ']'
        else:
            return ""

    # 设置源、源链接
    def set_source_url(self, node_list):
        # 按顺序优先选择："知网", "Springer", "维普", "Wiley", "Elsevier", "万方"
        if len(node_list) == 0:
            return "", ""
        source_and_url = {}
        source_and_url.fromkeys(self.source_list, "")

        for node in node_list:
            source = self.my_strip(node.css(".dl_item span.dl_source ::text").extract_first(""))
            source_url = node.css("a.dl_item ::attr(data-url)").extract_first("")
            source_and_url[source] = source_url

        for source in self.source_list:
            if not source_and_url.get(source, "") == "":
                return source, source_and_url.get(source, "")

        return "", ""

    # 去除字符串中空格和其他字符
    def my_strip(self, text=""):
        text = re.sub(r'\u00a0', ' ', text)
        re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r']
        while len(text) > 0 and text[0] in re_list:
            text = text.lstrip(text[0])
        while len(text) > 0 and text[-1] in re_list:
            text = text.rstrip(text[-1])
        return text

    # 去除名字与机构中的空格和其他字符
    def my_list_strip(self, t_list=[]):
        t_list = [self.my_strip(i) for i in t_list]
        return [i for i in t_list if len(i) > 0]

