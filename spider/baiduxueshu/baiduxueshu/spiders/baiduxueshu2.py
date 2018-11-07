
from pypinyin import lazy_pinyin
import scrapy,time,pickle
from  spider.baiduxueshu.baiduxueshu.settings import cookie_str
import re,os
from spider.baiduxueshu.baiduxueshu.spiders import mysql
from urllib.parse import quote
from urllib.parse import unquote
from urllib import parse
def qs(url):
    parseResult = parse.urlparse(url)
    param_dict = parse.parse_qs(parseResult.query)
    return param_dict

class CnkiSpider(scrapy.Spider):
    name = 'baiduxueshu2'
    start_urls = ['http://www.baidu.com']
    slx=mysql.DB("SLX")
    feng3=mysql.DB("feng3")
    school={}
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    def parse(self, response):
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
            self.teacher={f.strip():{"all":-1,"page":[]} for f in file}

        school="清华大学"
        for t in self.teacher:
            if self.teacher[t]['all']==len(self.teacher[t]['page']):
                continue
            url = "https://apps-webofknowledge-com.vpn.seu.edu.cn/WOS_AdvancedSearch.do"
            cookie=self.getCookie()
            formdata=self.getFromData(cookie['SID'],t,school)
            yield scrapy.FormRequest(url=url,
                                     meta={"teacher": t},
                                     formdata=formdata,
                                     callback=self.parse_list,
                                     cookies=cookie)

    def parse_list(self, response):
        error=self.setValue(response.xpath('//div[@id="client_error_input_message"]/text()'))
        print('----------')
        print(error)
        # print(str(response.body, 'utf8'))
        teacher = response.meta.get("teacher", -1)


    def getCookie(self):
        items=cookie_str.split(';')
        cookies={}
        for item in items:
            c=item.split("=")
            cookies[c[0].strip()]=''.join(c[1:]).strip()
        return cookies
    def getFromData(self,sid,name,school):
        sid=sid[1:-1]
        en_name=self.name2enjianc(name)
        en_shcool=self.school[school]
        value='au='+en_name+' and oo='+en_shcool
        value= quote(value, 'utf-8')
        str1="product=UA&search_mode=AdvancedSearch&SID="+sid+"&input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&action=search&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&value%28input1%29="+value+"&value%28searchOp%29=search&limitStatus=collapsed&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=&SinceLastVisit_DATE=&period=Range+Selection&range=ALL&startYear=1900&endYear=2018&editions=WOS.ESCI&editions=WOS.SSCI&editions=WOS.SCI&editions=WOS.IC&editions=WOS.AHCI&editions=WOS.ISSHP&editions=WOS.ISTP&editions=WOS.CCR&collections=WOS&editions=CSCD.CSCD&collections=CSCD&editions=DIIDW.EDerwent&editions=DIIDW.CDerwent&editions=DIIDW.MDerwent&collections=DIIDW&editions=KJD.KJD&collections=KJD&editions=MEDLINE.MEDLINE&collections=MEDLINE&editions=RSCI.RSCI&collections=RSCI&editions=SCIELO.SCIELO&collections=SCIELO&update_back2search_link_param=yes&ssStatus=display%3Anone&ss_showsuggestions=ON&ss_query_language=auto&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A"
        str2='product=WOS&search_mode=AdvancedSearch&SID='+sid+'&input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&action=search&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&value%28input1%29='+value+'&value%28searchOp%29=search&value%28select2%29=LA&value%28input2%29=&value%28select3%29=DT&value%28input3%29=&value%28limitCount%29=14&limitStatus=collapsed&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=&SinceLastVisit_DATE=&period=Range+Selection&range=ALL&startYear=1900&endYear=2018&editions=SCI&editions=SSCI&editions=AHCI&editions=ISTP&editions=ISSHP&editions=ESCI&editions=CCR&editions=IC&update_back2search_link_param=yes&ss_query_language=&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A'
        data=str2.split('&')
        dic={}
        for d in data:
            t=d.split('=')
            if t[0] not in dic:
                dic[t[0]]=[]
            dic[t[0]].append(t[1])
        for k in dic:
            if len(dic[k]):
                dic[k]=dic[k][0]
            else:
                dic[k]=';'.join(dic[k])
        return dic
    def PaperList(self,response):
        teacher = response.meta['teacher']
        list = response.xpath("//div[@class='result sc_default_result xpath-log']")
        for node in list:

            url= "http://xueshu.baidu.com" + self.setValue(node.xpath("./div[1]/h3/a/@href"), "", 0)
            request = scrapy.Request(url, callback=self.PaperInfo)
            request.meta['teacher'] = teacher
            yield request

        a = response.xpath("//span[@class='pc']")
        if len(a)==0:
            self.slx.updateTeacherById(teacher['id'],2)
        else:
            node=a[-1]
            b = self.setValue(node.xpath("./text()"), "", 0)
            pagestr  = re.findall(r"pn=([0-9]+)", response.url)[0]
            page = int(int(pagestr) / 10)+1
            if b == str(page):
                self.slx.updateTeacherById(teacher['id'], 2)
            else:
                url=self.getSearchUrl1(teacher,page)
                request = scrapy.Request(url, callback=self.PaperList)
                request.meta['teacher'] = teacher
                yield request

    def PaperInfo(self, response):
        teacher = response.meta['teacher']
        item={}
        item['author_id'] = teacher["id"]
        # 不在百度学术页面保存老师，因为老师数量大于五的后面的老师解析不出来
        item['name'] = self.setValue(response.xpath("//div[@id='dtl_l']/div[1]/h3[1]/a/text()"))
        item['url'] = response.url
        item['org']= self.setValue(response.xpath("//p[@class='publish_text']/a/text()"))
        item['year'] = self.setValue(response.xpath("//p[@class='publish_text']/span[1]/text()"))
        paper_author_list = response.xpath("//div[@class='author_wr']/p[2]/a")
        item['author'] = self.getAuthorOrg(paper_author_list)
        # 获取构造json链接的相关字段
        try:
            paper_md5 = re.findall(r"paperuri:\((.+)\)", str(response.body, 'utf-8'))[0]
            item['paper_md5'] = paper_md5
        except:
            try:
                paper_md5 = re.findall(r"paperuri:\((.+)\)", str(response.body))[0]
                item['paper_md5'] = paper_md5
            except:
                item['paper_md5'] = ""
                pass

        source_dic = {}
        step={}
        source_list = response.xpath("//a[@class='dl_item']")
        for node in source_list:
            source = self.setValue(node.xpath("./span[2]/text()"), "", 0)
            source_url = self.setValue(node.xpath("./@data-url"), "", 0)
            source_dic[source] = source_url
            if len(source.strip())==0:
                continue
            source_dic[source] = source_url
            step[source]=False
        item['lib_url']=str(source_dic)
        item['step']=str(step)
        abstract = self.setValue(response.xpath("//p[@class='abstract']/text()"), "", 0)
        item['abstract']= abstract
        item['search']=1


        temp={}
        temp["table"]="en_paper"
        temp["params"] =item
        self.feng3.insertItem(temp)

    def qs(self,url):
        parseResult = parse.urlparse(url)
        param_dict = parse.parse_qs(parseResult.query)
        return param_dict
    def getSearchUrl1(self,teacher,page):
        name=self.name2en(teacher['name'])
        page*=10
        school=self.school[teacher['school']]
        text="\""+school+"\" author:("+name+")"
        text = quote(text, 'utf-8')
        url="http://xueshu.baidu.com/s?wd="+text+"&pn="+str(page)+"&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_la%3D%7B1%7D&sc_f_para=sc_tasktype%3D%7BfirstAdvancedSearch%7D&sc_hit=1"
        return url
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







