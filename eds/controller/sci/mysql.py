import pymysql.cursors
import uuid
# 连接数据库
class DB(object):
    connectdic={

        # "LiWei": pymysql.Connect(
        #     host='10.6.11.44',
        #     port=3306,
        #     user='root',
        #     password='1111',
        #     db='englishpaper',
        #     charset='utf8'
        # ),
        # "feng3": pymysql.Connect(
        #     host='10.6.11.40',
        #     port=3306,
        #     user='root',
        #     password='zdf.0126',
        #     db='eds',
        #     charset='utf8'
        # ),
        "feng1": pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='SLX..eds123',
            db='eds_spider',
            charset='utf8'
        ),
    }
    def __init__(self,name):
        try:
            self.connect=self.connectdic[name]
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        except:
            print(name+":数据库链接失败")

    def updateItem(self,item):
        sql="updata en_paper set name=%s,org=%s,year=%s,abstract=%s,keyword=%s,addr=%s where id=%s"
        params=(item["name"],item["org"],item["year"],item["abstract"],item["keyword"],item["addr"],item["id"])
        self.exe_sql(sql,params)
    def insertItem(self,item):
        table=item["table"]+"("
        temp=",".join(["%s" for i in item["params"]])
        column=" values("+temp+")"
        paramList=[]
        columnList=[]
        for k in item["params"]:
            columnList.append(k)
            paramList.append(item["params"][k])
        params=tuple(paramList)
        sql="insert into "+table+ ",".join(columnList)+")"+column
        self.exe_sql(sql,params)

    def updateTeacherById(self,id,search):
        sql="update es_teacher set search=%s where id=%s"
        params = (search,id)
        self.cursor.execute(sql,params)
        self.connect.commit()
    def updateTeacherBySearch(self,search1,search2):
        sql="update eds_985teacher set search=%s where search=%s"
        params = (search1,search2)
        self.cursor.execute(sql,params)
        self.connect.commit()
    def getTeacher(self,search,num):
        sql="select * from es_teacher where search=%s limit 0,%s"
        params =(search,num)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()
    def getTeacherById(self,id):
        sql="select * from es_teacher where id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()

    def exe_sql(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.connect.commit()
        return self.cursor.fetchall()



