import requests
from utils.dbutils import dbs
import os
import re

root = os.path.dirname(os.path.abspath(__file__))


def ins2dict(sql=""):
    if sql == "":
        return

    school_dict = eval(open(root + "\\dicts\\institution2en_dict.txt", "r", encoding='utf8').read())
    serviceurl = 'http://xtk.azurewebsites.net/BingDictService.aspx?Word='

    inss = dbs.getDics(sql)
    l = []
    for ins in inss:
        if school_dict.get(ins['institution']) is not None:
            continue
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

    return "{%s}" % ",".join(l)


def school2dict():
    sql = "SELECT institution FROM teacher_searchlist GROUP BY institution"

    return ins2dict(sql)
    pass


if __name__ == "__main__":
    print(school2dict())
    pass

