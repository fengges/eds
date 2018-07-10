from spider.paperspider.papers.papers.dbutils import dbs
from spider.paperspider.papers.papers.settings import PC_NO, PC_COUNT

class PaperService:
    def get_search_list(self):
        sql = "select * from teacher_searchlist_copy_copy where searched=0 or searched=1"
        info_list = dbs.getDics(sql)
        return info_list

    # 需要重新获取机构的链接
    def institution_search_list_from_paper(self):
        sql = "select _id, author, url from paper_90_search_list where searched=0 and MOD(_id, %s)=%s" % (PC_COUNT, PC_NO)
        info_list = dbs.getDics(sql)
        return info_list

    # 需要重新获取机构的链接
    def update_paper_search_list(self, params):
        sql = "update paper_90_search_list set searched=1 where _id=%s"
        r = dbs.exe_sql(sql % params)
        return r

    # 需要重新获取abstract、org、name的链接
    def abstract_search_list_select(self):
        sql = "select * from paper_searchlist_1 where searched=0 and _id < 1000"
        info_list = dbs.getDics(sql)
        return info_list

    # 需要重新获取abstract、org、name的链接
    def abstract_search_list_update(self, params):
        sql = "update paper_searchlist_1 set searched=1 where _id=%s"
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
