
from pypinyin import lazy_pinyin
import scrapy,time
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
    name = 'baiduxueshu'
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

        self.slx.updateTeacherBySearch(3,1)
        while True:
            teacher=self.slx.getTeacher(3)
            if len(teacher)==0:
                break
            for t in teacher:
                self.slx.updateTeacherById(t['id'],1)
                if len(t['name'])==0:
                    continue
                url=self.getSearchUrl1(t,0)
                request = scrapy.Request(url, callback=self.PaperList)
                request.meta['teacher'] = t
                yield request

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

    def getAuthorOrg(self, paper_author_list):
        name_list = paper_author_list.xpath("./text()").extract()
        url_list = paper_author_list.xpath("./@href").extract()
        if (len(name_list) == len(url_list) and len(name_list) < 6):
            paper_author_out = "["
            for i in range(0, len(url_list)):
                t = re.findall(r'[\u4E00-\u9FA5]+', parse.unquote(url_list[i]))
                if len(t) == 2:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (t[0], t[1])
                elif len(t) == 1:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (t[0], "")
                elif len(t) == 0:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (
                        name_list[i].replace("\r\n        ", ""), "")
                else:
                    return ""
            return paper_author_out.rstrip(',') + ']'
        else:
            return ""

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
    def setPaperOrg(self, node):
        data = node.xpath("./div[1]/div[1]/span[2]/a")
        if len(data):
            return data.xpath('string(.)').extract()[0].strip()
        else:
            return self.setValue(node.xpath("./div[1]/div[1]/span[2]/em/text()"), "", 0)
    def name2en(self,name=""):
        fu_dict = {}.fromkeys(
            open(self.root+'/data/fu.txt', 'r', encoding='utf8').read().split('\n'), "ok")
        name_list = lazy_pinyin(name)
        if len(name) > 2 and fu_dict.get(name[0:2], "") != "":
            return "".join(name_list[2:]) + " " + name_list[0] + name_list[1]
        else:
            return "".join(name_list[1:]) + " " + name_list[0]






