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
    begin = 0
    step = 10000

    num = 0
    s_num = 0
    while begin + step <= 500000:
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
        i_sql = "insert into paper_50_clean_1 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s)"
        print(len(update_list))
        print(dbs.exe_many(i_sql, update_list))
        print("=" * 10)
        begin += step
    print(num)
    print(s_num)
    pass


if __name__ == "__main__":
    # strip_name()
    # clean_duplicate()
    clean_by_author_org()
    pass
