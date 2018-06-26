import json
import pymysql.cursors
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='eds',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    #从paper_all中获取数据
    def uppaperauthor(self):
        sql = "SELECT id,author FROM paper_wei"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def UpdateAuthor(self, id, name):
        sql = "UPDATE paper_wei SET author=%s where id=%s"
        params = (name, id)
        self.cursor.execute(sql, params)
        self.connect.commit()
        print("gengxing:::::", id)

import json
if __name__ == '__main__':
    # db = Mysql()
    #
    # plist = db.uppaperauthor()
    # for node in plist:
    #     id = node['id']
    #     author = node['author']
    #
    #     try:
    #         if author!="":
    #             if author[0] == '{':
    #
    #                 ss = author
    #                 ss = ss.rstrip('}').lstrip('{')
    #                 ss = '[{'+ss+'}]'
    #
    #                 db.UpdateAuthor(id, ss)
    #     except:
    #         print(node)
    data = '[{"name":""2017年湖北社会、经济改革探索十大问题"项目组","org":""},{"name":"黄伟","org":""},{"name":"张青","org":""}]'
    datajson = json.loads(data)
    print(datajson)