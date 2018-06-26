
import math
import json
from eds.config import pic_url
from eds.dao.expert.expertdao import expertDao

class ExpertService:

    def get_info(self,params):
        result=expertDao.get_info(params)
        return result
    def get_infosByIds(self,ids):
        params="("+(",".join(ids))+")"
        result=expertDao.get_infosByIds(params)
        r={str(t["id"]):t for t in result}
        return r
    def get_paper(self,params):
        data=expertDao.get_paper(params)
        if len(data)>9:data = data[:10]

        for i in range(len(data)):
            teacherjson = json.loads(data[i]['author'])
            teacherlist = []
            for teacher in teacherjson:
                teacherlist.append(teacher['name'])
            teacherstr = ', '.join(teacherlist)
            data[i]['author'] = teacherstr

        return data

    def get_theme(self,params):

        themedata,themelistdata=expertDao.get_theme(params)
        theme_year = []
        for node in themedata:
            theme_year.append([node['year'],node['num'],node['theme']])

        themelist = []
        for node in themelistdata:
            themelist.append(node['theme'])
        result = {'theme_year':theme_year,'themelist':themelist}

        print(theme_year)
        print(themelist)

        return result


    def get_pic(self,id):
        try:
            image = open(pic_url+'ProfileImgs/'+str(id)+'.jpg','rb')
        except:
            image = open(pic_url + 'ProfileImgs/demo.jpg', 'rb')
        return image
expertService=ExpertService()
# expertService.get_theme(23458)
