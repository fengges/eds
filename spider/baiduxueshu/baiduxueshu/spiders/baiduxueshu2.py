
from pypinyin import lazy_pinyin
import scrapy,time,pickle
from  spider.baiduxueshu.baiduxueshu.settings import cookie_str
import re,os
from spider.baiduxueshu.baiduxueshu.spiders import mysql
from urllib.parse import quote
import uuid
from urllib import parse
def qs(url):
    parseResult = parse.urlparse(url)
    param_dict = parse.parse_qs(parseResult.query)
    return param_dict

class CnkiSpider(scrapy.Spider):
    name = 'baiduxueshu2'
    start_urls = ['http://www.baidu.com']
    slx=mysql.DB("SLX")
    feng1=mysql.DB("feng1")
    school={}
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    query={}
    url="http://apps.webofknowledge.com"
    def parse(self, response):
        self.cookie_str = input("请输入cookie")
        if len(self.school)==0:
            sql="select name,english_name from school_info"

            file=open(self.root+'/data/school2en_dict.txt', 'r', encoding='utf8').readlines()
            self.school={s.split(":")[0]:s.split(":")[1].strip() for s in file}
            school=self.slx.exe_sql(sql)
            for s in school:
                if s['english_name'] and len(s['english_name'])>0:
                    self.school[s['name']]=s['english_name']
        try:
            self.teacher=pickle.load(open(self.root+"/data/teacherdic",'rb'))
        except:
            file=open(self.root+"/data/teacher.txt",'r',encoding='utf8').readlines()
            self.teacher={f.strip():{"name":f.strip(),"all":-1,"page":[],"url":"","query":""} for f in file}
        school="清华大学"
        for t in self.teacher:
            value=self.getValue(t,school)
            self.teacher[t]['url']=''
            self.query[value]=t

        for t in self.teacher:
            if self.teacher[t]['all']==len(self.teacher[t]['page']):
                continue
            url = self.url+"/WOS_AdvancedSearch.do"
            self.cookie=self.getCookie()
            self.value=self.getValue(t,school)
            formdata=self.getFromData(self.cookie['SID'],self.value)
            yield scrapy.FormRequest(url=url,
                                     formdata=formdata,
                                     callback=self.parse_url,
                                     cookies=self.cookie)
            # break

    def parse_url(self, response):

        trs= response.xpath('//div[@class="block-history"]/form/table/tr[@class]')
        for tr in trs:
            url=self.setValue(tr.xpath('./td/div[@class="historyResults"]/a/@href'))
            url=self.url+url
            all = self.setValue(tr.xpath('./td/div[@class="historyResults"]/a/text()')).replace(',','')
            query=self.setValue(tr.xpath("string(./td/div[@class='historyQuery'])")).strip()
            teacher=self.teacher[self.query[query]]
            if len(teacher['url'])!=0:
                continue
            all_page = int(all / 50)
            if all % 50 != 0:
                all_page += 1
            teacher['all']=all_page
            for i in range(all_page):
                if i in teacher['page']:
                    continue
                url1=self.getSearchUrl1(url,str(i+1))
                request = scrapy.Request(url1, callback=self.PaperList)
                request.meta['teacher'] = teacher
                yield request
    def PaperList(self,response):
        page=self.qs(response.url)['page'][0]
        teacher = response.meta['teacher']
        teacher['page'].append(page)
        list = response.xpath("//div[@class='search-results-item']")
        for node in list:
            url=node.xpath("./a[class='smallV110 snowplow-full-record']/@href")
            request = scrapy.Request(url, callback=self.PaperInfo)
            id=uuid.uuid1()
            request.meta['id'] = id
            item = {}
            item['id'] = id
            item['source'] = "sci"
            item['author_id'] = teacher["name"]
            item['url'] = url
            item['search'] = 0
            temp = {}
            temp["table"] = "en_paper"
            temp["params"] = item
            item['url'] = response.url
            self.feng1.insertItem(temp)
            yield request
        # if page==str(teacher['all']):
        #     print("done a teacher")
        #     time.sleep(10)
        #     school = "清华大学"
        #     for t in self.teacher:
        #         if self.teacher[t]['all'] == len(self.teacher[t]['page']):
        #             continue
        #         url = "http://apps.webofknowledge.com/WOS_AdvancedSearch.do"
        #         self.value = self.getValue(t, school)
        #         formdata = self.getFromData(self.cookie['SID'], self.value)
        #         yield scrapy.FormRequest(url=url,
        #                                  formdata=formdata,
        #                                  callback=self.parse_url,
        #                                  cookies=self.cookie)
        #         break

    def PaperInfo(self, response):
        id= response.meta['id']
        item = {}
        item['id'] = id
        item['name'] = self.setValue(response.xpath("//div[@class='title']/value/text()"))

        org= self.setValue(response.xpath('//p[@class="sourceTitle"]/value/text()'))
        item['org'] = org
        year=response.xpath('//p[@class="FR_field"]')
        for y in year:
            title = y.xpath('./span[@class="FR_label"]/text()')
            if title=="出版年:":
                item['year'] = y.xpath('./text()')
        nodes=response.xpath('//p[@class="FR_field"]')

        for n in nodes:
            title=self.setValue(n.xpath('./span[@class="FR_label"]')).strip()
            if title:
                abstract=self.setValue(n.xpath('./text()'))
                item['abstract'] = abstract
            elif title=="KeyWords Plus:":
                keyWord = n.xpath('./a/text()')
                keyword=[ self.setValue(node) for node in keyWord]
                item['keyword'] =";".join(keyword)
        table=response.xpath('//table[@class="FR_table_noborders"]')
        addrs={}
        if len(table)>=1:
            tong=table[0]
            addrs['tong']=";".join([ self.setValue(n) for n in   tong.xpath('./tr/td[@class="fr_address_row2"]/text()')])
        if len(table)==2:
            addr=table[1]
            addrs['tong'] =";".join( [self.setValue(n) for n in addr.xpath('./tr/td[@class="fr_address_row2"]/text()')])
        if len(table)!=2:
            print(response.url)
        item['addr']=str(addrs)
        self.feng1.updateItem(item)
    @staticmethod
    def close(spider, reason):
        print(spider.teacher)
        pickle.dump(spider.teacher,open(spider.root + "/data/teacherdic", 'wb'))
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)
    def getCookie(self):

        items=self.cookie_str.split(';')
        cookies={}
        for item in items:
            c=item.split("=")
            cookies[c[0].strip()]=''.join(c[1:]).strip()
        return cookies
    def getValue(self,name,school):
        en_name=self.name2enjianc(name)
        en_shcool=self.school[school]
        value='au='+en_name+' and oo='+en_shcool
        return value
    def getFromData(self,sid,value):
        sid=sid[1:-1]
        value= quote(value, 'utf-8')
        str1="product=UA&search_mode=AdvancedSearch&SID="+sid+"&input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&action=search&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&value%28input1%29="+value+"&value%28searchOp%29=search&limitStatus=collapsed&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=&SinceLastVisit_DATE=&period=Range+Selection&range=ALL&startYear=1900&endYear=2018&editions=WOS.ESCI&editions=WOS.SSCI&editions=WOS.SCI&editions=WOS.IC&editions=WOS.AHCI&editions=WOS.ISSHP&editions=WOS.ISTP&editions=WOS.CCR&collections=WOS&editions=CSCD.CSCD&collections=CSCD&editions=DIIDW.EDerwent&editions=DIIDW.CDerwent&editions=DIIDW.MDerwent&collections=DIIDW&editions=KJD.KJD&collections=KJD&editions=MEDLINE.MEDLINE&collections=MEDLINE&editions=RSCI.RSCI&collections=RSCI&editions=SCIELO.SCIELO&collections=SCIELO&update_back2search_link_param=yes&ssStatus=display%3Anone&ss_showsuggestions=ON&ss_query_language=auto&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A"
        str2='product=WOS&search_mode=AdvancedSearch&SID='+sid+'&input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&action=search&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&value%28input1%29='+value+'&value%28searchOp%29=search&value%28select2%29=LA&value%28input2%29=&value%28select3%29=DT&value%28input3%29=&value%28limitCount%29=14&limitStatus=collapsed&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=&SinceLastVisit_DATE=&period=Range+Selection&range=ALL&startYear=1900&endYear=2018&editions=SCI&editions=SSCI&editions=AHCI&editions=ISTP&editions=ISSHP&editions=ESCI&editions=CCR&editions=IC&update_back2search_link_param=yes&ss_query_language=&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A'
        return str2

    def qs(self,url):
        parseResult = parse.urlparse(url)
        param_dict = parse.parse_qs(parseResult.query)
        return param_dict
    def getSearchUrl1(self,url,page):
        qid=self.qs(url)['qid']
        SID=self.qs(url)['SID']
        new_url="https://apps-webofknowledge-com.vpn.seu.edu.cn/summary.do?product=WOS&parentProduct=WOS&search_mode=AdvancedSearch&qid="+qid+"&SID="+SID+"&page="+str(page)+"&action=changePageSize&pageSize=50"
        return new_url
    def setValue(self, node, value=None, index=0):
        if len(node):
            return node.extract()[index].strip()
        else:
            return value
    def name2en(self,name=""):
        fu_dict = {}.fromkeys(
            open(self.root+'/data/fu.txt', 'r', encoding='utf8').read().split('\n'), "ok")
        name_list = lazy_pinyin(name)
        if len(name) > 2 and fu_dict.get(name[0:2], "") != "":
            return "".join(name_list[2:]) + " " + name_list[0] + name_list[1]
        else:
            return "".join(name_list[1:]) + " " + name_list[0]

    def name2enjianc(self,name=""):
        fu_dict = {}.fromkeys(
            open(self.root+'/data/fu.txt', 'r', encoding='utf8').read().split('\n'), "ok")
        name_list = lazy_pinyin(name)

        if len(name) > 2 and fu_dict.get(name[0:2], "") != "":
            for n in range(2, len(name_list)):
                name_list[n]=name_list[n][0]
            return name_list[0] + name_list[1]+ " " +  "".join(name_list[2:])
        else:
            for n in range(1, len(name_list)):
                name_list[n]=name_list[n][0]
            return name_list[0]+ " " + "".join(name_list[1:])







