
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
    name = 'baiduxueshu2'
    start_urls = ['http://www.baidu.com']

    feng3=mysql.DB("feng3")
    school={}
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    def parse(self, response):
        paper=self.feng3.getPaperBySearch(1,100)
        for t in paper:
            lib=eval(t['lib_url'])
            step=eval(t['step'])
            t['step']=step
            t['lib_url'] = lib
            for k in step:
                if not step[k] and self.contain(k,t):
                    url=self.getUrl(k,lib)
                    request = scrapy.Request(url, callback=self.getCallBack(k,url))
                    request.meta['paper'] = t
                    yield request
                    break
            self.feng3.updatePaperSearchById(t['id'],3)
    def getUrl(self,k,lib):
        if k=="Springer":
            url=lib[k].strip()
            if url[-3:]=="pdf":
                index=url.find('pdf')
                text=url[index+3:-4].replace("%2F","/")
                t="https://link.springer.com/article/"+text
                return t
            else:
                return url
        else:
            return lib[k]
    def contain(self,k,t):
        if len(t['lib_url'][k])==0:
            return False
        dic=["知网","万方","维普","Elsevier","ResearchGate","Springer"]
        if k not in dic:
            return False
        abstract=t["abstract"]
        if abstract is None or len(abstract)==0 or abstract[-3:]=="...":
            return True
        org=t["org"]
        if org is None or len(org)==0 or org[-3:]=="...":
            return True
        keyword=t["keyword"]
        if keyword is None or len(keyword)==0:
            if k=="万方":
                return True
            elif k=="维普":
                return True
            elif k=="Elsevier":
                return True
            elif k=="Springer":
                return True
            else:
                return False
        else:
            return False

    def getCallBack(self,k,url):
        if k=="知网":
            if url.find("http://kns.cnki.net/KCMS/detail/detail.aspx")>=0:
                return self.cnki1
            else:
                return self.cnki2
        elif k=="万方":
            if url.find("med")>=0:
                return self.wanfang2
            else:
                return self.wanfang1
        elif k=="维普":
            return self.weipu
        elif k=="Elsevier":
            return self.Elsevier
        elif k=="ResearchGate":
            return self.ResearchGate
        elif k=="Springer":
            return self.Springer
        else:
            return False

    def cnki1(self, response):
        paper = response.meta['paper']
        abstract = self.setValue(response.xpath("//span[@id='ChDivSummary']/text()"),"")
        org = self.setValue(response.xpath("//p[@class='title'/a/text()"),"")
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["知网"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def cnki2(self, response):
        paper = response.meta['paper']
        org = self.setValue(response.xpath("//div[@id='content']/div[1]/div[1]/div[1]/a/b/text()"),"")
        abstract = self.setValue(response.xpath("//div[@id='content']/div[1]/div[4]/text()"),"")
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["知网"]=True
        paper["step"]=str(paper["step"])
        self.feng3.updataPaperById(paper)

    def wanfang2(self, response):
        paper = response.meta['paper']
        abstract = self.setValue(response.xpath("//div[@class='abstracts']/p/text()"), "")
        org = self.setValue(response.xpath("//div[@class='table-tr Source']/div/a[1]/text()"), "")
        list = []
        nodes = response.xpath("//div[@class='table-tr 主题词']/span/a/text")
        for n in nodes:
            key = self.setValue(n.xpath('./text()'))
            if key not in list:
                list.append(key)
        if len(",".join(list))> paper["keyword"]:
            paper["keyword"] = ",".join(list)
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"] = 2

        # paper["step"]["万方"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def wanfang1(self, response):
        paper = response.meta['paper']
        abstract = self.setValue(response.xpath("//input[@class='share_summary']/@value"),"")
        org = self.setValue(response.xpath("//div[@class='crumbs']/a[3]/text()"),"")
        list=[]
        nodes=response.xpath("//div[@class='info_right info_right_newline']/a")
        for n in nodes:
            key=self.setValue(n.xpath('./text()'))
            if key not in list:
                list.append(key)
        if len(",".join(list))> paper["keyword"]:
            paper["keyword"] = ",".join(list)
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["万方"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def weipu(self, response):
        paper = response.meta['paper']
        abstract = self.setValue(response.xpath("//div[@class='sum']/text()"),"",1)
        org = self.setValue(response.xpath("//span[@class='detailtitle']/strong/i/a/text()"),"")
        list=[]
        nodes=response.xpath("//table[@class='datainfo f14']/tr[2]/td/a")
        for n in nodes:
            key=self.setValue(n.xpath('./text()'))
            if key not in list:
                list.append(key)
        if len(",".join(list))> paper["keyword"]:
            paper["keyword"] = ",".join(list)
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["维普"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def ResearchGate(self, response):
        paper = response.meta['paper']
        abstract = self.setValue(response.xpath("//div[@class='nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-auto nova-e-text--color-inherit']/text()"),"")
        org = self.setValue(response.xpath("//span[@class='publication-meta-journal']/a/text()"),"")
        if len(org)==0:
            org = self.setValue(response.xpath("//div[@class='publication-meta-secondary']/span/text()"), "")
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["ResearchGate"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def Elsevier(self, response):
        print(response.url)
        print(response.body)
        paper = response.meta['paper']
        node=response.xpath("//div[@class='abstract author']/div/p")
        if len(node)>0:
            abstract =node.xpath("string(.)")
        else:
            abstract=""
        org = self.setValue(response.xpath("//a[@class='publication-title-link']/text()"),"")
        list=[]
        nodes=response.xpath("//div[@class='keyword']/span")
        for n in nodes:
            key=self.setValue(n.xpath('./text()'))
            if key not in list:
                list.append(key)
        if len(",".join(list))> paper["keyword"]:
            paper["keyword"] = ",".join(list)
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["Elsevier"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def Springer(self, response):
        paper = response.meta['paper']
        org = self.setValue(response.xpath("//span[@class='JournalTitle']/text()"),"")
        if len(org)==0:
            org = self.setValue(response.xpath("//div[@class='BookTitle']/text()"), "")
        abstractN = response.xpath("//p[@class='Para']")
        abstract=abstractN.xpath("string(*)")
        list=[]
        nodes=response.xpath("//span[@class='Keyword']")
        for n in nodes:
            key=self.setValue(n.xpath('./text()'))
            if key not in list:
                list.append(key)
        if len(",".join(list))> paper["keyword"]:
            paper["keyword"] = ",".join(list)
        if len(abstract)>paper["abstract"]:
            paper["abstract"] = abstract
        if len(org)>paper["org"] :
            paper["org"] = org
        paper["search"]=2
        # paper["step"]["Springer"]=True
        paper["step"] = str(paper["step"])
        self.feng3.updataPaperById(paper)
    def qs(self,url):
        parseResult = parse.urlparse(url)
        param_dict = parse.parse_qs(parseResult.query)
        return param_dict

    def setValue(self, node, value=None, index=0):
        if len(node):
            return node.extract()[index].strip()
        else:
            return value







