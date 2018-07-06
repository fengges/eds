from spider.paperspider.papers.papers.dbutils import dbs


class PaperService:
    def get_search_list(self):
        sql = "select * from teacher_searchlist_copy_copy where searched=0 or searched=1"
        info_list = dbs.getDics(sql)
        return info_list

    def abstract_search_list_from_paper(self, s, e):
        sql = "select _id, name, abstract, keyword, author, url from paper_new where _id>=%d and _id<%d"
        info_list = dbs.getDics(sql % (s, e))
        return info_list

    # 需要重新获取机构的链接
    def institution_search_list_from_paper(self):
        sql = "select _id, author, url from paper_search_list_copy where searched=0"
        info_list = dbs.getDics(sql)
        return info_list

    # 需要重新获取机构的链接
    def update_paper_search_list(self, params):
        sql = "update paper_search_list_copy set searched=1 where _id=%s"
        r = dbs.exe_sql(sql % params)
        return r

    def update_searched(self, params):
        sql = "update teacher_searchlist_copy_copy set searched=%s where id=%s"
        dbs.exe_sql(sql, params)

    def update_searching(self, params):
        sql = "update teacher_searchlist_copy_copy set searching = searching + 1 where id=%s"
        dbs.exe_sql(sql, params)

    def update_error(self, params):
        sql = "update teacher_searchlist_copy_copy set error=1 where id=%s"
        dbs.exe_sql(sql, params)


paper_service = PaperService()
