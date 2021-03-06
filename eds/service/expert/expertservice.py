
import math
import json
from eds.config import environment
from eds.dao.expert.expertdao import expertDao

class ExpertService:

    def get_info(self,params):
        out = {}
        data=expertDao.get_info(params)[0]
        name = data['name']
        title = self.getValue(data['title'])
        school = self.getValue(data['school'])
        institution = self.getValue(data['institution'])
        eduexp = self.getValue(data['eduexp'])
        if eduexp:eduexp = eduexp.split('\n')
        email = self.getValue(data['email'])
        homepage = self.getValue(data['homepage'])
        age = self.getValue(data['age'])
        fields = self.getValue(data['fields'])
        if fields !='':fields = ','.join(list(eval(fields).keys())[:5])
        out['id'] = params
        out['name'] = name
        out['title'] = title
        out['school'] = school
        out['institution'] = institution
        out['eduexp'] = eduexp
        out['email'] = email
        out['homepage'] = homepage
        out['age'] = age
        out['fields'] = fields
        return out

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

        themedata,themelistdata=expertDao.get_single_axis(params)
        theme_year = []
        for node in themedata:
            theme_year.append([node['year'],node['num'],node['theme']])

        themelist = []
        for node in themelistdata:
            themelist.append(node['theme'])
        result = {'theme_year':theme_year,'themelist':themelist}
        return result


    def get_single_axis(self,params):

        data = expertDao.get_single_axis(params)
        years = []
        themes = []
        numlist = []
        if len(data)>0:
            #初始化years数据
            minyear = int(data[0]['minyear'])
            maxyear = int(data[0]['maxyear'])
            for i in range(minyear,maxyear+1):
                years.append(i)
            #初始化themes数据
            themes = data[0]['themelist'].split('-link-')
            #初始化numlist数据
            for i in range(len(themes)):
                for j in range(len(years)):
                    numlist.append([i,j,0])
            #根据实际数据修改numlist
            for node in data:
                theme = node['theme']
                i = themes.index(theme)
                j = int(node['year'])-minyear
                x = i*(maxyear-minyear+1)+j
                numlist[x][2]+=1
        result = {'themes':themes,'years':years,'data':numlist}
        return result

    def get_topics(self,params):
        data = expertDao.get_topics(params)
        if len(data[0]['topics']) == 0:return ''
        topics = eval(data[0]['topics'])

        out = []

        for k,v in topics.items():
            out.append({'name':k,'value':v})
        return out

    def get_paperbar(self,params):
        data = expertDao.get_paperbar(params)[0]
        x = data['x'].strip(',').split(',')
        y = [int(i) for i in data['y'].strip(',').split(',')]
        maxy = max(y)
        out = {'x':x,'y':y,'maxy':maxy}
        return out

    def get_pic(self,id):
        try:
            image = open(environment['file']["pic_url"]+'ProfileImgs/'+str(id)+'.jpg','rb')
        except:
            image = open(environment['file']["pic_url"]+ 'ProfileImgs/demo.jpg', 'rb')
        return image

    def getValue(self,v):
        return v if v is not None else ''
expertService=ExpertService()