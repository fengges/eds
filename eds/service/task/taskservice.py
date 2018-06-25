#  author   ：feng
#  time     ：2018/6/13
#  function : 定时服务

import datetime
from eds.dao.task.taskdao import taskDao
from eds.service.expert.expertservice import expertService
from eds.service.login.loginservice import userService
class TaskService:
    def __init__(self):
        self.value=["登陆","注册","留言"]
    def statistics(self):
        taskDao.delRecord()
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        temp=taskDao.getRecord()

        valueTemp={}
        for v in self.value:
            item={}
            item["date"]=yesterday
            item["value"]=v
            item["num"]=0
            item["type"]=v
            valueTemp[v]=item
        for t in temp:
            if t["type"] in self.value:
                valueTemp[t["type"]]["num"]+=t["num"]
                continue
            t["date"]=yesterday
            item={}
            item["table"]="statistics"
            item["params"]=t
            taskDao.insertItem(item)
        for v in valueTemp:
            item = {}
            item["table"] = "statistics"
            item["params"] = valueTemp[v]
            taskDao.insertItem(item)
    def getSearchByValue(self,params):
        temp =taskDao.selectByTypeAndDateAndValue(params)
        data = {}
        data["legend"] = [params['value']]
        data["xAxis"] = [t["date"].strftime("%Y-%m-%d") for t in temp]
        data["series"] = [{'name': params["type"], 'type': 'line', 'smooth': True,
                           'itemStyle': {'normal': {'areaStyle': {'type': 'default'}}},
                           'data': [t["num"] for t in temp]}]
        return data
    def getSearch(self,params):
        if params['value'] is not None:
            return self.getSearchByValue(params)
        if params["type"] in self.value:
            temp =taskDao.selectByTypeAndDateOrderByDate(params)
        else:
            temp = taskDao.selectByTypeAndDate(params)
        data={}
        if params["type"]=="专家":
            ids=[t["value"] for t in temp]
            expers=self.getExpers(ids)
            data["xAxis"]=[expers[t['value']]['name'] for t in temp]
            data["data"] = [int(t["sum"]) for t in temp]
            data['value']=[{"value":t['value'],"label":expers[t['value']]['name']} for t in temp]
        elif params["type"] in self.value:
            data["legend"]=[params["type"]]
            data["xAxis"] = [t["date"].strftime("%Y-%m-%d") for t in temp]
            data["series"]=[{'name':params["type"],'type': 'line','smooth': True,'itemStyle': {'normal': {'areaStyle': {'type': 'default'}}},'data': [ t["num"]for t in temp ] }]
        else:
            data["xAxis"] = [t["value"] for t in temp]
            data["data"]=[int(t["sum"]) for t in temp]
            data['value'] = [{"value": t['value'], "label": t['value']} for t in temp]

        return data


    def getExpers(self,ids):
        return expertService.get_infosByIds(ids)

taskService=TaskService()
