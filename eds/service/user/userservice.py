
from eds.config import environment
from eds.dao.user.userdao import UserDao

class UserService:

    def get_info(self,params):
        result=UserDao.getUserInfo(params)
        return result

userService=UserService()

