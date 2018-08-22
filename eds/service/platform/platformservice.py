
import math
import json
from eds.config import environment
from eds.dao.platform.platformdao import platformDao

class PlatformService:

    def get_info(self,params):
        data=platformDao.get_infosByIds(params)[0]
        result = {}
        name = data['name']
        charge = data['charge']
        introduction = data['introduction']
        infodir = eval(data['infodir'])
        infolist = []
        for k,v in infodir.items():
            infolist.append({'title':k,'content':v})
        result['name'] = name
        result['charge'] = charge
        result['intro'] = introduction

        return result,infolist


platformService=PlatformService()
platformService.get_info('2')
