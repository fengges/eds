from eds.dao.base import dbs


class PlatformDao:
    def get_infosByIds(self, params):
        sql = "SELECT * FROM platform where id = "+str(params)
        info_result = dbs.getDics(sql)
        return info_result

platformDao=PlatformDao()