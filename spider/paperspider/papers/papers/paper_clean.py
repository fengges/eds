"""
英文论文清洗

### 数据特点 ###
    1.name字段:论文标题
        a.部分数据 标题不全 --- 重新获取 ---
    2.abstract字段:论文摘要
        a.部分数据 摘要不全 --- 重新获取 ---
    3.author字段:包含作者和对应机构信息
        a.部分数据 作者没有对应机构   --- 删除 ---
        b.部分数据 author中不包含author_id对应的老师   --- 删除 ---
        c.部分数据 author字段的作者名是简称   --- 重新获取 ---
    4.org字段:期刊
        a.部分数据 不是SCI和EI期刊   --- 删除 ---
        b.部分数据 期刊名称不全   --- 全匹配或者匹配一半 ---
        c.部分数据 没有期刊   --- 删除 ---

### 清洗步骤 ###
    1.根据org字段
    2.根据author字段
    3.根据paper_md5字段去重
"""

import re
from spider.paperspider.papers.papers.dbutils import dbs
import os
from spider.paperspider.papers.papers.cn2en import name2en


def paper_journal():
    # db = Mysql()
    # root = os.path.dirname(os.path.abspath(__file__))
    # journal_dict = eval(open(root + "\\data\\journal_dict.txt", "r", encoding='utf8').read())
    #
    # i = 0
    # b = 100000
    # num = db.getPaperNum()['count(*)']
    # yu = num % b
    # while i < num:
    #     if i == num - yu: b = yu
    #     update_list = []
    #     org_list = []
    #     papers = db.getPaperOrg(i,b)
    #     print("获取paper:", i, b)
    #     for paper in papers:
    #         org = my_strip(paper["org"])
    #         org_id = journal_dict.get(org, -1)
    #         if org_id == -1:
    #             org_list.append(org)
    #         update_list.append((org, org_id, paper["id"]))
    #     fw = open(root + "\\data\\unknow_journal_list.txt", "a", encoding='utf8')
    #     fw.write("\n".join(org_list))
    #     fw.close()
    #     db.UpdateOrg(update_list)
    #     i += b
    pass


def my_strip(str=""):
    # 去除字符串中空格和其他字符
    import re
    text = re.sub(r'\u00a0', ' ', str)
    re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r', '《', '》', '...']
    while len(text) > 0 and text[0] in re_list:
        text = text.lstrip(text[0])
    while len(text) > 0 and text[-1] in re_list:
        text = text.rstrip(text[-1])
    return text
    pass


def clean_by_author_org():
    p_list = "select * from paper_new where _id>=%d and _id<%d"
    begin = 500000
    step = 10000

    num = 0
    s_num = 0
    while begin + step <= 1400000:
        update_list = []
        search_list = dbs.getDics(p_list % (begin, begin + step))
        print(begin, begin + step)
        num += len(search_list)
        for s in search_list:
            try:
                author = eval(s["author"])
            except:
                li = s["author"].split(",")
                c = 0
                for i in li:
                    if re.findall(r'org', i) and len(i) > 8:
                        c += 1
                if c == 0:
                    print("删除", s["_id"])
                    s_num += 1
                    continue
                else:
                    update_list.append(
                        (s["_id"], s["name"], s["url"], s["abstract"], s["org"], s["year"], s["cited_num"],
                         s["source"], s["source_url"], s["keyword"], s["author"], s["author_id"], s["cited_url"],
                         s["reference_url"], s["paper_md5"], "0"))
                    continue
            if type(author) == dict:
                author_list = author.get("author")
            else:
                author_list = author
            c = 0
            for a in author_list:
                if a.get("org", "") != "":
                    c += 1
            if c == 0:
                print("删除", s["_id"])
                s_num += 1
                continue
            update_list.append((s["_id"], s["name"], s["url"], s["abstract"], s["org"], s["year"], s["cited_num"],
                               s["source"], s["source_url"], s["keyword"], s["author"], s["author_id"], s["cited_url"],
                               s["reference_url"], s["paper_md5"], "0"))
        i_sql = "insert into paper_90_clean_1 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s)"
        print(len(update_list))
        print(dbs.exe_many(i_sql, update_list))
        print("=" * 10)
        begin += step
    print(num)
    print(s_num)
    pass


def clean_select_name():
    """
    search = 1
        姓名
    :return:
    """
    p_list = "SELECT _id, author, author_id, teacher_ins.name as author_name, teacher_ins.school as school, teacher_ins.institution as institution FROM paper_english, teacher_ins WHERE paper_english.author_id = teacher_ins.id and _id > 14547"
    paper_list = dbs.getDics(p_list)
    print(len(paper_list))
    num = 0
    update_list = []
    for paper in paper_list:
        author_list = str2list(paper["author"])

        cn_name = name2en(paper["author_name"])
        this_author = []
        for author in author_list:
            en_name = "".join(re.findall(r'[a-zA-Z]+', author["name"])).lower()
            if en_name in cn_name or author["name"] == paper["author_name"]:
                this_author.append(author)
        if this_author:
            author_str = str(this_author)
            update_list.append((paper["_id"], paper["author"], paper["author_id"], author_str, paper["author_name"], paper["school"], paper["institution"], 1))
            num += 1
    #     if len(update_list) == 1000:
    #         i_sql = "insert paper_ins(_id, author, author_id, author_cn, author_name, school, institution, search) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    #         print(dbs.exe_many(i_sql, update_list))
    #         update_list = []
    #
    # if update_list:
    #     i_sql = "insert paper_ins(_id, author, author_id, author_cn, author_name, school, institution, search) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    #     print(dbs.exe_many(i_sql, update_list))

    print(num)


def str2list(s=""):
    try:
        author_list = eval(s)
        if type(author_list) == dict:
            author_list = author_list["author"]
    except:
        a_list = re.findall(r'\{"name":.*?\}|\{"org":.*?\}', s)
        author_list = []
        for item in a_list:
            name = re.findall(r'"name":.*?\}|"name":.*?,', item)[0].split(":")
            name_value = my_strip_1(name[1])
            org = re.findall(r'"org".*?\}|"org".*?,', item)[0].split(":")
            org_value = my_strip_1(org[1])

            d = dict()
            d["name"] = name_value
            d["org"] = org_value
            author_list.append(d)

    return author_list


def my_strip_1(text=""):
    re_list = [':', '{', '}', ',']
    while len(text) > 0 and text[0] in re_list:
        text = text.lstrip(text[0])
    while len(text) > 0 and text[-1] in re_list:
        text = text.rstrip(text[-1])
    return text


def clean_select_school():
    """
    search = 2
        学校
    :return:
    """
    p_list = "SELECT * FROM paper_ins"
    paper_list = dbs.getDics(p_list)
    print(len(paper_list))
    num = 0
    update_list = []
    for paper in paper_list:
        author_list = str2list(paper["author_cn"])

        en_name_list = [i.lower() for i in paper["en_school"].split(',')]
        flag = 0
        for author in author_list:
            if author["org"] == "":
                continue
            org_name = author["org"].lower()
            for i in en_name_list:
                if re.findall(i, org_name):
                    flag = 2
        if flag == 2:
            update_list.append((2, paper["_id"]))
            print(author_list, en_name_list)
            num += 1

        if len(update_list) == 1000:
            u_sql = "update paper_ins set search=%s where _id =%s"
            print(dbs.exe_many(u_sql, update_list))
            update_list = []

    if update_list:
        u_sql = "update paper_ins set search=%s where _id =%s"
        print(dbs.exe_many(u_sql, update_list))

    print(num)


def clean_select_ins():
    """
    search = 3
        机构
    :return:
    """
    p_list = "SELECT * FROM paper_ins"
    paper_list = dbs.getDics(p_list)
    print(len(paper_list))
    num = 0
    update_list = []
    for paper in paper_list:
        cn_org = paper["cn_org"]
        school = paper["school"]
        ins = paper["institution"]
        if not cn_org:
            continue
        ins = "".join(re.findall(r'[\u4E00-\u9FA5]+', ins))
        school = "".join(re.findall(r'[\u4E00-\u9FA5]+', school))
        cn_org = "".join(re.findall(r'[\u4E00-\u9FA5]+', cn_org))
        if re_include(cn_org, school):
            if ins != "" and ins is not None:
                if re_include(cn_org, ins) or include(cn_org, ins):
                    update_list.append((3, paper["_id"]))
                    print("%s,%s,%s:%d" % (cn_org, school, ins, 3))
            elif include(cn_org, school) and re.findall(r'研究院|研究所', school):
                update_list.append((3, paper["_id"]))
                print("%s,%s,%s:%d" % (cn_org, school, ins, 3))
            else:
                # update_list.append((2, paper["_id"]))
                print("%s,%s,%s:%d" % (cn_org, school, ins, 2))
            num += 1
        else:
            # print(cn_org, ins + school)
            pass
        if len(update_list) == 1000:
            u_sql = "update paper_ins set search=%s where _id =%s"
            print(dbs.exe_many(u_sql, update_list))
            update_list = []

    if update_list:
        u_sql = "update paper_ins set search=%s where _id =%s"
        print(dbs.exe_many(u_sql, update_list))

    print(num)
    pass


def include(a, b):
    if len(a) > len(b):
        lista = set(a)
        listb = set(b)
    else:
        lista = set(b)
        listb = set(a)
    c = len(lista)-len(listb)
    if len(lista-listb) <= c:
        return True
    else:
        return False


def re_include(a, b):

    if re.findall(a, b) or re.findall(b, a):
        return True
    else:
        return False


# def


if __name__ == "__main__":
    # strip_name()
    # clean_duplicate()
    # clean_by_author_org()
    clean_select_name()
    # clean_select_school()
    # clean_select_ins()
    pass
