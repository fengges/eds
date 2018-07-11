
from eds.dao.base import dbs


class UserDao:
    def getUserInfo(self,params):
        sql = "SELECT * FROM teacher where id in " + params
        info_result = dbs.getDics(sql)
        return info_result
expertDao=UserDao()