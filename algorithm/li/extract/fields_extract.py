from algorithm.li.extract.utils.dbutils import dbs


def paper_seg():
    import re
    import jieba
    jieba.load_userdict('.\\dicts\\user_dict_1.txt')
    term_dict = {}.fromkeys(open('.\\dicts\\term.txt', 'r', encoding='utf8').read().split('\n'), 'ok')

    # s_sql = "SELECT id, title, abstract FROM paper_data WHERE discipline='0812'"
    s_sql = "SELECT id, title, abstract FROM paper_data WHERE id in (632158,632690,633512,634259,634504,644862,645697,647947,651835,696197,697667,698942,701609,701882,702953,703279,719978,778166,781868,782636,785997,787785,788662,788852,789241,868144,869130,869391,869971,870955,871869,873702,877593,878509,878761,1057022,1069453,1070486,1085083,1085705,1086615,1088270,1096989,1328935,1329754,1330950,1333472,1336010,1376006,1379811,1382522,1384484,1519331,1538164,1591831,1912371,1913089,1913270,1915550,1916681,1921026,1921611,1922188,1923005,1923339,1923498,1924501,1925167,1934011,1935109,1942329,1947322,1951950,1955110,1978880,1983142,1986760,1987129,1989538,1990521,1991737,1995202,2023057,2030104,2032255,2032605,2039093,2043059,2045712,2051244,2064811,2090132,2090809,2091235,2102585,2103888)"
    data_list = dbs.getDics(s_sql)

    u_sql = "UPDATE paper_data SET word_seg=%s WHERE id=%s"
    u_list = []

    fields_dict = dict()

    for data in data_list:
        title = data['title']
        abstract = data['abstract']

        word_list = jieba.cut(title+"\n"+abstract, HMM=False, cut_all=True)
        seg_dict = dict()

        for word in word_list:
            if term_dict.get(word, "") != "":
                c = seg_dict.get(word, 0)
                seg_dict[word] = c+1

                cc = fields_dict.get(word, 0)
                fields_dict[word] = cc+1

        # u_list.append((str(seg_dict), data['id']))
        print(abstract)
        print((str(seg_dict), data['id']))
        print("*" * 10)

    for w, k in fields_dict.items():
        print("%s,%s\n" % (w, str(k)))

        # l = len(u_list)
        # if l == 10000:
        #     print(dbs.exe_many(u_sql, u_list))
        #     u_list = []

    # print(len(u_list))
    # print(dbs.exe_many(u_sql, u_list))

    pass


def get_user_dict():
    term_list = open('.\\dicts\\term.txt', 'r', encoding='utf8').read().split('\n')
    r_list = [term+" "+str(10**len(term))+" "+"n" for term in term_list]
    fw = open('.\\dicts\\user_dict_1.txt', 'w', encoding='utf8')
    fw.write('\n'.join(r_list))
    fw.close()
    pass


def check_word():
    import re

    s_sql = "SELECT id, title, abstract FROM paper_data WHERE discipline='0812'"
    data_list = dbs.getDics(s_sql)

    for data in data_list:
        title = data['title']
        # abstract = data['abstract']
        abstract = ""
        if re.findall(r'半监督', title + abstract):
            print(data['id'])
            print(title + abstract)
        if re.findall(r'k近邻|K近邻', title + abstract):
            print(data['id'])
            print(title + abstract)
        if re.findall(r'k值|K值', title + abstract):
            print(data['id'])
            print(title + abstract)
        if re.findall(r'CNN|cnn', title + abstract):
            print(data['id'])
            print(title + abstract)


def test():
    t_list = open('.\\test\\ttt.txt', 'r', encoding='utf8').read().split('\n')
    t_dict = dict()
    for t in t_list:
        the_t = t.split(',')
        r = the_t[0]
        f = the_t[1]

        c = t_dict.get(r, 0)
        t_dict[r] = c+int(f)

    for w, v in t_dict.items():
        print("%s,%s" % (w, str(v)))

    print(len(t_list))
    print(len(t_dict))


def t():
    import jieba.posseg as pseg
    import xlwt

    s_sql = "SELECT id, title, abstract FROM paper_data WHERE discipline='0812'"
    data_list = dbs.getDics(s_sql)

    flag_list = ["p", "x", "uj", "f", "c", "uv", "ul", "r"]

    word_dict = dict()
    for data in data_list:
        title = data['title']
        abstract = data['abstract']

        word_list = pseg.cut(title + "\n" + abstract, HMM=True)
        for w, f in word_list:
            if f in flag_list:
                key = w+"--SPLIT--"+f
                c = word_dict.get(key, 0)
                word_dict[key] = c+1

    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('sheet1')
    row = 0
    for k, v in word_dict.items():
        word = k.split('--SPLIT--')[0]
        flag = k.split('--SPLIT--')[1]
        f = v
        sheet.write(row, 0, word)
        sheet.write(row, 1, flag)
        sheet.write(row, 2, f)
        row += 1

    wbk.save('.\\test\\con_stop.xls')
    print(row)


if __name__ == "__main__":
    # get_user_dict()
    # paper_seg()
    # test()
    t()
    pass
