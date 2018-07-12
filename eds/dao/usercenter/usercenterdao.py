
from eds.dao.base import dbs


class UsercenterDao:
    def get_Record(self, params):
        sql = "SELECT * FROM `records` WHERE user=%s AND type='登陆' ORDER BY time DESC LIMIT 0,5"
        info_result = dbs.getDics(sql,params)
        return info_result
    def update_password(self,params):
        sql = "UPDATE user SET `password`=%s WHERE account=%s"
        dbs.exe_sql(sql,params)
usercenterDao=UsercenterDao()
