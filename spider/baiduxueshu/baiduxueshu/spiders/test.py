
from spider.baiduxueshu.baiduxueshu.spiders import mysql
from spider.baiduxueshu.baiduxueshu import settings
def func():
    db_li = mysql.DB("LiWei")
    db_localhost = mysql.DB("feng3")
    for i in range(0,10000000,5000):
        ids=db_li.getEnglishPaperSerach(i,5000)
        if len(ids)!=0:
            for i in ids:
                cn=db_localhost.getCnById(i["_id"])
                if len(cn)==0:
                    print('update:'+str(i["_id"]))
                    db_li.updateEnglishPaper(i["_id"],0)
        else:
            break
def qingxi():
    i=0
    db_li = mysql.DB("LiWei")
    # sql="SELECT a.*,b.year,b.cited_num,b.source,b.author,b.author_id,b.cited_url,b.reference_url,b.paper_md5,b.timestamp FROM paper_searchlist_1 a  JOIN paper_new b on a._id=b._id "
    sql="SELECT b.* FROM paper_90_clean_1 a  JOIN paper_new b on a._id=b._id"
    englist=db_li.getDics(sql)
    for eng in englist:
        i+=1
        if i%1000==0:
            print(i)
        records = {"table": "paper_english", "params": eng}
        try:
            db_li.insertItem(records)
        except:
            print(eng)
def setTeacherTitle():
    db_li = mysql.DB("LiWei")
    file=open("englist_title.txt","w",encoding="utf8")
    paper = getTeacherTitle(db_li)
    for p in paper:
        file.write(str(p)+"\n")

    file.close()
def getTeacherTitle(db_li):
    paper=[]
    teacher=db_li.getEnglishTeacher()
    for t in teacher:
        eng=db_li.getEnglishPaperByTeacherId(t["author_id"])
        s=""
        for e in eng:
            s+=e["name"]+"."+e["keyword"]+"."
        paper.append({"_id":t["author_id"],"title":s})
    return paper
if __name__ == "__main__":
    # func()
    # qingxi()
    # setTeacherTitle()
    n = 0
    feng3=mysql.DB("feng3")
    while True:
        print(n)
        n += 1
        teacher = feng3.getPaperBySearch(0, 100)
        if len(teacher) == 0:
            break
        for t in teacher:
            lib = eval(t['lib_url'])
            dic = {k: False for k in lib}
            feng3.updatePaperStepById(t['id'], str(dic))
            feng3.updatePaperSearchById(t['id'], 1)

