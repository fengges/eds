#  author   ：feng
#  time     ：2018/6/13
#  function : 定时服务

import datetime
from eds.dao.task.taskdao import taskDao
from eds.service.expert.expertservice import expertService
from eds.service.login.loginservice import userService
class TaskService:
    def statistics(self):
        taskDao.delRecord()
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        temp=taskDao.getRecord()
        for t in temp:
            t["date"]=yesterday
            item={}
            item["table"]="statistics"
            item["params"]=t
            taskDao.insertItem(item)
    def getSearch(self,params):
        temp=taskDao.selectByTypeAndDate(params)
        data={}
        if params["type"]=="专家":
            data["xAxis"]=[self.getExperName(t["value"]) for t in temp]
        elif params["type"]=="登陆" or params["type"]=="注册":
            data["xAxis"] = [self.getUserName(t["value"]) for t in temp]
        else:
            data["xAxis"] = [t["value"] for t in temp]
        data["data"]=[t["sum"] for t in temp]
        data["markPoint"]=[{"xAxis":10, "y": 350, "name":t["value"], "symbolSize":20} for t in temp]
        return data
    def getExperName(self,id):
        return expertService.get_info(id)[0]["name"]
    def getUserName(self,id):
        return userService.getUserByAccount(id)[0]["username"]
taskService=TaskService()
