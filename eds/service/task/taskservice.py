#  author   ：feng
#  time     ：2018/6/13
#  function : 定时服务

import datetime
from eds.dao.task.taskdao import taskDao
from eds.service.expert.expertservice import expertService
from eds.service.login.loginservice import userService
class TaskService:
    def __init__(self):
        self.value=["登陆","注册"]
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

    def getSearch(self,params):
        if params["type"] in self.value:
            temp =taskDao.selectByTypeAndDateOrderByDate(params)
        else:
            temp = taskDao.selectByTypeAndDate(params)
        data={}
        if params["type"]=="专家":
            data["xAxis"]=[self.getExperName(t["value"]) for t in temp]
            data["data"] = [t["sum"] for t in temp]
        elif params["type"]=="登陆" or params["type"]=="注册":
            data["legend"]=[params["type"]]
            data["xAxis"] = [t["date"].strftime("%Y-%m-%d") for t in temp]
            data["series"]=[{'name':params["type"],'type': 'line','smooth': True,'itemStyle': {'normal': {'areaStyle': {'type': 'default'}}},'data': [ t["num"]for t in temp ] }]
        else:
            data["xAxis"] = [t["value"] for t in temp]
            data["data"]=[t["sum"] for t in temp]

        return data


    def getExperName(self,id):
        return expertService.get_info(id)[0]["name"]

taskService=TaskService()
