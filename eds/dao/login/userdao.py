
#  author   ：feng
#  time     ：2018/1/25
#  function : 用户查询
from eds.dao.base import dbs
class UserDao:
    def getUserByAccount(self,params):
        sql = "SELECT * FROM user where account=%s"
        s=dbs.getDics(sql,params)
        return s
    def addUser(self,params):
        sql = "INSERT INTO user VALUE(NULL,%s,%s,%s)"
        dbs.exe_sql(sql,params)

userDao=UserDao()