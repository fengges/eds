#  author   ：feng
#  time     ：2018/2/28
#  function : 搜索服务


from eds.dao.needTopic.needTopicdao import  needTopicDao


class NeedTopicService:

    #  判断是否有筛选条件
    def getNeedTopicByTopic(self,topic):
        return needTopicDao.getNeedTopicByTopic((topic,))

needTopicService=NeedTopicService()

