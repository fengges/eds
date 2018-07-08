
#  author   ：feng
#  time     ：2018/6/22
#  function : 领域
from eds.error import MyError
from eds.dao.field.fieldDao import  fieldDao

class FieldService:
    def getFieldTeacher(self):
        dic={}
        list=fieldDao.getFieldTeacher()
        for r in list:
            if r["theme"] is None:
                r["theme"]=[]
            else:
                r["theme"]=r["theme"].split(",")[0:5]
            if r["codeName"] in dic:
                dic[r["codeName"]].append(r)
            else:
                if r["name"] is None:
                    dic[r["codeName"]]=[]
                    continue
                dic[r["codeName"]]=[r]
        result=[]
        for k in dic:
            result.append({"field":k,"teacher":dic[k]})
        return result
    def getField(self):
        result=fieldDao.getField()
        return result

    def setField(self,param):
        if len(param)<3:
            raise MyError(701)
        elif len(param)>5:
            raise MyError(702)
        param.reverse()
        fieldDao.setField(param)

    def changeTeacherField(self,param):
        fieldDao.changeTeacherField(param)

    def getTeacgerByXueKe(self,xueke):
        return fieldDao.getTeacgerByXueKe(xueke)

fieldService=FieldService()

