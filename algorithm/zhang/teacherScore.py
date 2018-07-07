import pickle
from algorithm.base import dbs

sql="select a.xueke2,b.code from (SELECT xueke2 from discipline  GROUP BY xueke2) a left join  discipline_new b on a.xueke2=b.`name` GROUP BY a.xueke2"
xueDic={
"中国史":"06",
"农业资源与环境":"09",
"图书情报与档案管理":"12",
"城乡规划学":"12",
"安全科学与工程":"0819",
"戏剧与影视学":"05",
"考古学":'06',
"艺术学理论":'05',
"草学":'09',
"设计学":'05',
"软件工程":"0812",
"音乐与舞蹈学":'05',
"风景园林学":'05',
}
xue=dbs.getDics(sql)
for x in xue:
    if x["code"] is None:
        x["code"]=xueDic[x["xueke2"]]

    elif x["code"][0:2]=="07" or x["code"][0:2]=="08":
        x["code"]=x["code"][0:4]
    else:
        x["code"] = x["code"][0:2]

sql='select * from teacher_dis_code'
list=dbs.getDics(sql)
sql = "SELECT * FROM school_info where name like %s"

for l in list:
    params = (str(l["school"]),)
    school=dbs.getDics(sql,params)
    if len(school)!=0:
        if school[0]["scope"]:
            l["scool_value"] = int(school[0]["scope"])
        else:
            l["scool_value"] =50
        l["scool_id"] = school[0]["id"]
        continue
    params = ("%" + l["school"] + "%",)
    school=dbs.getDics(sql,params)
    if len(school)==0:
        l["scool_value"]=50
    else:
        if school[0]["scope"]:
            l["scool_value"] = int(school[0]["scope"])
        else:
            l["scool_value"] =50
        l["scool_id"] = school[0]["id"]
sql = "SELECT * FROM discipline where school =%s and xueke2=%s"
xuekeDic={
    "A+":9,
    "A":8,
    "A-":7,
    "B+": 6,
    "B": 5,
    "B-": 4,
    "C+": 3,
    "C": 2,
    "C-": 1,
}
for l in list:
    l["xueke_value"]=[]
    for x in xue:
        if l['discipline_code']==x["code"]:
            if "scool_id" in l :
                params = (l["scool_id"],x["xueke2"])
                xueke = dbs.getDics(sql, params)
                if len(xueke)!=0:
                    l["xueke_value"].append(xuekeDic[xueke[0]["level"].strip()])

for l in list:
    print(l)
pickle.dump(list, open('data/13.txt', 'wb'))



