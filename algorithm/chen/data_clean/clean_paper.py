"""
数据清洗流程：
###1、合并paper到paper_all：
将paper_cr paper_wei paper_feng paper_all合并到paper_all
操作：直接运行sql查询即可。
INSERT INTO paper_all(name,url,abstract,org,`year`,cited_num,source,source_url,keyword,author,author_id,cited_url,reference_url,paper_md5)
SELECT t2.name,t2.url,t2.abstract,t2.org,t2.`year`,t2.cited_num,t2.source,t2.source_url,t2.keyword,t2.author,t2.author_id,t2.cited_url,t2.reference_url,t2.paper_md5 FROM paper_feng t2;
INSERT INTO paper_all(name,url,abstract,org,`year`,cited_num,source,source_url,keyword,author,author_id,cited_url,reference_url,paper_md5)
SELECT t2.name,t2.url,t2.abstract,t2.org,t2.`year`,t2.cited_num,t2.source,t2.source_url,t2.keyword,t2.author,t2.author_id,t2.cited_url,t2.reference_url,t2.paper_md5 FROM paper_cr t2;
INSERT INTO paper_all(name,url,abstract,org,`year`,cited_num,source,source_url,keyword,author,author_id,cited_url,reference_url,paper_md5)
SELECT t2.name,t2.url,t2.abstract,t2.org,t2.`year`,t2.cited_num,t2.source,t2.source_url,t2.keyword,t2.author,t2.author_id,t2.cited_url,t2.reference_url,t2.paper_md5 FROM paper_wei t2;
###2、从paper_all中取数据做第一步清洗存入paper_clean1
第一步清洗包括：
    a.删除姓名与作者不匹配的文章
    b.删除 摘要 or 题名 or 作者 or 机构 为空的文章
    c.删除作者组织与作者学校不匹配的文章
    d.删除不存在的author_id的文章

###3、paper_clean1去重
操作：直接运行sql查询即可。
TRUNCATE TABLE temp_idtable2;
INSERT INTO temp_idtable2
SELECT t1.id FROM `paper_clean1` AS t1 GROUP BY t1.author_id,t1.paper_md5;
TRUNCATE TABLE temp_idtable;
INSERT INTO temp_idtable
SELECT id FROM paper_clean1 WHERE id not in(
SELECT id FROM temp_idtable2
);
DELETE a.* FROM paper_clean1 AS a,temp_idtable AS b WHERE a.id=b.id;
"""
# 连接数据库
import json
import pymysql.cursors
class Mysql(object):
    connect = pymysql.Connect(
        # host='localhost',
        # port=3306,
        # user='root',
        # passwd='Cr648546845',
        # db='eds',
        # charset='utf8'

        host = '47.104.236.183',
        port = 3306,
        user = 'root',
        passwd = 'SLX..eds123',
        db = 'eds',
        charset = 'utf8'
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

    # 从paper_all的数量
    def getPaperNum(self):
        sql = "SELECT count(*) FROM paper_all"

        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data

    # 从paper_clean1的数量
    def getPaperNum_clean(self):
        sql = "SELECT count(*) FROM paper_clean1"

        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data

    def getTeacher(self):
        sql = "SELECT * FROM paper_search_list_all"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # 插入论文
    def InsertPaper(self, list):
        sql = "INSERT INTO paper_clean1 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.executemany(sql, list)
        self.connect.commit()

    def getPaperOrg(self,start,num):
        sql = "SELECT id,org FROM paper_clean1 LIMIT %s,%s;"
        params = (start, num)
        self.cursor.execute(sql, params)
        data = self.cursor.fetchall()
        return data

    # 改出版机构
    def UpdateOrg(self, list):
        sql = "UPDATE paper_clean1 SET org=%s, org_id=%s WHERE id=%s"
        r = self.cursor.executemany(sql, list)
        self.connect.commit()
        print('更改org条数：',r)

    # 核心期刊鉴别
    def UpdateCorej(self, list):
        sql = "UPDATE paper_clean1 SET core_journal=%s WHERE id=%s"
        r = self.cursor.executemany(sql, list)
        self.connect.commit()
        print('更改org条数：', r)
def dataclean_step2():
    """
    数据清洗的第二步
    :return:
    """

    db = Mysql()

    teacherlist = db.getTeacher()
    teacherdic = {}
    for teacher in teacherlist:
        teacherdic[teacher['id']] = teacher['name'] + "-split-" + teacher['school']

    """
    批处理操作：从第i个数据开始，每次取b个元素进行清洗
    """
    i = 0
    b = 100000
    num = db.getPaperNum()['count(*)']
    yu = num%b
    while i < num:
        if i == num-yu: b = yu

        paperlist = db.getPaper(i, b)
        print("获取数据i,b:", i, b)
        dpaperlist = []
        for paper in paperlist:
            id = paper['id']
            name = paper['name']
            abstract = paper['abstract']
            org = paper['org']
            author = paper['author']
            author_id = paper['author_id']

            try:
                teacher = teacherdic[author_id]
                teachername = teacher.split('-split-')[0]
                teacherschool = teacher.split('-split-')[1]
            except:
                print('这个paper没有这个authorid', author_id)
                dpaperlist.append(id)
                continue

            if name == '':
                # print('name删')
                dpaperlist.append(id)
                continue
            if abstract == '':
                # print('abstract删')
                dpaperlist.append(id)
                continue
            if org == '':
                # print('org删')
                dpaperlist.append(id)
                continue
            if author == '':
                # print('author删')
                dpaperlist.append(id)
                continue
            else:
                flag = 0
                try:
                    authorjson = json.loads(author)
                    for node in authorjson:
                        if node['name'] == teachername and node['org'].find(teacherschool) != -1: flag = 1
                except:
                    print('authorjson解析出错')
                    print(author)
                if flag == 0:
                    # print('authorname shan')
                    # print(author,teachername,teacherschool)
                    dpaperlist.append(id)
        newpaperlist = []
        for item in paperlist:
            if not (item['id'] in dpaperlist):
                newpaperlist.append((item['id'], item['name'], item['url'], item['abstract'], item['org'], item['year'],
                                     item['cited_num'],
                                     item['source'],
                                     item['source_url'], item['keyword'], item['author'], item['author_id'],
                                     item['cited_url'],
                                     item['reference_url'], item['paper_md5']))
        db.InsertPaper(newpaperlist)
        print("插入十万条")
        print(i)
        i += b


import os
def paper_journal():
    """
    给paper关联journalid
    """
    db = Mysql()
    root = os.path.dirname(os.path.abspath(__file__))
    journal_dict = eval(open(root + "\\data\\journal_dict.txt", "r", encoding='utf8').read())

    i = 0
    b = 100000
    num = db.getPaperNum_clean()['count(*)']
    yu = num % b
    while i < num:
        if i == num - yu: b = yu
        update_list = []
        org_list = []
        papers = db.getPaperOrg(i,b)
        print("获取paper:",i,b)
        for paper in papers:
            org = my_strip(paper["org"])
            org_id = journal_dict.get(org, -1)
            if org_id == -1:
                org_list.append(org)
            update_list.append((org, org_id, paper["id"]))
        fw = open(root + "\\data\\unknow_journal_list.txt", "a", encoding='utf8')
        fw.write("\n".join(org_list))
        fw.close()
        db.UpdateOrg(update_list)
        i += b

def my_strip(str=""):
    # 去除字符串中空格和其他字符
    import re
    text = re.sub(r'\u00a0', ' ', str)
    re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r', '《', '》', '.', '—']
    while len(text) > 0 and text[0] in re_list:
        text = text.lstrip(text[0])
    while len(text) > 0 and text[-1] in re_list:
        text = text.rstrip(text[-1])
    return text
    pass

import re
def get_core_journal():
    f = open('data/core_journal.txt', 'r', encoding='utf-8')
    data = f.read()
    cjlist = data.split(',')
    # print(cjlist)
    return cjlist

def paper_core_journal():
    """
    给paper判断是否是核心期刊
    """
    db = Mysql()
    cjlist = get_core_journal()

    i = 0
    b = 100000
    num = db.getPaperNum_clean()['count(*)']
    yu = num % b
    while i < num:
        if i == num - yu: b = yu
        paperlist = db.getPaperOrg(i,b)
        update_list = []
        for paper in paperlist:
            org = paper['org']
            words = re.findall('[\u4e00-\u9fa5]', org)
            word = ''.join(words)
            if word in cjlist:
                update_list.append([1,paper['id']])
            else:update_list.append([0,paper['id']])
        db.UpdateCorej(update_list)
        i += b
        print(i,b)

from algorithm.chen.data_clean.utils.dbutils import dbs
def check_org():



    sql = 'select id,name,school,institution from teacher'
    teacherlist = dbs.getDics(sql)
    teacherdic = {}
    for teacher in teacherlist:
        teacherdic[teacher['id']] = teacher['name'] + "-split-" + teacher['institution'] +"-split-" + teacher['school']

    i = 1243000
    b = 10000
    num = 3812079
    yu = num % b
    while i < num:
        if i == num - yu: b = yu

        sql = 'select id,author,author_id from paper_clean1 limit %s,%s'%(i,b)
        data = dbs.getDics(sql)
        updatelist = []
        for paper in data:
            author_id = paper['author_id']
            author = paper['author']
            try:
                teacher = teacherdic[author_id]
                teachername = teacher.split('-split-')[0]
                teacherinstitution = teacher.split('-split-')[1]
                teacherschool = teacher.split('-split-')[2]
            except:
                print('这个paper没有这个authorid', author_id)
                continue

            flag = 0
            authorjson = json.loads(author)
            for node in authorjson:
                if node['name'] == teachername:
                    org = node['org']
                    org = org.replace(teacherschool,'')
                    if org!='' and include(org,teacherinstitution):
                        flag = 1
            updatelist.append([flag,paper['id']])
        sql = 'UPDATE paper_clean1 SET checkOrg=%s WHERE id=%s'
        dbs.exe_many(sql,updatelist)
        i += b
        print(i,b)

def include(a,b):
    if len(a)>len(b):
        lista = set(a)
        listb = set(b)
    else:
        lista = set(b)
        listb = set(a)
    c = len(lista)-len(listb)
    if len(lista-listb)<=c:
        return True
    else:return False


if __name__ == '__main__':
    # db = Mysql()
    # paper_core_journal()
    # get_core_journal()
    check_org()

    pass
