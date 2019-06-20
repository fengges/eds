from spider.paperspider.papers.papers.dbutils import dbs


class TermService:
    def get_search_list(self, params):
        sql = "SELECT * FROM paper_data WHERE discipline=%s AND term_%s IS NULL LIMIT 100000" % params
        info_list = dbs.getDics(sql)
        return info_list


term_service = TermService()
