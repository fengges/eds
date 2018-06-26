
from eds.config import pic_url
from eds.dao.index.indexdao import index_dao


class IndexService:

    def get_school_info(self, params):
        result = index_dao.get_school_info(params)
        return result

indexService = IndexService()
