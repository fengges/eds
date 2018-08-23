#  author   ：feng
#  time     ：2018/2/28
#  function : 搜索服务
import requests,json
from collections import Counter
from werkzeug.contrib.cache import SimpleCache
from eds.service.search.jiebautil import jeibaUitl
from eds.elastic import  paperSearch
from eds.service.task.taskservice import taskService
from eds.service.expert.expertservice import expertService
from eds.config import environment
from eds.service.school.schoolservice import schoolService
class SearchService:
    #  初始化
    def __init__(self):
        self.cache=SimpleCache()
    #  判断是否有筛选条件
    def findFilter(self,params):
        if len(params["school"])>0:
            return True
        if len(params["field"]) >0:
            return True
        if len(params["h_index"]) > 0:
            return True
    def findFilter2(self,params):
        if "school"in params and len(params["school"])>0:
            return True
        if "code"in params and len(params["code"]) >0:
            return True
        if "name"in params and len(params["name"]) >0:
            return True
        return False
    #  找到搜索缓存的记录
    def getKey2(self,params):
        key = ['keyword']
        p={}
        for k in key:
            p[k]=params[k]
        return str(p)
    def getKey(self,params):
        key = ['keyword', 'name']
        p={}
        for k in key:
            p[k]=params[k]
        return str(p)
    # 得到查询结果
    def getSearchResult(self,params):
        re={}
        key=params['keyword']
        temp=jeibaUitl.cut(params['keyword'])
        if len(temp)==0:
            if len(key)==0:
                params['keyword']=[]
            else:
                temp=[key]
                params['keyword']=temp
        else:
            params['keyword'] = temp
        temp=paperSearch.searchdao(params)
        re['num'] = temp["num"]
        key = self.getKey(params)
        if not self.findFilter(params):
            re['filter'] = self.getfilter(temp["filter"])
            self.cache.set(key, re['filter'], timeout=5 * 60*60)
        else:
            value=self.cache.get(key)
            if value is None:
                re['filter'] = self.getfilter(temp["filter"])
                self.cache.set(key, re['filter'], timeout=5 * 60 * 60)
            else:
                re['filter']=value
        re['allPage']=int(re['num']/params['pPageNum'])
        if re['num']%params['pPageNum']!=0:
            re['allPage']+=1
        re['params']=params
        for r in temp['result']:
            r["link"]="/main/expert/"+str(r["author_id"])
        # re['result']=temp['result']
        re['result']=self.setLight(temp['result'],params['keyword'])
        if len(re['result'])>0 and "light_abstract" not in re['result'][0].keys():
            for r in re['result']:
                r['light_abstract']=r['abstract']
        return re
    def getSearchResult2(self,params):
        re={}
        requrl ="http://"+ environment['se']["host"] + ":" + str(environment['se']["port"])+ environment['se']["url"]
        s = json.dumps(params)
        r = requests.post(requrl, data=s)
        res =r.text
        res=eval(res)
        t_id=[str(r[0]) for code in res for r in res[code]]
        if len(t_id)==0:
            teacher={}
        else:
            teacher=expertService.get_infosByIds(t_id)
        key = self.getKey2(params)
        if not self.findFilter2(params['filer']):
            re['filter'] = self.getfilter2(res,teacher)
            self.cache.set(key, re['filter'], timeout=5 * 60*60)
        else:
            value=self.cache.get(key)
            if value is None:
                re['filter'] = self.getfilter2(res,teacher)
                self.cache.set(key, re['filter'], timeout=5 * 60 * 60)
            else:
                re['filter']=value
        re['params']=params
        temp=[]
        for code in res:
            temp.extend(res[code])
        sortrk = sorted(temp, key=lambda item: item[1], reverse=True)
        re['result']=[teacher[str(t[0])]for t in sortrk]
        re["num"]=len(re['result'])
        return re
    # 对查询的结果显示不同的样式
    def setLight(self,result,keys):
        for r in result:
            for k in keys:
                r['abstract']=r['abstract'].replace(k,"<span class='light'>"+k+"</span>")

        return result
    # 对查询的结构生成筛选条件和数量
    def getfilter(self, result):
        f = {}
        f['hindexs']={}
        f['hindexs']['>30']=0
        f['hindexs']['20-29'] = 0
        f['hindexs']['10-19'] = 0
        f['hindexs']['<10'] = 0
        f['fields']=[]
        f['schools'] = []
        field=[]
        schools = []
        for r in result:
            if r['h_index']>=30 :
                f['hindexs']['>30']+=1
            elif r['h_index']>=20:
                f['hindexs']['20-29'] += 1
            elif r['h_index'] >= 10:
                f['hindexs']['10-19'] += 1
            else :
                f['hindexs']['<10'] += 1
            field.extend(r['fields'])
            schools.append(r['school'])
        temp=[]
        temp.append({'value':">30",'num':f['hindexs']['>30']})
        temp.append({'value': "20-29", 'num': f['hindexs']['20-29']})
        temp.append({'value': "10-19", 'num': f['hindexs']['10-19']})
        temp.append({'value': "<10", 'num': f['hindexs']['<10']})
        f['hindexs']=temp
        c2 = Counter(field).items()
        c1=sorted(c2, key=lambda x: x[1], reverse=True)
        if len(c1)-5>=0:
            n=5
        else:
            n=len(c1)
        for i in range(n):
            f['fields'].append({'value':c1[i][0],'num':c1[i][1]})

        c3 = Counter(schools).items()
        c0=sorted(c3, key=lambda x: x[1], reverse=True)
        if len(c0)-5>=0:
            n=5
        else:
            n=len(c0)
        for i in range(n):
            f['schools'].append({'value':c0[i][0],'num':c0[i][1]})
        return f
        # 得到查询结果
    # 对查询的结构生成筛选条件和数量
    def getfilter2(self, result,teacher):
        f={}
        f["codes"]=[]
        f["schools"] = []
        codes={}
        schools={}
        for code in result:
            codes[code]=len(result[code])
            for t in result[code]:
                school_id=teacher[str(t[0])]["school_id"]
                if  school_id in schools:
                    schools[school_id]+=1
                else:
                    schools[school_id]= 1
        if 0 in schools:
            del schools[0]
        school_id=[str(id) for id in schools]
        if len(school_id)==0:
            s={}
        else:
            s=schoolService.get_infosByIds(school_id)
        code_id=[c for c in codes]
        if len(code_id)==0:
            c={}
        else:
            c = schoolService.get_infosByCodes(code_id)

        c2 = Counter(codes).items()
        c1=sorted(c2, key=lambda x: x[1], reverse=True)
        if len(c1)-5>=0:
            n=5
        else:
            n=len(c1)
        for i in range(n):
            f['codes'].append({'value':c1[i][0],'num':c1[i][1],"name":c[c1[i][0]]["name"]})
        c2 = Counter(schools).items()
        c1=sorted(c2, key=lambda x: x[1], reverse=True)
        if len(c1)-5>=0:
            n=5
        else:
            n=len(c1)
        for i in range(n):
            f['schools'].append({'value':c1[i][0],'num':c1[i][1],"name":s[str(c1[i][0])]["name"]})
        return f
        # 得到查询结果
    def getIndexSearchResult(self, params):

        key = params['keyword']
        temp = jeibaUitl.cut(params['keyword'])
        if len(temp) == 0:
            if len(key) == 0:
                params['keyword'] = []
            else:
                temp = [key]
                params['keyword'] = temp
        else:
            params['keyword'] = temp
        temp = paperSearch.IndexSearchdao(params)

        for r in temp['result']:
            r["link"] = "/main/expert/" + str(r["author_id"])

        return temp
    def getHotSearch(self,params):
        if params["type"] is None:
            return []
        r=taskService.getHotSearch(params)
        if params["type"]=="专家":
            ids = [t["value"] for t in r]
            expers=expertService.get_infosByIds(ids)
            result=[{"name":expers[t['value']]["name"],"url":"/main/expert/"+t["value"]} for t in r]
            return result
        else:
            result = [{"name":t["value"] , "url": "/main/school/" + t["value"]} for t in r]
            return result


searchService=SearchService()