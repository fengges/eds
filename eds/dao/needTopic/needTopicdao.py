#  author   ：feng
#  time     ：2018/5/26
#  function ：需求主题
from eds.dao.base import dbs


class NeedTopicDao:
    def getNeedTopicByTopic(self,params):
        params=('%'+params[0]+'%',)
        sql = "SELECT * FROM need_topic where topic like %s"
        radar_result = dbs.getDics(sql, params)
        return radar_result[0]

needTopicDao=NeedTopicDao()