import pymysql.cursors
from spider.baiduxueshu.baiduxueshu.settings import DB_SETTING
from spider.baiduxueshu.baiduxueshu.settings import CRAWL_SETTING
from spider.baiduxueshu.baiduxueshu.settings import ENGLISH_PAPER,name
import random
import uuid
# 连接数据库
class DB(object):
    connectdic={
        "local": pymysql.Connect(
                host=DB_SETTING['host'],
                port=DB_SETTING['port'],
                user=DB_SETTING['user'],
                passwd=DB_SETTING['passwd'],
                db=DB_SETTING['db'],
                charset=DB_SETTING['charset']
        ),
        "SLX":  pymysql.Connect(
                host='47.104.236.183',
                port=3306,
                user='root',
                password='SLX..eds123',
                db='eds',
                charset='utf8'
        ),
        "LiWei": pymysql.Connect(
            host='10.6.11.44',
            port=3306,
            user='root',
            password='1111',
            db='englishpaper',
            charset='utf8'
        ),
        "feng3": pymysql.Connect(
            host='10.6.11.40',
            port=3306,
            user='root',
            password='zdf.0126',
            db='eds',
            charset='utf8'
        ),
    }
    def __init__(self,name):
        self.connect=self.connectdic[name]
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
    def updataPaperById(self,item):
        sql = "update en_paper set abstract=%s,org=%s,keyword=%s,step=%s,search=%s where id=%s"
        params=(item["abstract"],item["org"],item["keyword"],item["step"],item["search"],item["id"])
        # self.cursor.execute(sql,params)
        # self.connect.commit()
    def getPaperBySearch(self,search,num):
        sql = "select * from en_paper where search=%s limit 0,%s"
        params=(search,num)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()
    def updatePaperSearchById(self,id,search):
        sql = "update en_paper set search=%s where id=%s"
        params=(search,id)
        self.cursor.execute(sql,params)
        self.connect.commit()
    def updatePaperStepById(self,id,step):
        sql = "update en_paper set step=%s where id=%s"
        params=(step,id)
        self.cursor.execute(sql,params)
        self.connect.commit()
    def getEnglishTeacher(self):
        sql = "select author_id from paper_english_clean where t_search=0 or t_search is Null group by author_id"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def getDics(self,sql,params=None):
        if params is None:
            self.cursor.execute(sql)
        else :
            self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result
    def getEnglishPaperByTeacherId(self,id):
        sql = "select _id,name,keyword from paper_english_clean where  author_id=%s"
        self.cursor.execute(sql,(id,))
        return self.cursor.fetchall()

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
    def getCnById(self,id):
        sql="select * from englist_to_cn where id=%s"
        params = (id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()

    def getEnglishPaper(self):
        sql = "select _id,name,abstract from paper_english where search=0 and mod(_id,2)=" + str(
            ENGLISH_PAPER[name]) + " limit 0,100"
        # sql = "select _id,name,abstract from paper_new where search=1"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def getDics(self,sql,params=None):
        if params is None:
            self.cursor.execute(sql)
        else :
            self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result
    def getEnglishPaperSerach(self,param):
        sql = "select _id from paper_new where search=1  limit %s,%s"
        self.cursor.execute(sql,(param[0],param[1]))
        return self.cursor.fetchall()
    def updateEnglishPaper(self, id, num):
        sql = "update paper_english set search=%s where _id=%s"
        params = (num, id)
        self.cursor.execute(sql, params)
        self.connect.commit()


    def exe_sql(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.connect.commit()
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


