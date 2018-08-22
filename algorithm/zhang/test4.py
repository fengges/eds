
import time,os
from algorithm.zhang.base import dbs
import jieba
import jieba.posseg as pseg
import gensim

import pyLDAvis.gensim
from gensim import corpora
# f = open('data2/paperfenci.txt', 'w',encoding='utf8')

# subject_topics = [('0802',100, 150 ), ('0810', 100, 150), ('0812',150,300),
#                   ('0701', 150, 300), ('0811', 150, 300)]
#
# subject_topics = [('0802',100, 150 )]
# for i in range(0,10000000,50000) :
#     sql = 'select b.* from teacher_dis_code_paper_corejornal a join fenci b on a.id_paper=b.id_paper limit %s,50000'
#     paper_list = dbs.getDics(sql,(i))
#     if len(paper_list)==0:
#         break
#     print('save:'+str(i))
#     print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
#     for paper in paper_list:
#         item=paper["words"]
#         f.write(str(paper["id_paper"])+" "+str(paper["id_paper"])+" "+item)
#         f.write("\n")
# f.close()
# f2.close()
catalog="fenci/"
def strToMap(s):
    dic={}
    list=s.split(' + ')
    for l in list:
        v=l.split('*')
        key=v[1][1:-1]
        dic[key]=float(v[0])
    return dic
def loadData(code):
    sql = 'SELECT id FROM `teacher_dis_code` where discipline_code=%s'
    papersql="select id,name,keyword from paper where author_id=%s"
    engsql = "select cn from englist_title where id=%s"
    teacher = dbs.getDics(sql,(code,))
    file=open("fenci/"+code+".txt",'w',encoding='utf8')
    num1,num2,num3=0,0,0
    for t in teacher:
        id=t["id"]
        papers=dbs.getDics(papersql,(id,))
        num1+=len(papers)
        paper=[]
        keyWord=[]
        for p in papers:
            paper.append(p["name"])
            keyWord.extend(p["keyword"].split(','))
        eng=dbs.getDics(engsql,(id,))
        num2 += len(eng)
        temp = {"id": id, "paper":".".join(paper), "keyWord":keyWord}
        if len(eng)>0:
            temp["paper"]+=eng[0]["cn"]
        if len(temp["paper"])>0 or len(temp["keyWord"])>0:
            file.write(str(temp)+'\n')
            num3+=1
    file.close()
    print("paper:",num1)
    print("eng:", num2)
    print("teacher:", num3)
def fenci(code):
    stopwords = [line.strip() for line in open('stopwords.txt', encoding='utf-8').readlines()]
    fill = ['vn', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
            'nt', 'nz', 'nl', 'ng']
    print('词典更新')
    jieba.load_userdict('userdict.txt')
    file = open(catalog+ code + ".txt", 'r', encoding='utf8')
    file2 = open(catalog + code + "_fenci.txt", 'w', encoding='utf8')
    dic={}
    for line in file.readlines():

        item=eval(line)
        seg_list = pseg.cut(item["paper"])
        words = []
        for word, flag in seg_list:
            if flag in fill and word not in stopwords:
                words.append(word)

        for w in words:
            if w not in dic:
                dic[w]=0
            dic[w]+=1
        words.extend(item['keyWord'])
        temp = {"id": item["id"],"fenci":" ".join(words)}
        file2.write(str(temp)+"\n")
    file2.close()
    c1 = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    file3=open(catalog + code + "_dic.txt", 'w', encoding='utf8')
    for d in c1:
        file3.write(str(d[0])+":"+str(d[1])+"\n")
    file3.close()
def lda(subject):

    code=subject[0]
    file = open(catalog+ code + "_fenci.txt", 'r', encoding='utf8')
    DocWord=[]
    for line in file.readlines():
        item=eval(line)
        words=item["fenci"].split(" ")
        DocWord.append(words)
    file.close()

    dictionary = corpora.Dictionary(DocWord)
    corpus = [dictionary.doc2bow(text) for text in DocWord]
    num_topics=subject[1]
    num_words=50
    iterations=subject[2]
    print('学科代码:'+code+'总数为%d，即将分为主题数%d个，关键字%d个......' % (len(corpus),num_topics,num_words))
    time1 = time.time()
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary,iterations=iterations,passes=5)
    result = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
    time2 = time.time()
    print('模型训练用时：', time2 - time1)
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)

    pyLDAvis.save_html(vis, catalog+'view/k'+str(num_topics)+'.html')
    try:
        os.makedirs(catalog+"k"+str(num_topics)+"/")
    except:
        pass
    file1 = open(catalog+"k"+str(num_topics)+"/" + code + "_topic.txt", 'w', encoding='utf8')
    for r in result:
        d = strToMap(r[1])
        file1.write(str(r[0])+":"+str(d)+'\n')
    file1.close()

    file2 = open(catalog+"k"+str(num_topics)+"/" + code + "_teacher_topic.txt", 'w', encoding='utf8')
    doc_lda = ldamodel[corpus]
    for n in range(len(doc_lda)):
        Topic=doc_lda[n]
        c1 = sorted(Topic, key=lambda x: x[1], reverse=True)
        file2.write(str(c1)+'\n')
    file2.close()
    # for n in range(len(doc_lda)):
    #     Topic=doc_lda[n]
    #     top={}
    #     c1 = sorted(Topic, key=lambda x: x[1], reverse=True)
    #     wordTopic = [i[1] for i in result if int(c1[0][0]) == i[0]]
    #     d=strToMap(wordTopic[0])
    #     t={}
    #     for key in DocWord[n]:
    #         if key in d.keys():
    #             t[key]=d[key]
    #     topic=c1[0][0]
    #     prams=(institution_paper_list[n][0],institution+str(topic),json.dumps(d,ensure_ascii=False),json.dumps(t,ensure_ascii=False))
    #     sql='insert into lda values(%s,%s,%s,%s)'
    #     list = dbs.exe_sql(sql, prams)
if __name__=="__main__":
    # subject_topics = [('0802',100, 150 ), ('0810', 100, 150), ('0812',150,300),
    #                   ('0701', 150, 300), ('0811', 150, 300)]
    #
    subject_topics = [('0812',[i for i in range(10,500,5)],6000)]
    for subject in subject_topics:
        # loadData(subject[0])
        # fenci(subject[0])

        for i in subject[1]:
            try:
                os.makedirs(catalog + "view")
            except:
                pass
            sub=[subject[0],i,subject[2]]
            lda(sub)
