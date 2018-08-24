from algorithm.li.extract.utils.dbutils import dbs
import os
import csv

def f():
    dis_name = open('dis_name.txt', 'r', encoding='utf8').read().split('\n')
    dis_name = set(dis_name)
    dis_school_dict = dict()
    s_sql = "SELECT school FROM `discipline_school` WHERE `name` = '%s' AND school_id IS NOT NULL"
    for name in dis_name:
        print(name)
        dis_school = [i['school'] for i in dbs.getDics(s_sql % name)]
        dis_school_dict[name] = dis_school

    re_li = list()
    csvreader = csv.reader(open('jishulingyuyuxueke.csv', 'r'))
    lingyu_xueke = [tuple(node) for node in csvreader]

    for node in lingyu_xueke:
        di = dict()
        d_list = node[1].split('-')
        for d in d_list:
            s_list = dis_school_dict[d]
            for s in s_list:
                if di.get(s):
                    di[s] += "-" + d
                else:
                    di[s] = d
        ll = list()
        for key, value in di.items():
            item = key + '(' + '/'.join(value.split('-')) + ')'
            ll.append(item)
        re_li.append('，'.join(ll))
    print(re_li)
    print(len(re_li))

    print('\n'.join(re_li))


if __name__ == "__main__":
    f()
    pass
