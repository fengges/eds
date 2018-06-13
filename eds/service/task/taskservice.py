#  author   ：feng
#  time     ：2018/6/13
#  function : 定时服务

import datetime
from eds.dao.task.taskdao import taskDao


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


taskService=TaskService()
