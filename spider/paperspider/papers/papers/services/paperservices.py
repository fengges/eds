from papers.dbutils import dbs


class PaperService:
    def get_search_list(self):
        sql = "select * from teacher_searchlist_copy where searching=0 and searched=0"
        info_list = dbs.getDics(sql)
        return info_list

    def update_searched(self, params):
        sql = "update teacher_searchlist_copy set searched=%s where id=%s"
        dbs.exe_sql(sql, params)

    def update_searching(self, params):
        sql = "update teacher_searchlist_copy set searching = searching + 1 where id=%s"
        dbs.exe_sql(sql, params)

    def update_error(self, params):
        sql = "update teacher_searchlist_copy set error=1 where id=%s"
        dbs.exe_sql(sql, params)


paper_service = PaperService()
