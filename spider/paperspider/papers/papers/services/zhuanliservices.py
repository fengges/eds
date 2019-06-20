from spider.paperspider.papers.papers.dbutils import dbs


class ZhuanliService:
    def get_search_list(self):
        sql = "select * from zhuanli_search where status = '0' OR status = '-2' OR status = '2'"
        info_list = dbs.getDics(sql)
        return info_list

    #
    def update_search_list_all(self, params):
        sql = "update zhuanli_search set status='1' where id=%s"
        r = dbs.exe_sql(sql % params)
        return r

    #
    def update_search_list_none(self, params):
        sql = "update zhuanli_search set status='-1' where id=%s and status='0'"
        r = dbs.exe_sql(sql % params)
        return r

    #
    def update_search_list_ing(self, params):
        sql = "update zhuanli_search set status='2' where id=%s"
        r = dbs.exe_sql(sql % params)
        return r

    #
    def update_search_list_error(self, params):
        sql = "update zhuanli_search set status='-2' where id=%s"
        r = dbs.exe_sql(sql % params)
        return r


zhuanli_service = ZhuanliService()

