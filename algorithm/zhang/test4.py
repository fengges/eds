
import time
from algorithm.zhang.base import dbs


f = open('data2/paperfenci.txt', 'w',encoding='utf8')
f2 = open('data2/id.txt', 'w',encoding='utf8')
subject_topics = [('0802',100, 150 ), ('0810', 100, 150), ('0812',150,300),
                  ('0701', 150, 300), ('0811', 150, 300)]
for i in range(0,10000000,50000) :
    sql = 'select b.* from teacher_dis_code_paper_corejornal a join fenci b on a.id_paper=b.id_paper limit %s,50000'
    paper_list = dbs.getDics(sql,(i))
    if len(paper_list)==0:
        break
    print('save:'+str(i))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    for paper in paper_list:
        item=paper["words"]
        f.write(item)
        f.write("\n")
        f2.write(str(paper["id_paper"]))
        f2.write("\n")
f.close()
f2.close()