import pymysql.cursors
from spider.baiduxueshu.baiduxueshu.settings import DB_SETTING
from spider.baiduxueshu.baiduxueshu.settings import CRAWL_SETTING
from spider.baiduxueshu.baiduxueshu.settings import ENGLISH_PAPER,name
import random
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
        "SLX": pymysql.Connect(
            host='47.104.236.183',
            port=3306,
            user='root',
            password='SLX..eds123',
            db='eds',
            charset='utf8'
        ),
    }
    def __init__(self,name):
        try:
            self.connect=self.connectdic[name]
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        except:
            print(name+":数据库链接失败")


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
        sql="update eds_985teacher set search=%s where id=%s"
        params = (search,id)
        self.cursor.execute(sql,params)
        self.connect.commit()
    def updateTeacherBySearch(self,search1,search2):
        sql="update eds_985teacher set search=%s where search=%s"
        params = (search1,search2)
        self.cursor.execute(sql,params)
        self.connect.commit()
    def getTeacher(self,search):
        sql="select * from eds_985teacher where search=%s limit 0,10"
        params =(search)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()
    def getCnById(self,id):
        sql="select * from englist_to_cn where id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()

    def getEnglishPaper(self):
        sql = "select _id,name,abstract from paper_new where search=0 and mod(_id,3)=" + str(
            ENGLISH_PAPER[name]) + " limit 0,1000"
        # sql = "select _id,name,abstract from paper_new where search=0  limit 0,1000"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getEnglishPaperSerach(self):
        sql = "select _id from paper_new where search=1 and mod(_id,3)=" + str(ENGLISH_PAPER[name])
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def updateEnglishPaper(self, id, num):
        sql = "update paper_new set search=%s where _id=%s"
        params = (num, id)
        self.cursor.execute(sql, params)
        self.connect.commit()


    def exe_sql(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.connect.commit()
        return self.cursor.fetchall()
    # 插入论文
    def InsertPaper(self, item):
        sql = "INSERT INTO paper VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        params = (str(uuid.uuid1()),
            item['name'], item['url'], item['abstract'], item['org'], item['year'], item['cited_num'],
            item['source'],
            item['source_url'], item['keyword'], item['author'], item['author_id'], item['cited_url'],
            item['reference_url'], item['paper_md5'])
        self.cursor.execute(sql, params)
        self.connect.commit()


