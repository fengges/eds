import pymysql.cursors
from spider.baiduxueshu.baiduxueshu.settings import DB_SETTING
from spider.baiduxueshu.baiduxueshu.settings import CRAWL_SETTING
import random
import uuid
# 连接数据库
class LocalDB(object):
    connect = pymysql.Connect(
        host=DB_SETTING['host'],
        port=DB_SETTING['port'],
        user=DB_SETTING['user'],
        passwd=DB_SETTING['passwd'],
        db=DB_SETTING['db'],
        charset=DB_SETTING['charset']
)
    #---获取游标---
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

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

class AliyunDB(object):
    connect = pymysql.Connect(
        host='120.78.201.159',
        port=3306,
        user='root',
        password='zdf.0126',
        db='eds',
        charset='utf8'
)
#获取游标
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

    # #---从search表中获取一条教师信息---
    # def getAuthor(self):
    #     randint = str(random.randint(1, 10))
    #     sql = "SELECT * FROM paper_search_list WHERE search=0 AND searching=0 LIMIT " + randint + ",1;"
    #     self.cursor.execute(sql)
    #     teacher = self.cursor.fetchone()
    #
    #     # ---在查询后更改状态为：读取中---
    #     sql = "UPDATE paper_search_list SET searching=1 where id=%s"
    #     params = (teacher['id'])
    #     self.cursor.execute(sql, params)
    #     self.connect.commit()
    #
    #     return teacher

    #---获取所有教师---
    def getAuthor(self):
        sql = "SELECT * FROM paper_search_list WHERE search=0 AND searching=0 and id%"+CRAWL_SETTING['total']+"="+CRAWL_SETTING['num']
        self.cursor.execute(sql)
        teacher = self.cursor.fetchall()
        return teacher

    # ---搜索后更新状态---
    def UpdateAuthor(self, id):
        sql = "UPDATE paper_search_list SET search=1 where id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()

# class TestDB(object):
#     connect = pymysql.Connect(
#         host='localhost',
#         port=3306,
#         user='root',
#         password='Cr648546845',
#         db='edstest',
#         charset='utf8'
# )
# #获取游标
#     cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
#
#     #---从search表中获取一条教师信息---
#     def getAuthor(self):
#         randint = str(random.randint(1, 10))
#         sql = "SELECT * FROM paper_search_list WHERE search=0 AND searching=0 and id%3"+CRAWL_SETTING['total']+"="+CRAWL_SETTING['num']
#         self.cursor.execute(sql)
#         teacher = self.cursor.fetchall()
#         return teacher
#
#     # 插入论文
#     def InsertPaper(self, item):
#         sql = "INSERT INTO paper VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#
#         params = (str(uuid.uuid1()),
#                   item['name'], item['url'], item['abstract'], item['org'], item['year'], item['cited_num'],
#                   item['source'],
#                   item['source_url'], item['keyword'], item['author'], item['author_id'], item['cited_url'],
#                   item['reference_url'], item['paper_md5'])
#         self.cursor.execute(sql, params)
#         self.connect.commit()
#
#     # ---搜索后更新状态---
#     def UpdateAuthor(self, id):
#         sql = "UPDATE paper_search_list SET search=1 where id=%s"
#         params = (id)
#         self.cursor.execute(sql, params)
#         self.connect.commit()