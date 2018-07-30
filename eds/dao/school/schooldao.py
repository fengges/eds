
from eds.dao.base import dbs


class SchoolDao:
    def get_info(self, params):
        if params.isdigit():
            sql = "SELECT * FROM school_info where id=%s"
        else:
            sql = "SELECT * FROM school_info where name=%s"
        info_result = dbs.getDics(sql, params)
        return info_result

    def get_discipline(self, id):
        d_sql = "SELECT xueke1, xueke2, level FROM discipline where school=%s"
        if not id.isdigit():
            sql = "SELECT id FROM school_info where name=%s"
            info_result = dbs.getDics(sql, id)
            if not info_result:
                return None
            id = info_result[0]["id"]
        result = dbs.getDics(d_sql, id)
        return result

    def get_teacher(self, params):

        if params is list:
            params = str(params)
            sql = "select id, name, theme, title, institution, pic from teacher where (name, school) in %s"
        else:
            sql = "select id, name, theme, title, institution, pic from teacher where school = %s limit 6"
        data_result = dbs.getDics(sql, params)
        return data_result


school_dao = SchoolDao()

if __name__ == "__main__":
    school_dao.get_discipline("清华大学")