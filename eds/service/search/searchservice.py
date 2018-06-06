#  author   ：feng
#  time     ：2018/2/28
#  function : 搜索服务

from collections import Counter
from werkzeug.contrib.cache import SimpleCache
from eds.service.search.jiebautil import jeibaUitl
from eds.elastic import  paperSearch


class SearchService:
    #  初始化
    def __init__(self):
        self.cache=SimpleCache()
    #  判断是否有筛选条件
    def findFilter(self,params):
        if len(params["field"]) >0:
            return True
        if len(params["h_index"]) > 0:
            return True
    #  找到搜索缓存的记录
    def getKey(self,params):
        key = ['keyword', 'name', 'institution']
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
        value=self.cache.get('filter')
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
            r["link"]="/main/profile/"+str(r["author_id"])
        # re['result']=temp['result']
        re['result']=self.setLight(temp['result'],params['keyword'])
        if len(re['result'])>0 and "light_abstract" not in re['result'][0].keys():
            for r in re['result']:
                r['light_abstract']=r['abstract']
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
            r["link"] = "/main/profile/" + str(r["author_id"])

        return temp

searchService=SearchService()