
#  author   ：feng
#  time     ：2018/1/25
#  function : 用户服务
import time
from eds.error import *
from eds.dao.login.userdao import userDao

class UserService:
    def getUsers(self,params):
        result=userDao.getUsers(params)
        for r in result["result"]:
            if r["register"]:
                r["register"]=r["register"].strftime("%Y-%m-%d %H:%M:%S")
            if r["lastlogin"]:
                r["lastlogin"]=r["lastlogin"].strftime("%Y-%m-%d %H:%M:%S")
        return result
    def getUser(self,params):
        if len(params)==1:
            if params[0]:
                s=userDao.getUserByAccount(params)
            else :
                raise MyError(602)
        else:
            raise MyError(601)
        if len(s)==0:
            return None
        else:
            return s[0]
    def getUserByAccount(self,Account):
        params=(Account,)
        s=userDao.getUserByAccount(params)
        return s
    def addUser(self,params):
        if len(params)==3:
            if params[0]:
                if params[1]:
                    s=userDao.addUser(params)
                else :
                    raise MyError(603)
            else :
                raise MyError(602)
        else:
            raise MyError(601)

userService=UserService()