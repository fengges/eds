
#  author   ：feng
#  time     ：2018/1/25
#  function : 用户查询
from eds.dao.base import dbs
class UserDao:
    def getUsers(self,params):
        sql_num = 'SELECT count(*) as num from (select a.account,a.username,b.lastlogin from user a left join (SELECT value,max(time) as lastlogin FROM `records` where type="登陆" GROUP BY value) b on a.account=b.value) c join (SELECT value,time  FROM `records` where type="注册" ) d on c.account=d.value'
        sql = 'SELECT c.*,d.time as register from (select a.account,a.username,b.lastlogin from user a left join (SELECT value,max(time) as lastlogin FROM `records` where type="登陆" GROUP BY value) b on a.account=b.value) c join (SELECT value,time  FROM `records` where type="注册" ) d on c.account=d.value limit %s,%s'
        param=(params['pPageNum']*(params['page']-1),params['pPageNum'])
        s=dbs.getDics(sql,param)
        n = dbs.getDics(sql_num)
        return {"result":s,"num":n[0]["num"]}
    def getUserByAccount(self,params):
        sql = "SELECT * FROM user where account=%s"
        s=dbs.getDics(sql,params)
        return s
    def addUser(self,params):
        sql = "INSERT INTO user VALUE(NULL,%s,%s,%s,%s,%s)"
        dbs.exe_sql(sql,params)

userDao=UserDao()