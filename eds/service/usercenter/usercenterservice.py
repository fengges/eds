
from eds.config import environment
from eds.dao.usercenter.usercenterdao import usercenterDao

class UserService:
    def get_login_record(self,params):
        datalist=usercenterDao.get_Record(params)
        resultlist = []
        for data in datalist:
            dir = {}
            dir['type'] = data['type']
            dir['time'] = data['time']


            dir['location'] = '等待更新' if data['location'] is None else data['location']
            dir['ip'] = data['ip']
            resultlist.append(dir)
        return resultlist
    def re_password(self,params):
        usercenterDao.update_password(params)
userService=UserService()

