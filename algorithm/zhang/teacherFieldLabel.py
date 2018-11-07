import pickle
from algorithm.zhang.base import dbs
# file=open('data/0812.csv',encoding="utf8")
# line=file.readlines()[1:]
# sql="SELECT a.topic,c.id,count(*) as num FROM `lda2` a join paper_clean1 b on a.id=b.id join teacher c on c.id=b.author_id GROUP BY a.topic,c.id"
# temp=dbs.getDics(sql)
# pickle.dump(temp, open('data2/temp', 'wb'))
# filed={}
# for i in line:
#     p=i.strip().split(",")
#     filed[p[0]]=p[1]
# teacher={}
# for t in temp:
#     if t['id'] not in teacher:
#         teacher[t['id']]={}
#     teacher[t['id']][filed[t["topic"]]]=t["num"]

teacher=pickle.load(open('data2/teacher', 'rb'))
sql="update teacher set fields=%s where id =%s"
for t in teacher:
    dbs.exe_sql(sql,(str(teacher[t]),t))
    print(t)

