import requests
from spider.paperspider.papers.papers.dbutils import dbs
import os
import re
from pypinyin import lazy_pinyin

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ins2en(word=""):

    # serviceurl = 'http://xtk.azurewebsites.net/BingDictService.aspx?Word='
    # print(root + "\\dicts\\institution2en.txt")
    # fw = open(root + "\\dicts\\institution2en.txt", "w", encoding='utf8')
    # sql = "select institution from teacher group by institution"
    # inss = dbs.getDics(sql)
    # for ins in inss:
    #     url = serviceurl + ins['institution']
    #     try:
    #         uh = requests.get(url)
    #     except:
    #         print('API错误')
    #         continue
    #     print(ins)
    #     print(str(uh.content, "utf-8"))
    #     if re.match(pattern=r'{.*?}', string=str(uh.content, "utf-8")) is None:
    #         continue
    #     data = uh.json()
    #     print(data['word'])
    #     print(data)
    #     if data['defs'] is None:
    #         continue
    #     en = ";".join([item['def'] for item in data['defs']])
    #     en = en.replace("; ", ";")
    #     print(en)
    #     fw.write("%s:%s\n" % (data['word'], en))
    # fw.close()

    serviceurl = 'http://xtk.azurewebsites.net/BingDictService.aspx?Word='

    url = serviceurl + word
    try:
        uh = requests.get(url)
    except:
        print('API错误')
    if re.match(pattern=r'{.*?}', string=str(uh.content, "utf-8")) is None:
        return ""
    data = uh.json()
    if data['defs'] is None:
        return ""
    return data['defs'][0]['def']


def ins2dict():

    serviceurl = 'http://xtk.azurewebsites.net/BingDictService.aspx?Word='
    sql = "select institution from teacher group by institution"
    inss = dbs.getDics(sql)
    l = []
    for ins in inss:
        url = serviceurl + ins['institution']
        try:
            uh = requests.get(url)
        except:
            print('API错误')
            continue
        if re.match(pattern=r'{.*?}', string=str(uh.content, "utf-8")) is None:
            continue
        data = uh.json()
        if data['defs'] is None:
            continue
        en = data['defs'][0]['def'].split(';')[0]
        print("%s;%s\n" % (data['word'], en))
        l.append("\"%s\":\"%s\"" % (data['word'], en))

    fw = open(root + "\\dicts\\institution2en_dict.txt", "w", encoding='utf8')
    fw.write("{%s}" % ",".join(l))
    print("{%s}" % ",".join(l))
    fw.close()


def name2en(name=""):
    name_list = lazy_pinyin(name)
    return "".join(name_list[1:]) + " " + name_list[0]


if __name__ == "__main__":
    # sql = "select name from teacher"
    # l = dbs.getDics(sql)
    # for item in l:
    #     print(item['name'])
    #     print(name2en(item['name']))
    ins2dict()
    pass

