import pickle
# from algorithm.base import dbs
# sql="select _id,name,abstract from paper_new limit 0,10"
# list=dbs.getDics(sql)
#
# dic={}
# import nltk.stem as ns
# import nltk
#
# lemmatizer = ns.WordNetLemmatizer()
# i=0
# for  l in list:
#     word=l['name']+" "+l["abstract"]
#     if i%10000==0:
#         print(i)
#     i+=1
#     text = nltk.word_tokenize(word)
#     tag=nltk.pos_tag(text)
#     temp=""
#     for t in tag:
#         if t[1][0]=="N":
#             temp+=" "+lemmatizer.lemmatize(t[0], 'n')
#         elif t[1][0] =="V":
#             temp += " " + lemmatizer.lemmatize(t[0], 'v')
#
#     dic[l["_id"]]=temp
#
# pickle.dump(dic, open('data/english2.txt', 'wb'))
file = open('data/english.txt', 'rb')
dic = pickle.load(file)
data = {k: dic[k].split() for k in dic}
dic={}
i = 0
for k in data:
    i += 1
    print(i)
    for t in data[k]:
        if t in dic:
            continue
        dic[t] = 1
f = open('data/dic.txt', 'wb')
pickle.dump(dic, f)

f.close()