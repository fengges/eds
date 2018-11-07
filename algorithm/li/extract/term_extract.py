from algorithm.li.extract.utils.dbutils import dbs


def get_tf_df():
    '''
    tf：词在领域内出现的频次
    df：词在领域内出现的文档数
    :return:
    '''
    stop_word_base = {}.fromkeys(open('.\\dicts\\stopword_base.txt', 'r', encoding='utf8').read().split('\n'))

    import jieba.posseg as pseg

    code_list = ["0801", "0802", "0803", "0804", "0805", "0806", "0807", "0808", "0809", "0810",
                 "0811", "0812", "0813", "0814", "0815", "0816", "0817", "0818", "0819", "0820",
                 "0821", "0822", "0823", "0824", "0825", "0826", "0827", "0828", "0829", "0830",
                 "0831", "0832"]

    code_num = dict()

    for code in code_list:
        s_sql = "SELECT * FROM paper_data WHERE discipline=%s" % code
        data_list = dbs.getDics(s_sql)
        tf_dict = dict()
        df_dict = dict()
        flag = ["an", "j", "n", "nz", "vn"]
        for data in data_list:
            word_dict = dict()
            seg_list = pseg.cut(data["abstract"], HMM=True)
            for w in seg_list:
                if stop_word_base.get(w.word, "") == "" and w.flag in flag:

                    c = tf_dict.get(w.word, 0) + 1
                    tf_dict[w.word] = c
                    word_dict[w.word] = 1

            for k, v in word_dict.items():
                df = df_dict.get(k, 0) + v
                df_dict[k] = df

        fw = open(".\\test\\tf_df\\%s.csv" % code, "w", encoding="utf8")
        fw.write("term,tf,df\n")
        for k, v in tf_dict.items():
            df = df_dict.get(k, 0)
            fw.write("%s,%s,%s\n" % (k, str(v), str(df)))
        fw.close()
        code_num[code] = len(data_list)

    print(code_num)


def get_pf():
    '''
    pf：t在平衡文档的频次
    df：t在领域内文档的频次
    :return:
    '''
    import pandas as pd

    code_list = ["0801", "0802", "0803", "0804", "0805", "0806", "0807", "0808", "0809", "0810",
                 "0811", "0812", "0813", "0814", "0815", "0816", "0817", "0818", "0819", "0820",
                 "0821", "0822", "0823", "0824", "0825", "0826", "0827", "0828", "0829", "0830",
                 "0831", "0832"]

    word_list = []
    for code in code_list:

        the_data = pd.read_csv('.\\test\\tf_df\\%s.csv' % code)
        for index in the_data.index:
            line_list = []
            count = [0] * len(code_list)
            word = the_data.loc[index].term
            dcount = the_data.loc[index].tf

            line_list.append(word)

            line_list.append(dcount)

            count[code_list.index(code)] = dcount
            line_list.extend(count)

            word_list.append(tuple(line_list))

    print("=" * 10)
    word_list.sort(key=lambda k: k[0])
    lol = len(word_list)
    new_word_list = list()
    new_word_list.append(word_list[0])
    for i in range(1, lol):
        try:
            if word_list[i][0] == new_word_list[-1][0]:
                new_line = list()
                new_line.append(word_list[i][0])
                for j in range(1, 1 + len(code_list) + 1):
                    new_line.append(word_list[i][j] + new_word_list[-1][j])
                new_word_list.pop(-1)
                new_word_list.append(tuple(new_line))
            else:
                new_word_list.append(word_list[i])
        except:
            print("error")
            pass
    print(new_word_list[0:10])
    print(lol)
    print(len(new_word_list))
    new_word_list.sort(key=lambda k: k[1], reverse=True)
    the_file = open(".\\test\\pf_df.csv", 'w', encoding='utf8')
    the_file.write("%s\n" % ",".join(["term", "pf"] + code_list))
    for item in new_word_list:
        the_file.write("%s\n" % ",".join([str(i) for i in list(item)]))
    the_file.close()
    pass


def get_P():
    '''
    计算P值，用于后续计算DC值（即H值）和DR值

    公式：P(t, Dj) ≈ f(t, Dj) / Tj
    :return:
    '''

    import pandas as pd

    code_list = ["0801", "0802", "0803", "0804", "0805", "0806", "0807", "0808", "0809", "0810",
                 "0811", "0812", "0813", "0814", "0815", "0816", "0817", "0818", "0819", "0820",
                 "0821", "0822", "0823", "0824", "0825", "0826", "0827", "0828", "0829", "0830",
                 "0831", "0832"]

    word_list = []
    for code in code_list:
        num_dict = eval(open(".\\test\\discipline_DF.txt", 'r', encoding="utf8").read())
        sum_ = num_dict[code]
        if sum_ == 0:
            continue
        the_df = pd.read_csv('.\\test\\tf_df\\%s.csv' % code)
        for index in the_df.index:
            line_list = []
            count = [0] * len(code_list)
            word = the_df.loc[index].term
            dcount = the_df.loc[index].df

            line_list.append(word)

            value = dcount / sum_

            count[code_list.index(code)] = value

            line_list.append(value)
            line_list.extend(count)

            word_list.append(tuple(line_list))

    print("=" * 10)
    word_list.sort(key=lambda k: k[0])
    lol = len(word_list)
    new_word_list = list()
    new_word_list.append(word_list[0])
    for i in range(1, lol):
        try:
            if word_list[i][0] == new_word_list[-1][0]:
                new_line = list()
                new_line.append(word_list[i][0])
                for j in range(1, 1 + len(code_list) + 1):
                    new_line.append(word_list[i][j] + new_word_list[-1][j])
                new_word_list.pop(-1)
                new_word_list.append(tuple(new_line))
            else:
                new_word_list.append(word_list[i])
        except:
            print("error")
            pass
    print(new_word_list[0:10])
    print(lol)
    print(len(new_word_list))
    new_word_list.sort(key=lambda k: k[1], reverse=True)
    the_file = open(".\\test\\p_value.csv", 'w', encoding='utf8')
    the_file.write("%s\n" % ",".join(["term", "P"] + code_list))
    for item in new_word_list:
        the_file.write("%s\n" % ",".join([str(i) for i in list(item)]))
    the_file.close()


def get_H():
    '''
    计算H值--领域共识性
    公式1：H(t) = -ΣP(t, Dj)*log(x=P(t, Dj), base=2)
    公式2：P(t, Dj) ≈ f(t, Dj) / Tj

    Dj  领域j
    Tj  j领域的文档数
    f(t, Dj)    t在j领域出现的文档数

    :return:
    '''
    import pandas as pd

    code_list = ["0801", "0802", "0803", "0804", "0805", "0806", "0807", "0808", "0809", "0810",
                 "0811", "0812", "0813", "0814", "0815", "0816", "0817", "0818", "0819", "0820",
                 "0821", "0822", "0823", "0824", "0825", "0826", "0827", "0828", "0829", "0830",
                 "0831", "0832"]

    word_list = []
    for code in code_list:
        num_dict = eval(open(".\\test\\discipline_DF.txt", 'r', encoding="utf8").read())
        sum_ = num_dict[code]
        if sum_ == 0:
            continue
        the_df = pd.read_csv('.\\test\\tf_df\\%s.csv' % code)
        for index in the_df.index:
            line_list = []
            count = [0] * len(code_list)
            word = the_df.loc[index].term
            dcount = the_df.loc[index].df

            line_list.append(word)

            meta_H = get_meta_H(dcount, sum_)

            count[code_list.index(code)] = meta_H

            line_list.append(meta_H)
            line_list.extend(count)

            word_list.append(tuple(line_list))

    print("=" * 10)
    word_list.sort(key=lambda k: k[0])
    lol = len(word_list)
    new_word_list = list()
    new_word_list.append(word_list[0])
    for i in range(1, lol):
        try:
            if word_list[i][0] == new_word_list[-1][0]:
                new_line = list()
                new_line.append(word_list[i][0])
                for j in range(1, 1 + len(code_list) + 1):
                    new_line.append(word_list[i][j] + new_word_list[-1][j])
                new_word_list.pop(-1)
                new_word_list.append(tuple(new_line))
            else:
                new_word_list.append(word_list[i])
        except:
            print("error")
            pass
    print(new_word_list[0:10])
    print(lol)
    print(len(new_word_list))
    new_word_list.sort(key=lambda k: k[1], reverse=True)
    the_file = open(".\\test\\h_value.csv", 'w', encoding='utf8')
    the_file.write("%s\n" % ",".join(["term", "H"] + code_list))
    for item in new_word_list:
        the_file.write("%s\n" % ",".join([str(i) for i in list(item)]))
    the_file.close()


def get_meta_H(f, t):
    import math

    if t <= 0:
        return 0

    return f/t * math.log(t/f, 2)


def get_T(a=0.4, b=0.6, code='0812'):
    '''
    计算领域内候选词的T值
    公式1：
        文档密度 m(t) = tf(t)/df(t)
            tf(t)   t在领域内的频次
            df(t)   t在领域内出现的文档数
    公式2：
        D(t) = α*m(t) + β*(pf(t)/df(t))*(DF/PF)
            α、β 权值参数
            PF  平衡文档数
            DF  领域文档总数
            pf(t)   t在平衡文档的频次
            df(t)   t在领域文档的频次
    公式3：
        T(t) = λ/H(t) + D(t)
            λ   max(H(t))
    :param a: 密集程度权重 α
    :param b: 领域文档和平衡文档的文档差比权重 β
    :param code: 领域代码
    :return:
    '''

    import pandas as pd

    # 读取全部候选术语的H值
    data_h = pd.read_csv('.\\test\\h_value.csv')
    data_h.set_index('term', inplace=True)    # 将term设为索引

    # 读取全部候选术语的平衡文档频次pf
    data_pf = pd.read_csv('.\\test\\pf_df.csv')
    data_pf.set_index('term', inplace=True)    # 将term设为索引

    # 读取候选词文档
    data_term = pd.read_csv('.\\test\\tf_df\\%s.csv' % code)

    # 读取文档分布数据
    data_DF = eval(open('.\\test\\discipline_DF.txt', 'r', encoding='utf8').read())

    DF = data_DF[code]  # 领域内文档总数
    PF = 0  # 平衡文档数
    for w, v in data_DF.items():
        PF += v

    max_H = 0   # 记录领域内词的最大H值

    H_list = []
    D_list = []

    for index in data_term.index:
        term = data_term.loc[index].term
        m_tf = data_term.loc[index].tf
        m_df = data_term.loc[index].df

        # 计算D
        m = m_tf/m_df

        n_pf = data_pf.loc[term]['pf']
        n_df = data_pf.loc[term][code]

        n = n_pf*DF/n_df/PF

        D = a*m + b*n
        D_list.append(D)

        # 获取H
        H = data_h.loc[term].H
        H_list.append(H)

        if H > max_H:
            max_H = H

    data_term['H'] = H_list
    data_term['D'] = D_list
    data_term['T'] = max_H/data_term['H'] + data_term['D']

    data_term.sort_values(by='T', axis=0, ascending=True)

    print(data_term[0:10])

    fw = open('.\\test\\%s_T.csv' % code, 'w', encoding='utf8')
    fw.write("%s\n" % ",".join(["term", "T", "H"]))
    for index, row in data_term.iterrows():
        term = row['term']
        H = row['H']
        T = row['T']

        fw.write("%s,%s,%s\n" % (term, str(T), str(H)))
    fw.close()


def get_regex(code='0812', top=5):
    '''
    计算组成次规则
    :param code:
    :return:
    '''
    import jieba.posseg as pseg

    stop_word = {}.fromkeys(open('.\\dicts\\stopword_base.txt', 'r', encoding='utf8').read().split('\n'), 'ok')

    s_sql = "SELECT id, title, abstract FROM paper_data WHERE discipline=%s"
    data_list = dbs.getDics(s_sql % code)

    regex_dict = dict()

    for data in data_list:
        t_seg = pseg.cut(data["title"])
        d_seg = pseg.cut(data["abstract"])

        t_word = []
        t_flag = []
        d_word = []
        d_flag = []

        for word, flag in t_seg:
            t_word.append(word)
            t_flag.append(flag)

        for word, flag in d_seg:
            d_word.append(word)
            d_flag.append(flag)

        # idx = [i for i in range(len(d_flag)) if d_flag[i] == 'uj' or stop_word.get(d_word[i], "")!=""]
        idx = [i for i in range(len(d_flag)) if stop_word.get(d_word[i], "") != ""]

        s = 0
        e = 0
        for i in idx:
            e = i
            begin, end = get_LCS(t_word, d_word[s: e])
            if e < len(d_flag):
                s = e + 1

            if begin == -1 or end == -1:
                continue
            else:
                s_regex = "+".join(t_flag[begin: end])

            r_list = regex_dict.get(s_regex, [])
            r_list.append("".join(t_word[begin: end]))
            regex_dict[s_regex] = r_list

    fw = open('.\\test\\regex_4.csv', 'w', encoding='utf8')
    fw.write("%s,%s\n" % ("re_s", "sum"))
    for re_s, r_list in regex_dict.items():
        fw.write("%s,%s,%s\n" % (re_s, len(r_list), "/".join(r_list[0:20])))
    fw.close()

    # 取出规则

    import re

    r_li = []
    for i in range(1, 6):
        li = []
        for re_s, r_list in regex_dict.items():
            c = len(r_list)
            l = len(re.findall('\+', re_s))
            if l != i:
                continue
            li.append((re_s, int(c), l))
        li.sort(key=lambda k:k[1], reverse=True)
        print(li[0: top])
        for r in li[0: top]:
            r_li.append(r[0])
    the_file = open('.\\test\\regex_TOP.txt', 'w', encoding='utf8')
    the_file.write("%s" % "\n".join(r_li))
    the_file.close()


def get_LCS(l1, l2):
    m = [[0 for i in range(len(l2) + 1)] for j in range(len(l1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在l1中的最后一位
    for i in range(len(l1)):
        for j in range(len(l2)):
            if l1[i] == l2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    if mmax > 1:
        return p - mmax, p
    else:
        return -1, -1


def get_cTerm(word_list=[], flag_list=[], regex_list=[]):
    import re

    result = []
    s_idx = []
    for regex in regex_list:
        l = len(re.findall('\+', regex)) + 1
        lof = len(flag_list)
        for i in range(0, lof):
            if not i+l <= lof:
                continue
            if "+".join(flag_list[i: i+l]) == regex:
                result.append(("--split--".join(word_list[i: i+l]), regex, l))
                s_idx.extend([j for j in range(i, i+l) if j not in s_idx])

    for idx in s_idx:
        result.append((word_list[idx], flag_list[idx], 1))
    # print(result[0: 5])
    return result


def get_CTerm_seg(code='0812'):
    '''
    根据规则抽取长术语
    :return:
    '''
    import re
    import jieba.posseg as pseg

    # regex_list = open('.\\test\\%s_regex_TOP.txt' % code, 'r', encoding='utf8').read().split('\n')
    regex_list = open('.\\test\\%s_regex_TOP_1.txt' % code, 'r', encoding='utf8').read().split('\n')
    # 生成前缀、后缀规则
    ex_regex = []
    for regex in regex_list:
        r_list = regex.split('+')
        lor = len(r_list)
        if lor < 2:
            continue
        for i in range(1, lor-1):
            new_regex = "+".join(r_list[0: i+1])
            if new_regex not in regex_list and new_regex not in ex_regex:
                ex_regex.append(new_regex)
        for i in range(1, lor-1):
            new_regex = "+".join(r_list[i: lor])
            if new_regex not in regex_list and new_regex not in ex_regex:
                ex_regex.append(new_regex)
    regex_list.extend(ex_regex)
    regex_list = list(set(regex_list))
    print(len(regex_list))
    del ex_regex

    stop_word = {}.fromkeys(open('.\\dicts\\stopword_base.txt', 'r', encoding='utf8').read().split('\n'), 'ok')

    save_flag = ["an", "j", "n", "nz", "vn"]    # 要保留的单词的词性

    s_sql = "SELECT id, title, abstract FROM paper_data WHERE discipline=%s"
    data_list = dbs.getDics(s_sql % code)

    save_compound = dict()  # 保留组合词
    N = 0

    print("*"*10)

    for data in data_list:
        d_seg = pseg.cut(data["title"] + "\n" + data["abstract"])

        d_word = []
        d_flag = []

        for word, flag in d_seg:
            d_word.append(word)
            d_flag.append(flag)

        N += len(d_word)

        index = [i for i in range(len(d_flag)) if d_flag[i] == 'x' or d_flag[i] == 'uj' or stop_word.get(d_word[i], "")!=""]

        s = 0
        for idx in index:
            e = idx
            if s > e:
                break
            result = get_cTerm(d_word[s: e], d_flag[s: e], regex_list=regex_list)

            s = e + 1

            if not result:
                continue

            print(result[0:5])

            for te in result:
                info = save_compound.get(te[0], [0, ""])
                info[0] += 1
                info[1] = te[1]
                save_compound[te[0]] = info

    print("N:%s\n" % N)

    fw_0 = open('.\\test\\C_WORD_3\\%s_C_1.csv' % code, 'w', encoding='utf8')
    fw_1 = open('.\\test\\C_WORD_3\\%s_C_2.csv' % code, 'w', encoding='utf8')
    fw_2 = open('.\\test\\C_WORD_3\\%s_C_3.csv' % code, 'w', encoding='utf8')
    fw_3 = open('.\\test\\C_WORD_3\\%s_C_4.csv' % code, 'w', encoding='utf8')
    fw_4 = open('.\\test\\C_WORD_3\\%s_C_5.csv' % code, 'w', encoding='utf8')
    fw_5 = open('.\\test\\C_WORD_3\\%s_C_6.csv' % code, 'w', encoding='utf8')
    fw_0.write('term,regex,f\n')
    fw_1.write('term,regex,f\n')
    fw_2.write('term,regex,f\n')
    fw_3.write('term,regex,f\n')
    fw_4.write('term,regex,f\n')
    fw_5.write('term,regex,f\n')

    head_tail = dict()

    for k, v in save_compound.items():
        l = len(re.findall(pattern=r'--split--', string=k))
        if l == 0:
            fw_0.write("%s,%s,%s\n" % (k, v[1], str(v[0])))
        elif l == 1:
            fw_1.write("%s,%s,%s\n" % (k, v[1], str(v[0])))
        elif l == 2:
            fw_2.write("%s,%s,%s\n" % (k, v[1], str(v[0])))
        elif l == 3:
            fw_3.write("%s,%s,%s\n" % (k, v[1], str(v[0])))
        elif l == 4:
            fw_4.write("%s,%s,%s\n" % (k, v[1], str(v[0])))
        elif l == 5:
            fw_5.write("%s,%s,%s\n" % (k, v[1], str(v[0])))

        k_list = k.split('--split--')
        k_l = len(k_list)
        for i in range(0, k_l - 1):
            w = '--split--'.join(k_list[0: i+1])
            if save_compound.get(w, "") == "" and head_tail.get(w, "") == "":
                head_tail[w] = 'ok'
        for i in range(2, k_l):
            w = '--split--'.join(k_list[i: k_l])
            if save_compound.get(w, "") == "" and head_tail.get(w, "") == "":
                head_tail[w] = 'ok'

    fw_0.close()
    fw_1.close()
    fw_2.close()
    fw_3.close()
    fw_4.close()
    fw_5.close()

    fw = open('.\\test\\C_WORD_3\\other_word.csv', 'w', encoding='utf8')
    fw.write('term\n')
    for k, v in head_tail.items():
        fw.write('%s\n' % k)
    fw.close()


def get_DR(code='0812'):
    '''
    计算领域相关性

    公式1：DR(t, Dj) = P(t, Di)/ΣP(t, D)
    D   所有领域
    :return:
    '''

    import pandas as pd

    # 读取P值文件
    p_df = pd.read_csv('.\\test\\p_value.csv')
    p_df.set_index('term', inplace=True)

    # 读取候选词文档
    data_term = pd.read_csv('.\\test\\tf_df\\%s.csv' % code)

    DR_list = []

    for index in data_term.index:
        term = data_term.loc[index].term

        p_sum = p_df.loc[term]['P']
        p = p_df.loc[term][code]

        DR_list.append(p/p_sum)

    data_term['DR'] = DR_list

    print(data_term[0:10])

    fw = open('.\\test\\%s_DR.csv' % code, 'w', encoding='utf8')
    fw.write("%s\n" % ",".join(["term", "DR"]))
    for index, row in data_term.iterrows():
        term = row['term']
        DR = row['DR']

        fw.write("%s,%s\n" % (term, str(DR)))
    fw.close()


def get_DC(code="0812"):
    '''
    计算领域共识性DC
    :param code:
    :return:
    '''
    import pandas as pd
    import numpy as np
    import math

    # 读取P值文件
    p_df = pd.read_csv('.\\test\\p_value.csv')
    p_df.set_index('term', inplace=True)

    # 读取候选词文档
    data_term = pd.read_csv('.\\test\\tf_df\\%s.csv' % code)

    DC_list = []

    for index in data_term.index:
        term = data_term.loc[index].term

        h = 0.0

        for c in code_list:
            p = p_df.loc[term][c]
            if p == 0:
                continue
            h += p*math.log(1/p, 2)

        DC_list.append(h)
    data_term['DC'] = DC_list

    print(data_term[0:10])

    fw = open('.\\test\\%s_DC.csv' % code, 'w', encoding='utf8')
    fw.write("%s\n" % ",".join(["term", "DC"]))
    for index, row in data_term.iterrows():
        term = row['term']
        DC = row['DC']

        fw.write("%s,%s\n" % (term, str(DC)))
    fw.close()


def get_tf_idf():
    pass


def get_logL(p, k, n):
    import math
    return k*math.log(p, 2)+(n-k)*math.log(1-p, 2)


def get_log_f(N=9840397, n=2, sum_x=0, sum_y=0, f_1n=0):

    f_1n = f_1n/N
    avy = sum_y/(n-1)
    avx = sum_x/(n-1)

    kf1 = f_1n
    kf2 = avy - kf1
    nf1 = avx
    nf2 = N - nf1

    return 2*(get_logL(kf1/nf1, kf1, nf1) + get_logL(kf2/nf2, kf2, nf2) - get_logL((kf1+kf2)/(nf1+nf2), kf1, nf1) - get_logL((kf1+kf2)/(nf1+nf2), kf2, nf2))


def get_likelihood(code='0812'):
    import pandas as pd

    word_length = [2, 3, 4, 5, 6]
    # word_length = [2]
    for length in word_length:
        data_df = pd.read_csv('.\\test\\C_WORD_3\\%s_C_%s.csv' % (code, str(length)))
        sum_x = [0] * len(data_df)
        sum_y = [0] * len(data_df)

        for ll in range(1, length):
            word_dict = pd.read_csv('.\\test\\C_WORD_3\\%s_C_%s.csv' % (code, str(ll)))

            word_dict.set_index('term', inplace=True)
            for index in data_df.index:
                term = data_df.loc[index]['term']

                t_list = term.split('--split--')

                lot = len(t_list)

                w = '--split--'.join(t_list[0: 0+ll])
                if w == "NA":
                    x = 11
                elif w == "null":
                    x = 3
                elif w == "NULL":
                    x = 3
                else:
                    x = word_dict.loc[w]['f']
                sum_x[index] += x

                w = '--split--'.join(t_list[lot-ll: lot])
                if w == "NA":
                    y = 11
                elif w == "null":
                    y = 3
                elif w == "NULL":
                    y = 3
                else:
                    y = word_dict.loc[w]['f']
                sum_y[index] += y
        data_df['sum_x'] = sum_x
        data_df['sum_y'] = sum_y

        print(data_df[0:10])
        print("*"*10)

        data_df.to_csv('.\\test\\C_WORD_3\\%s_%s_result.csv' % (code, str(length)), index=None)


def word_filter(code="0812"):
    print("word_filter")
    import pandas as pd

    regex_list = open('.\\test\\%s_regex_TOP_1.txt' % code, 'r', encoding='utf8').read().split('\n')

    word_length = [2, 3, 4, 5, 6]
    # word_length = [2]
    for length in word_length:
        data_df = pd.read_csv('.\\test\\C_WORD_3\\%s_%s_result.csv' % (code, str(length)))
        term_list = []
        f_list = []
        r_list = []
        likelihood_list = []
        for index in data_df.index:
            term = data_df.loc[index]['term']
            f = data_df.loc[index]['f']
            sum_x = data_df.loc[index]['sum_x']
            sum_y = data_df.loc[index]['sum_y']
            regex = data_df.loc[index]['regex']

            if regex not in regex_list:
                continue
            likelihood = get_log_f(n=length, sum_x=sum_x, sum_y=sum_y, f_1n=f)
            term_list.append(term)
            f_list.append(f)
            r_list.append(regex)
            likelihood_list.append(likelihood)
        new_df = pd.DataFrame()
        new_df['term'] = term_list
        new_df['f'] = f_list
        new_df['regex'] = r_list
        new_df['likelihood'] = likelihood_list
        print(new_df[0: 10])
        new_df.to_csv('.\\test\\C_WORD_3\\%s_%s_likelihood.csv' % (code, str(length)), index=None)


def get_C_Value(code='0812'):
    """
    计算候选串的C-value值
    :param code:
    :return:
    """
    import pandas as pd
    import math

    stop_word = {}.fromkeys(open('.\\test\\%s_stop.txt' % code, 'r', encoding='utf8').read().split('\n'), "ok")

    # word_length = [1]
    word_length = [6, 5, 4, 3, 2, 1]
    word_dict = {}.fromkeys(open('.\\test\\C_WORD_3\\word_dict.txt', 'r', encoding='utf8').read().split('\n'), [0, 0])  # 记录词的母串个数和作为嵌套串出现的频次
    for length in word_length:
        data_df = pd.read_csv('.\\test\\C_WORD_3\\%s_%s_likelihood.csv' % (code, str(length)))
        c_value_list = []
        term_list = []
        f_list = []
        likelihood_list = []
        regex_list = []
        for index in data_df.index:
            term = str(data_df.loc[index]['term'])
            f = data_df.loc[index]['f']
            likelihood = data_df.loc[index]['likelihood']
            regex = data_df.loc[index]['regex']

            if len(term) < 2:
                continue
            if stop_word.get(term, "") == "ok":
                continue

            if likelihood < 0.1:
                continue

            s_t = word_dict.get(term, [0, 0])

            if length == 6 or s_t == [0, 0]:
                c_value = math.log(length*f, 2)
            else:
                x = length*(f - s_t[0]/s_t[1])
                if x == 0:
                    x = 10e-9
                    print(f, s_t, math.log(x, 2))
                c_value = math.log(x, 2)
            c_value_list.append(c_value)
            term_list.append(term)
            f_list.append(f)
            likelihood_list.append(likelihood)
            regex_list.append(regex)

            split_list = term.split('--split--')
            los = len(split_list)

            if los < 2:
                continue
            for i in range(0, los - 1):
                key_word = "--split--".join(split_list[0: i + 1])
                key_s_t = word_dict.get(key_word, [0, 0])
                key_s_t[0] += 1
                key_s_t[1] += f
                word_dict[key_word] = key_s_t
            for i in range(1, los - 1):
                key_word = "--split--".join(split_list[i: los])
                key_s_t = word_dict.get(key_word, [0, 0])
                key_s_t[0] += 1
                key_s_t[1] += f
                word_dict[key_word] = key_s_t

        new_df = pd.DataFrame()
        new_df['term'] = term_list
        new_df['f'] = f_list
        new_df['regex'] = regex_list
        new_df['likelihood'] = likelihood_list
        new_df['c_value'] = c_value_list

        new_df = new_df.sort_values(by='c_value', axis=0, ascending=False)

        new_df.to_csv('.\\test\\C_WORD_3\\%s_%s_c_value.csv' % (code, str(length)), index=None)

        print("*"*10)


def get_top(code='0812', top=100000, min_c_value=4.75):
    import pandas as pd
    import re

    stop_word = {}.fromkeys(open('.\\test\\%s_stop.txt' % code, 'r', encoding='utf8').read().split('\n'), "ok")
    regex_dict = {}.fromkeys(open('.\\test\\%s_regex_stop.txt' % code, 'r', encoding='utf8').read().split('\n'), "ok")

    word_length = [6, 5, 4, 3, 2, 1]
    # word_length = [4, 3, 2]

    term_list = []
    split_list = []
    c_value_list = []
    regex_list = []
    ll_list = []
    f_list = []
    for length in word_length:
        data_df = pd.read_csv('.\\test\\C_WORD_3\\%s_%s_c_value.csv' % (code, str(length)))
        for index in data_df.index:
            split_term = data_df.loc[index]['term']
            c_value = data_df.loc[index]['c_value']
            regex = data_df.loc[index]['regex']
            ff = data_df.loc[index]['f']
            if type(split_term) == float or type(split_term) == int:
                continue
            if len(split_term) < 2:
                continue
            if stop_word.get(split_term, "") == "ok":
                continue
            if regex_dict.get(regex, "") == "ok":
                continue
            if c_value < min_c_value:
                continue
            term = re.sub('--split--', '', split_term)

            term_list.append(term)
            split_list.append(split_term)
            c_value_list.append(c_value)
            regex_list.append(regex)
            ll_list.append(str(length))
            f_list.append(ff)

    new_df = pd.DataFrame()
    new_df['term'] = term_list
    new_df['split'] = split_list
    new_df['regex'] = regex_list
    new_df['length'] = ll_list
    new_df['f'] = f_list
    new_df['c_value'] = c_value_list
    new_df = new_df.sort_values(by='c_value', axis=0, ascending=False)

    # new_df[0: top].to_csv('.\\test\\C_WORD_3\\%s_result_%s_1.csv' % (code, str(top)), index=None)
    new_df.to_csv('.\\test\\C_WORD_3\\%s_result_%s.csv' % (code, str(min_c_value)), index=None)

    pass


def LIKELIHOOD():
    '''
    计算似然比
    :return:
    '''
    # get_CTerm_seg()
    # get_likelihood()
    word_filter()
    pass


def C_VALUE():
    '''
    计算C-value
    :return:
    '''
    get_C_Value()
    # get_top()
    pass


if __name__ == "__main__":

    # regex_list = ['n+n', 'v+n', 'n+v',
    #               'n+n+n', 'n+v+n', 'n+n+v',
    #               'n+n+n+n', 'n+n+v+n', 'n+n+vn+n',
    #               'n+n+n+n+n', 'n+n+n+vn+n']

    code_list = ["0801", "0802", "0803", "0804", "0805", "0806", "0807", "0808", "0809", "0810",
                 "0811", "0812", "0813", "0814", "0815", "0816", "0817", "0818", "0819", "0820",
                 "0821", "0822", "0823", "0824", "0825", "0826", "0827", "0828", "0829", "0830",
                 "0831", "0832"]

    # get_tf_df()
    # get_pf()
    # get_H()
    # get_T()

    # get_P()
    # get_DR()
    # get_DC()

    get_regex(top=5)

    # LIKELIHOOD()

    # C_VALUE()

    pass
