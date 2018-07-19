

from algorithm.base import dbs

sql="SELECT _id,discipline_subject FROM `journal`"

temp=dbs.getDics(sql)
dic={}
for t in temp:
    sub=t['discipline_subject']
    list=sub.split('-')
    if list[0] not in dic:
        dic[t["_id"]]=list[0]

sql="SELECT id,org_id,author_id FROM paper_clean1"
paper=dbs.getDics(sql)
teacher={}
i=0
for p in paper:
    if p['org_id']!=-1:
        item={}
        item["father_id"]=p["id"]
        item["type"]="1"
        item["prefix"]=dic[p['org_id']]
        records = {"table": "LdaPrefix", "params": item}
        dbs.insertItem(records)
        if p["author_id"] in teacher:
            if p['org_id'] in teacher[p["author_id"]]:
                teacher[p["author_id"]][p['org_id']]+=1
            else:
                teacher[p["author_id"]][p['org_id']] = 1
        else:
            teacher[p["author_id"]]={p['org_id']:1}
        i+=1
        if i%10000==0:
            print(i)

for i in teacher:
    c1 = sorted(teacher[i].items(), key=lambda x: x[1], reverse=True)
    item["father_id"] = i
    item["type"] = "2"
    item["prefix"] = dic[c1[0][0]]
    records = {"table": "LdaPrefix", "params": item}
    dbs.insertItem(records)





