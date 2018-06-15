
#  author   ：feng
#  time     ：2018/6/13
#  function : 统计


from eds.dao.base import dbs
class TaskDao:
    def delRecord(self):
        sql="delete FROM statistics where TO_DAYS(date) = TO_DAYS(NOW())-1 "
        dbs.exe_sql(sql)
    def getRecord(self):
        sql="SELECT count(*) as num,type,value FROM `records` where TO_DAYS(time) = TO_DAYS(NOW())-1 GROUP BY type,value "
        re= dbs.getDics(sql)
        return re
    def insertItem(self,item):
        dbs.insertItem(item)
    def selectByTypeAndDate(self,param):
        sql="select value,sum(num) as sum from statistics where type=%s and date between %s and %s GROUP BY value";
        params=(param["type"],param['startDate'],param['endDate'])
        r=dbs.getDics(sql,params)
        return r
    def selectByTypeAndDateAndValue(self,param):
        sql = "select * from statistics where type=%s and value=%s and date between %s and %s  order BY date";
        params = (param["type"],param['value'], param['startDate'], param['endDate'])
        r = dbs.getDics(sql, params)
        return r
    def selectByTypeAndDateOrderByDate(self,param):
        sql="select * from statistics where type=%s and date between %s and %s order BY date";
        params=(param["type"],param['startDate'],param['endDate'])
        r=dbs.getDics(sql,params)
        return r

taskDao=TaskDao()

