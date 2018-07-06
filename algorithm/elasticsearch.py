
import random
import string
from algorithm.base import dbs


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
sql='SELECT paper.id,paper.author_id,paper.`name` as title,paper.abstract,t.name,t.school,t.institution,t.citation,t.paper_num,t.h_index,t.fields from paper JOIN (select radar.author_id,radar.citation,radar.paper_num,radar.h_index,teacher.name,teacher.school,teacher.institution,teacher.fields from teacher LEFT JOIN radar on teacher.id =radar.author_id ) as t on paper.author_id=t.author_id'
list=dbs.getDics(sql)
print(len(list))
sql = "SELECT * FROM school_info where name like %s"

for l in list:
    params = ("%" + l["school"] + "%",)
    school=dbs.getDics(sql,params)
    if len(school)==0:
        l["score"]=50
    else:
        l["score"]=school[0]["scope"]

list=setDateSet(list)
save_path = 'E:temp\\' + str(0) + '.json'
f = open(save_path, 'w+',encoding='utf-8')
i=1
bat=open('E:upload.bat', 'w+',encoding='utf-8')
bat.write('curl -H "Content-Type: application/json" 47.104.236.183:9200/_bulk?pretty --data-binary @'+save_path)
bat.write('\n')

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
        save_path = 'E:temp\\' + str(i/10000) + '.json'
        bat.write('curl -H "Content-Type: application/json" 47.104.236.183:9200/_bulk?pretty --data-binary @' + save_path)
        bat.write('\n')
        f = open(save_path, 'w+', encoding='utf-8')
    i+=1
