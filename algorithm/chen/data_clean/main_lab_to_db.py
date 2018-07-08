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
    def getPaper(self,start,num):
        sql = "SELECT * FROM paper_all LIMIT %s,%s;"
        params = (start,num)
        self.cursor.execute(sql,params)
        data = self.cursor.fetchall()
        return data

    def InsertMainLab(self, list):
        sql = "INSERT INTO main_lab VALUES(Null,%s,%s,%s)"
        self.cursor.executemany(sql, list)
        self.connect.commit()


import re
if __name__ == '__main__':
    db = Mysql()
    f = open('F:/Myproject/Python/eds/data_clean/data/main_lab_name.txt','r',encoding='utf-8')

    data = f.read()
    dlist = data.split('\n')
    lablist = []
    i = 0
    while i<len(dlist):
        if dlist[i]!='':
            lablist.append(dlist[i])
        i+=1
    f.close()

    uplist = []
    for lab in lablist:
        org = re.findall('（(.*)）',lab)[0]
        uplist.append((lab,org,''))


    db.InsertMainLab(uplist)
    pass