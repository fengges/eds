import re

f = open('data/北大核心期刊.txt','r',encoding='utf-8')
lines = f.readlines()

cjlist = []
for line in lines:
    if len(line)>0 and re.findall('[0-9]',line[0]):
        words  = re.findall('[\u4e00-\u9fa5]',line)
        word = ''.join(words)
        cjlist.append(word)

# print(cjdata)

f = open('data/科技核心期刊.txt','r',encoding='utf-8')
lines = f.readlines()
for line in lines:
    if len(line)>0 and re.findall('[A-Za-z]{1}[0-9]{3}',line):


        words  = re.findall('[\u4e00-\u9fa5]',line)
        word = ''.join(words)
        cjlist.append(word)


cjlist = set(cjlist)
rusult = ','.join(cjlist)
f1 = open('data/core_journal.txt','w',encoding='utf-8')
f1.write(rusult)

f.close()
f1.close()
