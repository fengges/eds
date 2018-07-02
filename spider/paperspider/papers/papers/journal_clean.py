from spider.paperspider.papers.papers.dbutils import dbs
import os

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def strip_name():
    sql = "select * from journal_old"
    journal_list = dbs.getDics(sql)
    update_list = []
    for j in journal_list:
        en_name = j["en_name"].strip()
        cn_name = j["cn_name"].strip()
        former_name = j["former_name"].strip()
        if en_name != j["en_name"] or cn_name != j["cn_name"] or former_name != j["former_name"]:
            update_list.append((en_name, cn_name, former_name, j["_id"]))
    update_sql = "update journal_old set en_name=%s, cn_name=%s, former_name=%s where _id=%s"
    print(dbs.exe_many(update_sql, update_list))


def clean_duplicate():
    sql = "select * from journal"
    journal_list = dbs.getDics(sql)
    print(len(journal_list))
    di = dict()
    id_weight = dict()
    for j in journal_list:
        name_list = list()
        name_list.append(j["en_name"])
        name_list.append(j["cn_name"])
        name_list.extend(j["former_name"].split(';'))
        name_list = [i for i in name_list if i != ""]
        s = 0
        if j["IF"] != "":
            s += 1
        if j["ave_if"] != "":
            s += 1
        if j["cited_num"] != "":
            s += 1
        if j["self_cited_rate"] != "":
            s += 1
        id_weight[str(j["_id"])] = s
        for name in name_list:
            di[name] = (di.get(name, "") + ";" + str(j["_id"])).strip(";")
        pass
    d = di
    drop_list = []
    for w, k in d.items():
        if len(k.split(';')) > 1:
            id_list = k.split(';')
            max_id = id_list[0]
            for i in range(1, len(id_list)):
                print(id_list[i])
                if id_weight[str(max_id)] <= id_weight[str(id_list[i])]:
                    max_id = id_list[i]
            drop_list.extend([i for i in id_list if i != max_id])
    print(len(drop_list))

    drop_sql = "delete from journal where _id=%s"
    print(dbs.exe_many(drop_sql, drop_list))


def journal2dict():
    sql = "select * from journal"
    r_list = dbs.getDics(sql)
    journal_dict = dict()
    for j in r_list:
        name_list = list()
        name_list.append(j["en_name"])
        name_list.append(j["cn_name"])
        name_list.extend(j["former_name"].split(';'))
        name_list = [i for i in name_list if i != ""]
        for name in name_list:
            journal_dict[name] = j["_id"]
    import json
    fw = open(root + "\\dicts\\journal_dict.txt", "w", encoding='utf8')
    fw.write(json.dumps(journal_dict, "utf-8"))
    fw.close()


def paper_journal():
    journal_dict = eval(open(root + "\\dicts\\journal_dict.txt", "r", encoding='utf8').read())

    update_list = []
    sql = "select * from paper"
    papers = dbs.getDics(sql)
    for paper in papers:
        org = my_strip(paper["org"])
        update_list.append((org, journal_dict.get(org, ""), paper["id"]))
    update_sql = "update paper set org=%s, journal_id=%s where id=%s"
    print(update_list)
    print(len(update_list))
    print(len([i for i in update_list if i[0] != ""]))
    print(dbs.exe_many(update_sql, update_list))


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


if __name__ == "__main__":
    # strip_name()
    # clean_duplicate()
    paper_journal()
    pass
