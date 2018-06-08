
#  author   ：feng
#  time     ：2018/1/25
#  function : 用户服务

from eds.error import *
from eds.dao.login.userdao import userDao

class UserService:
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