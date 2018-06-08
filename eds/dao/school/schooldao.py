
from eds.dao.base import dbs


class SchoolDao:
    def get_info(self, params):
        if params.isdigit():
            sql = "SELECT * FROM school_info where id=%s"
        else:
            sql = "SELECT * FROM school_info where name=%s"
        info_result = dbs.getDics(sql, params)
        return info_result

    def get_teacher(self, params):

        if params is list:
            params = str(params)
            sql = "select id, name, fields, title, institution, pic from teacher where (name, school) in %s"
        else:
            sql = "select id, name, fields, title, institution, pic from teacher where school = %s limit 6"
        data_result = dbs.getDics(sql, params)
        return data_result


school_dao = SchoolDao()
