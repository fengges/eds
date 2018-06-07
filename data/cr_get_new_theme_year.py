import pymysql.cursors
# 连接数据库
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


    def getTheme(self,id):

        sql = "SELECT * FROM `theme_year` where author_id=%s;"
        self.cursor.execute(sql,id)
        data = self.cursor.fetchall()
        return data


    def getIdlist(self):
        sql = "SELECT author_id FROM `theme_year` GROUP BY author_id;"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def upThemecr(self, list):
        sql = "INSERT INTO theme_year_cr VALUES(%s,%s,%s,%s)"
        self.cursor.executemany(sql, list)
        self.connect.commit()

def getlist(id):
    db = Mysql()
    themedata = db.getTheme(id)

    themedic = {}
    for node in themedata:
        #---生成统计字典---
        if node['theme'] in themedic:
            themedic[node['theme']]['sum'] += 1
            maxyear = int(themedic[node['theme']]['maxyear'])
            minyear = int(themedic[node['theme']]['minyear'])
            nodeyear = int(node['year'])
            if nodeyear>maxyear:themedic[node['theme']]['maxyear'] = node['year']
            elif  nodeyear<minyear:themedic[node['theme']]['minyear'] = node['year']
        else:
            themedic[node['theme']] = {'sum':1,'maxyear':node['year'],'minyear':node['year']}

    # print(themedic)
    themesortlist = sorted(themedic, key=lambda k: themedic[k]['sum'],reverse=True)
    themelist = []
    MAXyear = 0
    MINyear = 9999
    if len( themesortlist)>4:
        themelist = themesortlist[:5]
    else:themelist = themesortlist

    for node in themelist:
        if MAXyear<int(themedic[node]['maxyear']):MAXyear = int(themedic[node]['maxyear'])
        if MINyear>int(themedic[node]['minyear']):MINyear = int(themedic[node]['minyear'])

    #---得到前5个主题，以及最大最小年---
    # print(MINyear,MAXyear,themelist)

    datadic = {}
    for theme in themelist:
        tempdic = {}

        for year in range(MINyear,MAXyear+1):
            tempdic[year] = 0
        datadic[theme] = tempdic

    for node in themedata:
        if node['theme'] in themelist:
            datadic[node['theme']][int(node['year'])] += 1

    datalist = []

    for k,v in datadic.items():
        theme = k
        vdic = v
        for key,value in vdic.items():
            year = key
            num = value
            datalist.append([id,str(year),num,theme])
    return datalist

# db = Mysql()
#
# idlist = db.getIdlist()
# for node in idlist:
#     id = node['author_id']
#     print(id)
#     datalist = getlist(id)
#     db.upThemecr(datalist)