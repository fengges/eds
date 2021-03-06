from eds.controller.sci.db_util import db
import os,re
from pypinyin import lazy_pinyin
class Service:
    def __init__(self):
        self.db=db
        self.root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sql = "select name,english_name from school_info"
        self.file = open(self.root + '/controller/sci/data/school2en_dict.txt', 'r', encoding='utf8').readlines()
        self.school = {s.split(":")[0]: s.split(":")[1].strip() for s in self.file}
        school = self.db.getDics(sql)
        s_sql = "select * from es_school"
        school_id=self.db.getDics(s_sql)
        self.school_id={s['ID']:s["NAME"] for s in school_id }
        for s in school:
            if s['english_name'] and len(s['english_name']) > 0:
                self.school[s['name']] = s['english_name']
        for s in self.school:
            self.school[s]= self.school[s].replace('(',' ').replace(')',' ')
    def updataPage(self,id,page,all_page=None):
        teacher = self.db.getTeacherById(id)[0]
        pages=eval(teacher['page'])
        if all_page and teacher['all_page']==-1:
            teacher['all_page']=int(all_page)
        if page not in pages:
            pages.append(int(page))
        teacher['page']=str(pages)
        if teacher['all_page']==len(pages):
            teacher['search']=2
        param = (teacher['page'], teacher['all_page'],teacher['search'], id)
        sql='update es_teacher set page=%s,all_page=%s,search=%s where id=%s'
        self.db.exe_sql(sql,param)
    def getQuery(self):
        print("find teacher")
        teacher=self.db.getTeacher(0,1)
        if len(teacher)==0:
            return None
        else:
            print("update teacher")
            self.db.updateTeacherById(teacher[0]['id'],1)
            teacher[0]['page']=eval(teacher[0]['page'])
            return {'query':self.getQueryByTeacher(teacher[0]),'teacher':teacher[0]}
    def getQueryByTeacher(self,teacher):
        print("get teacher query")
        name=teacher['name']
        school=self.school_id[teacher['SCHOOL_ID']]
        en_name = self.name2enjianc(name)
        en_shcool = self.school[school]
        value = 'au=' + en_name + ' and oo=' + en_shcool
        print("return  teacher query")
        return value
    def name2enjianc(self,name=""):
        fu_dict = {}.fromkeys(
            open(self.root+'/controller/sci/data/fu.txt', 'r', encoding='utf8').read().split('\n'), "ok")
        name_list = lazy_pinyin(name)
        if len(name) > 2 and fu_dict.get(name[0:2], "") != "":
            return name_list[0] + name_list[1]+ " " +  "".join(name_list[2:])
        else:
            return name_list[0]+ " " + "".join(name_list[1:])
    def initCode(self):

        n=0
        while True:
            print(n)
            sql = "SELECT DISTINCT(a.id) FROM `es_teacher` a join es_institution b on a.INSTITUTION_ID=b.id join es_relation_in_dis c on c.INSTITUTION_ID=b.id where c.DISCIPLINE_CODE like '08%' limit "+str(n)+",1000"
            teacher=self.db.getDics(sql)
            if len(teacher)==0:
                break
            for t in teacher:
                self.db.updateTeacherById(t['id'],0)
            n+=1000

    def searchCheck(self):
        while True:
            teacher = self.db.getTeacher(1, 100)
            if len(teacher) == 0:
                break
            for t in teacher:
                page=set(eval(t['page']))
                if t['all_page']!=len(page):
                    self.db.updateTeacherById(t['id'],0)
                else:
                    self.db.updateTeacherById(t['id'],2)
    def endPaper(self,id):
        self.db.updateTeacherById(id, 2)
    def addPaper(self,item):
        item['addr']=str(item['addr'])
        temp = {}
        temp["table"] = "en_paper"
        temp["params"] = item
        self.db.insertItem(temp)
scis=Service()
if __name__=="__main__":
    # scis.initCode()
    scis.searchCheck()

