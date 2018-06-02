
from eds.dao.base import dbs


class ExpertDao:

    def get_radar(self, params):
        sql = "SELECT * FROM radar where author_id=%s"
        radar_result = dbs.getDics(sql, params)
        return radar_result[0]
    def get_info(self, params):
        sql = "SELECT * FROM teacher where id=%s"
        info_result = dbs.getDics(sql, params)
        return info_result

    def get_theme(self, params):
        # 从计算后的theme_year_new表中获取数据
        sql_0 = "select year, theme, paper_num from theme_year_new where author_id=%s"
        sql_2 = "SELECT DISTINCT theme " \
                "FROM theme_year " \
                "WHERE author_id=%s"
        data_result = dbs.getDics(sql_0, params)
        theme_result = dbs.getDics(sql_2, params)
        return theme_result, data_result

    def get_ego(self, params):
        sql = "SELECT * FROM ego_network where author_id=%s order by w desc limit 0,50"
        ego_result = dbs.getDics(sql, params)
        return ego_result

expertDao=ExpertDao()