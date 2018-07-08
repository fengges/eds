
from eds.dao.school.schooldao import school_dao
from eds.config import environment

class SchoolService:

    def get_info(self, params):
        result = school_dao.get_info(params)
        return result

    def get_teacher(self, params):
        result = school_dao.get_teacher(params)
        return result

    def get_pic(self, params):
        try:
            image = open(environment['file']["pic_url"]+'SchoolImgs/'+str(params)+'.jpg', 'rb')
        except:
            image = open(environment['file']["pic_url"] + 'SchoolImgs/demo.jpg', 'rb')
        return image


schoolService = SchoolService()
