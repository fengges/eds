
from eds.dao.base import dbs


class IndexDao:
    def get_school_info(self, params):
        sql = "SELECT * FROM school_info where characteristic=%s limit 4"
        info_result = dbs.getDics(sql, params)
        return info_result



index_dao = IndexDao()
