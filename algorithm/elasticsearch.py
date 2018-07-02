
import random
import string
from algorithm.base import dbs
import pickle

def setDateSet(result):
    list = []
    field = ["数据挖掘", "人脸识别", "机器学习", "deep learning", "healthcare", "data mining", "machine learning", "deep learning",
             "healthcare", "organic", "c", "css3", "html5"]
    for t in result:
        if t['fields'] is not None:
            list.append(t)
            continue
        f = []
        for j in range(random.randint(0, 4) + 1):
            f.append(field[random.randint(0, len(field)) - 1])
        t['fields'] = f
        list.append(t)
    return list
print('导出数据')
sql='SELECT paper_clean1.id,paper_clean1.author_id,paper_clean1.`name` as title,paper_clean1.abstract,t.name,t.school,t.institution,t.citation,t.paper_num,t.h_index,t.fields from paper_clean1 JOIN (select radar.author_id,radar.citation,radar.paper_num,radar.h_index,teacher.name,teacher.school,teacher.institution,teacher.fields from teacher LEFT JOIN radar on teacher.id =radar.author_id ) as t on paper_clean1.author_id=t.author_id'
list=dbs.getDics(sql)
print(len(list))

sql = "SELECT * FROM school_info"
schools=dbs.getDics(sql)
def getScool(name):
    r=[]
    for s in schools:
        if s['name'].find(name)>=0:
            r.append(s)
    return r

for l in list:
    school=getScool(l["school"])
    if len(school)==0:
        l["score"]=30
    else:
        l["score"]=school[0]["scope"]

list=setDateSet(list)

save_path = 'c://temp/' + str(0) + '.json'
f = open(save_path, 'w',encoding='utf-8')
i=1
bat=open('c://upload.bat', 'w',encoding='utf-8')
bat.write('curl -H "Content-Type: application/json" 127.0.0.1:9200/_bulk?pretty --data-binary @'+save_path)
bat.write('\n')
print(len(list))
for l in list:
    f.write('{"index":{"_index":"teachers","_type":"paper","_id":"%s"}}'%l['id'])
    f.write('\n')
    s='{'
    for k in l:
        s+='"'+k+'":'
        if isinstance(l[k], int):
            s+=str(l[k])+','
        elif type(l[k])==type([]):
            s += str(l[k]).replace('\'','"') + ','
        else:
            s+='"'+str(l[k]).replace('	','').replace('\r','').replace('\n','').replace('"','\\"')+'",'
    s=s[0:-1]+'}'
    f.write(s)
    f.write('\n')
    if i%10000==0:
        print(i/10000)
        f.close()
        save_path = 'c://temp/' + str(i/10000) + '.json'
        bat.write('curl -H "Content-Type: application/json" 127.0.0.1:9200/_bulk?pretty --data-binary @' + save_path)
        bat.write('\n')
        f = open(save_path, 'w', encoding='utf-8')
    i+=1

f.close()
bat.close()
