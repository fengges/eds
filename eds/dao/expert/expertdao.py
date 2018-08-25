
from eds.dao.base import dbs


class ExpertDao:
    def get_infosByIds(self, params):
        sql = "SELECT * FROM teacher where id in "+params
        info_result = dbs.getDics(sql)
        return info_result
    def get_info(self, params):
        sql = "SELECT * FROM teacher where id=%s"
        info_result = dbs.getDics(sql, params)
        return info_result

    def get_theme(self, params):
        # 从计算后的theme_year_new表中获取数据
        sql_0 = "select * from theme_year_cr where author_id=%s"
        sql_2 = "SELECT theme FROM `theme_year_cr` WHERE author_id=%s GROUP BY theme"
        data_result = dbs.getDics(sql_0, params)
        themelist = dbs.getDics(sql_2, params)
        return data_result,themelist

    def get_paper(self, params):
        sql = "SELECT `name`,author,org,`year`,cited_num,abstract FROM `paper_expertpage` WHERE author_id=%s;"
        info_result = dbs.getDics(sql, params)
        return info_result

    def get_single_axis(self, params):
        # 从计算后的theme_year_new表中获取数据
        sql_0 = "select * from theme_single_axis where author_id=%s"
        data_result = dbs.getDics(sql_0, params)
        return data_result

    def get_topics(self, params):
        # 画词云用
        sql_0 = "select topics from teacher where id=%s"
        data_result = dbs.getDics(sql_0, params)
        return data_result

    def get_paperbar(self, params):
        # 画历年成果数用
        sql_0 = "select * from paper_bar where id=%s"
        data_result = dbs.getDics(sql_0, params)
        return data_result

expertDao=ExpertDao()