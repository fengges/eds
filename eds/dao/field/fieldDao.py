#  author   ：feng
#  time     ：2018/6/22
#  function ：留言
from eds.dao.base import dbs
class FieldDao:
    def getFieldTeacher(self):
        sql="SELECT c.*,d.name,d.school,d.institution,d.theme,d.title from (select a.codeName,a.time,b.id from (SELECT code,time,name as codeName FROM `discipline_new` where selected=1 ORDER BY time desc) a LEFT JOIN teacher_dis_code b on b.selected=1 and a.`code`=b.discipline_code ORDER BY a.time desc,b.time desc) c LEFT JOIN teacher d on c.id=d.id"
        s=dbs.getDics(sql)
        return s
    def getField(self):
        sql = 'SELECT  a.*,b.`name`,b.selected from (SELECT discipline_code ,count(*) as num FROM `teacher_dis_code` GROUP BY discipline_code) a join discipline_new b on a.discipline_code=b.`code` ORDER BY  time desc'
        s=dbs.getDics(sql)
        return s

    def changeTeacherField(self,param):
        sql="update teacher_dis_code set selected=%s where id=%s"
        params=(param["selected"],param["id"])
        dbs.exe_sql(sql,params)

    def setField(self,param):
        update_sql="update discipline_new set selected=0"
        dbs.exe_sql(update_sql)
        set_sql="update discipline_new set selected=1 where code= %s"
        for p in param:
            dbs.exe_sql(set_sql,(p,))

    def getTeacgerByXueKe(self,param):
        sql_num="SELECT count(*) as num from (select id from teacher_dis_code where discipline_code=%s) a left join teacher b on a.id=b.id"
        sql="SELECT a.*,b.age,b.email,b.theme from (select id,name,school,institution,selected,time from teacher_dis_code where discipline_code=%s) a left join teacher b on a.id=b.id order by a.selected desc,a.time desc limit %s,%s"
        s=dbs.getDics(sql,(param['field'],param['pPageNum']*(param['page']-1),param['pPageNum']))
        n = dbs.getDics(sql_num,(param['field'],))
        return {"result":s,"num":n[0]["num"]}

fieldDao=FieldDao()