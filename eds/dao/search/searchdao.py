

#  author   ：feng
#  time     ：2018/1/25
#  function : 搜索


import random
import string
from eds.dao.base import dbs
class SearchDao:
    def getSearchResult(self,sql,params):
        re= dbs.getDics(sql)
        return self.getDateSet(re,params)

    def getDateSet(self,result,params):
        list=[]
        field=['数据挖掘','机器学习','社交网络','深度学习','医疗健康','人工智能','数据库','云计算']
        for t in result:
            t['information'] = ran_str = ''.join(
                random.sample(string.ascii_letters + string.digits, random.randint(0, 20)))+'_'+params['keyword']
            t['h_index']= random.randint(0, 100)
            t['link'] = '/main/profile/'+str(t['id'])
            t['Paper'] = random.randint(0, 1000)
            t['Citation'] = random.randint(0, 10000)
            f=[]
            for j in range( random.randint(0, 4)+1):
                f.append(field[random.randint(0, len(field))-1])
            t['fields']=f
            list.append(t)
        return list
searchDao=SearchDao()