
#  author   ：feng
#  time     ：2018/3/14
#  function : 搜索dao
from datetime import datetime
from elasticsearch import Elasticsearch

class PaperSearch:
    # 初始化
    def __init__(self):
        self.es = Elasticsearch([{"host": "120.78.201.159", "port": 9200}])
        # self.es = Elasticsearch()
    # 生成过滤条件的返回字段
    def IndexSearchdao(self,params):
        result = {}
        dic = self.getType()
        dic["query"]["bool"]["must"] = self.getQuery(params)
        dic["size"] = 5
        dic["from"] = 0
        dic = self.setResultSource(dic)
        result["result"],result["num"] = self.dosearch2(dic)

        return result
    def setFilterSource(self,dic):
        dic["_source"]["include"] = ["h_index", "fields"]
        return dic
    #  通用字段
    def getType(self):
        dic={}
        dic["_source"]={}
        dic["query"]={}
        dic["query"]["bool"] = {}
        dic["collapse"]= { "field": "author_id"}
        return dic
    # 设置排序
    def setOrder(self,dic,param):
        if param["order"] is None or len(param["order"]) == 0:
            pass
        else :
            dic["sort"]= [{param["order"]: {"order": "desc"}}]
        return dic
    # 设置搜索结果的返回字段
    def setResultSource(self,dic):
        dic["_source"]["include"] = ["author_id","name","school","institution","h_index","paper_num","citation","fields","abstract","title"]
        return dic
    # 生成 查询结构
    def getQuery(self,params):
        dic=[]
        for k in params:
            if params[k] is None:
                params[k]=''
        if len(params["institution"])>0 :
            dic.append({
                "bool": {
                    "should": [{
                        "match_phrase": {
                            "school":params["institution"]
                        }
                    },
                        {
                            "match_phrase": {
                                "institution": params["institution"]
                            }
                        }
                    ]
                }
            })
        if  len(params["keyword"])>0 :
            if params["accurate_search"]==True:
                print("精确搜索")
                for k in params["keyword"]:
                    dic.append({
                        "match_phrase": {
                            "abstract": k
                        }
                    })
            else:
                print("模糊搜索")
                s = ""
                for k in params["keyword"]:
                    s += k + " AND "
                s = s[0:-5]
                dic.append({
                    "query_string": {
                        "default_operator": "AND",
                        "query":s,
                        "fields": ["abstract"]
                    }
                })
        if  len(params["name"])>0 :
            dic.append({
                "match": {
                    "name": params["name"]
                }
			})
        return dic
    # 设置研究领域
    def setfilter(self,dic,params):
        hindex=self.getIfHindex(params['h_index'])
        if hindex is not None:
            dic["query"]["bool"]["must"].append(hindex)
        if params["field"] is None or len(params["field"]) == 0 or params["field"]=="全部":
            pass
        else :
            dic["query"]["bool"]["must"].append({
                "match": {
                    "fields": {
                        "query":params["field"]
                    }
                }
            })
        return dic
    # 设置h_index条件
    def getIfHindex(self, s):
        if s is None or len(s) == 0 or s=="全部":
            return None;
        dic={}
        dic["range"]={}
        dic["range"]["h_index"]={}
        if s.find('-') >= 0:
            t = s.split('-')
            dic["range"]["h_index"]["gte"]=t[0]
            dic["range"]["h_index"]["lte"] = t[1]
        elif s[0]=='>':
            dic["range"]["h_index"]["gte"]=s[1:]
        else:
            dic["range"]["h_index"]["lte"] = s[1:]
        return dic
    #设置页码
    def setPage(self,dic,params):
        dic["from"]=params['pPageNum']*(params['page']-1)
        dic["size"]=params['pPageNum']
        return dic
    # 请求
    def dosearch2(self,dic):
        print(dic)
        res = self.es.search(index="teachers", body=dic)
        sources=[source["_source"] for source in res['hits']['hits']]
        total=res['hits']['total']
        return sources,total
    def dosearch(self,dic):
        res = self.es.search(index="teachers", body=dic)
        sources=[source["_source"] for source in res['hits']['hits']]
        if len(sources)>0 and "highlight" in res['hits']['hits'][0].keys():
            for i in range(len(sources)):
                s=""
                for a in res['hits']['hits'][i]['highlight']['abstract']:
                    s+=a+" "
                sources[i]["light_abstract"]=s
        return sources
    #  搜索请求
    def searchdao(self,params):
        result={}
        dic=self.getType()
        dic = self.setFilterSource(dic)
        dic["query"]["bool"]["must"] = self.getQuery(params)
        self.setfilter(dic, params)
        dic["size"] =1000000
        print(dic)
        result["filter"] = self.dosearch(dic)
        dic=self.setResultSource(dic)
        self.setPage(dic,params)
        self.setOrder(dic,params)
        dic["highlight"] = {"fields": {"abstract": {}}}

        result["result"]=self.dosearch(dic)
        result["num"]=len(result["filter"])
        return result






