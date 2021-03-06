import re
import json
from algorithm.li.extract.utils.dbutils import dbs

from algorithm.li.extract.templates.tag_template import *


# 去除没有信息的标签和格式字符串
def f():

    select_sql = "SELECT id, name, html FROM `eds_985teacher` WHERE school = '清华大学';"
    teacher_list = dbs.getDics(select_sql)
    print(len(teacher_list))
    update_list = []
    for teacher in teacher_list:
        if teacher["html"] is None or teacher["html"] == "":
            continue
        html = teacher["html"]
        html = re.sub(reTRIM_closing.format("style"), "", html)
        html = re.sub(reTRIM_closing.format("style".upper()), "", html)
        html = re.sub(reTRIM_closing.format("script"), "", html)
        html = re.sub(reTRIM_closing.format("script".upper()), "", html)
        html = re.sub(reTRIM_closing.format("head"), "", html)
        html = re.sub(reTRIM_closing.format("head".upper()), "", html)
        html = re.sub(reCOMM, "", html)
        for re_tag in inline_tags:
            html = re.sub(re_tag, "", html)

        name = re.sub('（', '(', teacher["name"])
        name = re.sub('）', ')', name)
        name = re.sub('\(.*?\)', '', name)
        text_list = cut_blocks(html, re_list=[r'个人简介|个人简历', name])
        if not text_list:
            continue
        text = "\n".join(text_list)
        if text:
            print(teacher["id"])
            update_list.append((text, teacher["id"]))
        if len(update_list) == 1000:
            update_sql = "update eds_985teacher set info=%s where id=%s"
            print("插入……1000")
            print(dbs.exe_many(update_sql, update_list))
            update_list = []
    if update_list:
        update_sql = "update eds_985teacher set info=%s where id=%s"
        print("插入……%s" % len(update_list))
        print(dbs.exe_many(update_sql, update_list))
    pass


def cut_blocks(html="", re_list=[]):
    text_list = get_text(html)
    if not text_list:
        return
    start = 0
    end = 20 if len(text_list) > 20 else len(text_list)
    for i in range(0, end):
        for r in re_list:
            try:
                if re.findall(r, text_list[i]):
                    start = i
                    break
            except:
                print(text_list[i])
                pass

        if start != 0:
            text_list = text_list[start:]
            break

    return text_list


def get_text(html=""):
    if html == "":
        return
    for tag in block_tags:
        html = re.sub(tag, '\n', html)

    html = re.sub(r'。', '。\n', html)
    html = re.sub(r'；', '；\n', html)
    html = re.sub(r';', ';\n', html)
    t_list = html.split('\n')
    t_list = [my_strip(i) for i in t_list]
    t_list = [i for i in t_list if i != ""]

    return t_list


# 去除字符串中空格和其他字符
def my_strip(text=""):
    text = re.sub(r'\u00a0', ' ', text)
    re_list = ['\n', '\t', ' ', '\u3000', '\xa0', '\r']
    while len(text) > 0 and text[0] in re_list:
        text = text.lstrip(text[0])
    while len(text) > 0 and text[-1] in re_list:
        text = text.rstrip(text[-1])
    return text


def clear_1():
    """
    # 去除有工作描述的句子，没有工作经历的去除生日年份
    # 去除与出版信息有关的句子
    :return:
    """
    s_sql = "select id, edu_exp from teacher_eduexp where type = 2"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))

    re_title = r'讲师|教授|指导|博士生导师|研究生导师|硕士生导师|从事|研究员|所长|院长|博导|硕导'
    re_job = r'任教|任|从事'
    re_publish = r'《|》|出版|学报|杂志'
    re_birth = r'[1-2][9,0][0-9]{2}生|出生|生于'

    update_list = []
    num = 0
    for teacher in teacher_list:
        lines = teacher["edu_exp"].split('\n')
        new_lines = []
        for line in lines:
            line = re.sub(r'教 授', "教授", line)
            line = re.sub(r'讲 师', "讲师", line)
            line = re.sub(r'学 士', "学士", line)
            line = re.sub(r'博 士', "博士", line)
            line = re.sub(r'硕 士', "硕士", line)
            if re.findall(re_birth, line):
                continue
            if re.findall(re_job, line):
                continue
            if re.findall(re_title, line):
                if len(re.findall(r'学位|学士|硕士|博士|进修|硕博', line)) == 0:
                    continue
                elif (len(re.findall(r'博士', line)) == 1 and len(re.findall(r'博士生导师', line)) == 1) or (len(re.findall(r'硕士', line)) == 1 and len(re.findall(r'硕士生导师', line)) == 1):
                    continue
            if re.findall(re_publish, line) and len(re.findall(r'博士|硕士|学士|本科|研究生|访问学者|博士后|获|毕业|进修|学习|学位|直博|访问|MSW|硕博', line)) == 0:
                continue
            if re.findall(r'博士|硕士|学士|本科|研究生|访问学者|博士后|获|毕业|进修|学习|学位|直博|访问|MSW|硕博', line):
                new_lines.append(line)
            pass
        t1 = '\n'.join(lines)
        t2 = '\n'.join(new_lines)
        if t1 != t2:
            print(teacher["id"])
            print(t1)
            print('-' * 10)
            print(t2)
            print('-' * 10)
            num += 1
            if num % 1000 == 0:
                print()
        update_list.append(('\n'.join(new_lines), 2, teacher["id"]))

    print(num)
    print(len(update_list))
    update_sql = "update teacher_eduexp set exp_clear = %s, clear=%s where id = %s"
    # print(dbs.exe_many(update_sql, update_list))


def clear_2():
    """
    保留只包含学历信息的句子
    :return:
    """
    s_sql = "select id, edu_exp from teacher_eduexp where type = 2"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))

    re_title = r'讲师|教授|指导|博士生导师|研究生导师|硕士生导师|从事|研究员|所长|院长|博导|硕导'
    re_job = r'任教|任|从事|留校|留院'
    re_publish = r'《|》|出版|学报|杂志'
    re_birth = r'[1-2][9,0][0-9]{2}生|出生|生于|年生'

    update_list = []
    num = 0
    for teacher in teacher_list:
        if teacher["edu_exp"] == "" or teacher["edu_exp"] is None:
            continue
        lines = teacher["edu_exp"].split('\n')
        new_lines = []
        for line in lines:
            if re.findall(re_title, line):
                continue
            if re.findall(re_job, line):
                continue
            if re.findall(re_publish, line):
                continue
            if re.findall(re_birth, line):
                continue
            new_lines.append(line)
        if new_lines:
            print(teacher["id"])
            num += 1
            update_list.append(('\n'.join(new_lines), 2, teacher["id"]))

    print(num)
    print(len(update_list))
    update_sql = "update teacher_eduexp set exp_clear = %s, clear=%s where id = %s"
    print(dbs.exe_many(update_sql, update_list))


def clear_3():
    """
    清洗ne字段：补全date，部分没有date的，实体识别将date识别为organization
    如果date为空
    :return:
    """
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ne != ''"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    for teacher in teacher_list:
        ne_list = eval(teacher["ne"])
        flag = 0
        for i in range(0, len(ne_list)):
            date = ne_list[i].get("date", "")
            org = ne_list[i].get("org", "")
            new_date_list = []
            new_org_list = []
            if date == "" and org != "" and re.findall(r'[1-2][9,0][0-9]{2}', org):
                org_list = org.split(';')
                for org in org_list:
                    the_org_list = re.findall(r'[\u4E00-\u9FA5]+', org)
                    if not the_org_list:
                        new_org_list.append(org)
                        continue
                    new_org = the_org_list[0]
                    if re.findall(r'^年', new_org):
                        new_org = re.sub(r'^年', "", new_org)
                    new_date = re.sub(new_org, "", org)
                    new_date_list.append(new_date)
                    new_org_list.append(new_org)
            if new_date_list:
                ne_list[i]["date"] = ";".join(new_date_list)
                ne_list[i]["org"] = ";".join(new_org_list)
                flag = 1
        if flag == 1:
            print("-" * 10)
            print(teacher["id"])
            print(eval(teacher["ne"]))
            print("-" * 3)
            print(ne_list)
            print("-" * 10)
            update_list.append((str(ne_list), teacher["id"]))

    u_sql = "update teacher_eduexp set ne = %s where id = %s"
    print(len(update_list))
    # print(dbs.exe_many(u_sql, update_list))


def clear_7():
    """
    :return:
    """
    # s_sql = "select id, ne, exp_clear from teacher_eduexp where ne != '' and id < 1000"
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ne != '' and type=1 and ok = 0 limit 1000"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    num = 0
    for teacher in teacher_list:
        exp_list = teacher["exp_clear"].split('\n')
        ne_list = eval(teacher["ne"])
        if not ne_list:
            continue
        flag = 1
        print(teacher["id"])
        print(teacher["exp_clear"])
        for i in range(0, len(ne_list)):
            if not ne_list[i]:
                continue
            degree_list = ne_list[i].get("degree", "").split(';')
            org_list = ne_list[i].get("org", "").split(';')
            date_list = ne_list[i].get("date", "").split(';')
            degree_list = [i for i in degree_list if i != ""]
            org_list = [i for i in org_list if i != ""]
            date_list = [i for i in date_list if i != ""]

            org = ne_list[i].get("org", "")
            d = re.findall('[0-9\-年\.月－～~—/]{4,}', org)
            if len(d) == 1:
                exp = re.sub(r' ', '', exp_list[i])
                da = re.findall(r'[0-9\-年\.月－～~\—―/]{4,}', exp)
                if len(da) > 1:
                    # org = re.sub(r'[0-9\-年\.月－～~——/]{4,}', '', org)
                    # ne_list[i]["org"] = org
                    # ne_list[i]["date"] = da[0]
                    print(da)
                    print(exp)
                    flag = 1

        # if flag == 1:
        #     print(teacher["id"])
        #     # print(teacher["exp_clear"])
        #     # print(eval(teacher["ne"]))
        #     print(ne_list)
        #     # update_list.append((str(ne_list), teacher["id"]))
        #     update_list.append(teacher["id"])
        #     print('-' * 10)
        #     num += 1

    # print(num)
    # print(len(update_list))
    # u_sql = "update teacher_eduexp set ne = %s, ok = 1 where id = %s"
    # u_sql = "update teacher_eduexp set ne = %s where id = %s"
    # u_sql = "update teacher_eduexp set ok = 1 where id = %s"
    # print(dbs.exe_many(u_sql, update_list))


def show_data():
    """
    :return:
    """
    # s_sql = "select id, ne, exp_clear from teacher_eduexp where ne != '' and id < 1000"
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ok = 1"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    num = 0
    for teacher in teacher_list:
        exp_list = teacher["exp_clear"].split('\n')
        ne_list = eval(teacher["ne"])
        if not ne_list:
            continue
        flag = 0
        for i in range(0, len(ne_list)):
            if not ne_list[i]:
                continue
            degree = ne_list[i].get("degree", "")
            org = ne_list[i].get("org", "")
            if degree == "毕业" and org == "":
                flag = 1
                print(ne_list[i])
        if flag == 1:
            num += 1

    print(num)


def date2date():
    """
    日期格式统一
    2017年3月-2017年7月
    [0-9\-年\.月－～~\—―/]{4,}
    :return:
    """
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ok = 1"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    num = 0
    for teacher in teacher_list:
        exp_list = teacher["exp_clear"].split('\n')
        try:
            ne_list = eval(teacher["ne"])
        except:
            print(teacher["id"])
        if not ne_list:
            continue
        flag = 0
        for i in range(0, len(ne_list)):
            if not ne_list[i]:
                continue
            date = ne_list[i].get("date", "")
            if re.findall(r'－|～|~|——|至', date):
                date = re.sub(r'－|～|~|——|至', '-', date)

                flag = 1

            if re.findall(r'年', date):
                date = re.sub(r'年', '.', date)
                date = re.sub(r'月', '', date)
                date = re.sub(r'\.;', ';', date)
                date = date.strip('.')
                flag = 1

            if re.findall(r'\.-', date):
                date = re.sub(r'\.-', '-', date)
                flag = 1
            ne_list[i]["date"] = date

        if flag == 1:
            num += 1
            print(ne_list)
            update_list.append((str(ne_list), teacher["id"]))

    print("-" * 10)
    print(num)
    print(len(update_list))
    u_sql = "update teacher_eduexp set ne = %s where id = %s"
    print(dbs.exe_many(u_sql, update_list))
    pass


def kk():
    from algorithm.li.extract.templates.ne2sentence_template import sentence_template
    ne_name = ["org", "date", "degree", "country", "state_or_province", "major", "discipline_category", "graduate"]
    s_t = sentence_template
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ok = 1"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    num = 0
    d_list = []
    for teacher in teacher_list:
        try:
            ne_list = eval(teacher["ne"])
        except:
            print(teacher["id"])
            continue
        if not ne_list:
            continue
        exp_list = teacher["exp_clear"].split('\n')
        new_ne_list = []
        for i in range(0, len(ne_list)):

            new_ne = ne_list[i]

            t_l = []
            for nn in ne_name:
                t = ne_list[i].get(nn, "")
                if t != "":
                    t_l.append(nn)
            s = ",".join(t_l)
            if s != "" and s not in s_t:
                s_t.append(s)

            degree_list = ne_list[i].get("degree", "").split(';')
            # org_list = ne_list[i].get("org", "").split(';')
            # date_list = ne_list[i].get("date", "").split(';')
            d_list.extend(degree_list)


def nn(ne_str, ne_dict):
    from algorithm.li.extract.templates.ne2sentence_template import sentence_format
    try:
        if ne_str == "org,date,degree":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,date,degree,major":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'], ne_dict['degree'])
        elif ne_str == "org,degree":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,degree,state_or_province":
            r = sentence_format[ne_str].format(ne_dict['state_or_province'], ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,date,degree,country":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,date,degree,state_or_province":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,date,major":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'])
        elif ne_str == "org,date,degree,country,state_or_province":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,degree,country":
            r = sentence_format[ne_str].format(ne_dict['country'], ne_dict['org'], ne_dict['degree'])
        elif ne_str == "org,degree,major":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['major'], ne_dict['degree'])
        elif ne_str == "org,date,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'])
        elif ne_str == "org,date,state_or_province,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['state_or_province'], ne_dict['org'])
        elif ne_str == "org,date,degree,country,major":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['country'], ne_dict['org'], ne_dict['major'],
                                               ne_dict['degree'])
        elif ne_str == "org,date,major,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'])
        elif ne_str == "org,date,degree,state_or_province,major":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['state_or_province'], ne_dict['org'],
                                               ne_dict['major'], ne_dict['degree'])
        elif ne_str == "org,degree,country,state_or_province":
            r = sentence_format[ne_str].format(ne_dict['country'], ne_dict['state_or_province'], ne_dict['org'],
                                               ne_dict['degree'])
        elif ne_str == "date,degree,major":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['major'], ne_dict['degree'])
        elif ne_str == "org,degree,state_or_province,major":
            r = sentence_format[ne_str].format(ne_dict['state_or_province'], ne_dict['org'], ne_dict['major'],
                                               ne_dict['degree'])
        elif ne_str == "date,major,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['major'])
        elif ne_str == "org,degree,country,major":
            r = sentence_format[ne_str].format(ne_dict['country'], ne_dict['org'], ne_dict['major'], ne_dict['degree'])
        elif ne_str == "org,date,state_or_province":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'])
        elif ne_str == "org,date,degree,country,state_or_province,major":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'], ne_dict['degree'])
        elif ne_str == "date,state_or_province,major,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['state_or_province'], ne_dict['major'])
        elif ne_str == "org,date,country,state_or_province,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'])
        elif ne_str == "org,date,degree,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,degree,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,degree,state_or_province,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,date,degree,state_or_province,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,date,degree,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'],
                                               ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,date,degree,country,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,date,degree,country,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,date,degree,country,state_or_province,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,date,degree,state_or_province,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'],
                                               ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,degree,country,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,degree,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['major'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,degree,country,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['major'], ne_dict['discipline_category'],
                                               ne_dict['degree'])
        elif ne_str == "org,date,degree,country,state_or_province,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'], ne_dict['major'],
                                               ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,degree,state_or_province,major,discipline_category":
            r = sentence_format[ne_str].format(ne_dict['org'], ne_dict['major'],
                                               ne_dict['discipline_category'], ne_dict['degree'])
        elif ne_str == "org,date,country,graduate":
            r = sentence_format[ne_str].format(ne_dict['date'], ne_dict['org'])
        else:
            r = ""
    except:
        print("=====")
        r = ""
    return r


def ne2sentence():
    from algorithm.li.extract.templates.ne2sentence_template import sentence_template
    ne_name = ["org", "date", "degree", "country", "state_or_province", "major", "discipline_category", "graduate"]
    s_t = sentence_template
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ok = 1"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    num = 0
    for teacher in teacher_list:
        try:
            ne_list = eval(teacher["ne"])
        except:
            print(teacher["id"])
            continue
        if not ne_list:
            continue
        str_list = []
        for i in range(0, len(ne_list)):

            ne = ne_list[i]

            t_l = []
            for n in ne_name:
                t = ne_list[i].get(n, "")
                if t != "":
                    t_l.append(n)
            s = ",".join(t_l)
            if s != "" and s not in s_t:
                s_t.append(s)

            if ne.get("degree", "") == "" or ne.get("degree", "") in ["学士", "硕士", "博士"]:
                r = nn(s, ne)
                if r != "":
                    str_list.append(r)

        update_list.append(("\n".join(str_list), teacher["id"]))

    print(len(update_list))
    u_sql = "update teacher set eduexp = %s where id = %s"
    print(dbs.exe_many(u_sql, update_list))


def get_abroad():
    school_dict = eval(open(".\\dicts\\school2en_dict.txt", "r", encoding='utf8').read())

    abroad = {}.fromkeys(open(".\\dicts\\in.txt", "r", encoding='utf8').read().split('\n'))
    s_sql = "select id, ne, exp_clear from teacher_eduexp where ok = 1"
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    update_list = []
    num = 0
    o_list = []
    for teacher in teacher_list:
        try:
            ne_list = eval(teacher["ne"])
        except:
            print(teacher["id"])
            continue
        if not ne_list:
            continue
        flag = 0
        for i in range(0, len(ne_list)):

            ne = ne_list[i]

            org_list = ne.get("org", "").split(';')
            for o in org_list:
                o = re.sub('大学.+?系', '大学', o)
                o = re.sub('大学.+?学院', '大学', o)
                if school_dict.get(o, "") == "" and re.findall('国|日本|澳大利亚|州|芬兰|瑞典|挪威|冰岛|丹麦|爱沙尼亚'
                                                               '|拉脱维亚|立陶宛|白俄罗斯|俄罗斯|乌克兰|摩尔多瓦|波兰|捷克'
                                                               '|斯洛伐克|匈牙利|德国|奥地利|瑞士|列支敦士登|英国|爱尔兰|荷兰'
                                                               '|比利时|卢森堡|法国|摩纳哥|罗马尼亚|保加利亚|塞尔维亚|马其顿'
                                                               '|阿尔巴尼亚|希腊|斯洛文尼亚|克罗地亚|波斯尼亚和墨塞哥维那'
                                                               '|意大利|梵蒂冈|圣马力诺|马耳他|西班牙|葡萄牙|安道尔', o) \
                        and not re.findall('中国|首都|华东|华北|华南|华西|华中|西北|西南|东北|东南|北京|天津|上海|重庆|河北'
                                           '|山西|辽宁|吉林|黑龙江|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|海南|四川'
                                           '|贵州|云南|陕西|甘肃|青海|台湾|内蒙|广西|西藏|宁夏|新疆|香港|澳门|石家庄|沈阳'
                                           '|哈尔滨|杭州|福州|济南|广州|武汉|成都|昆明|兰州|台北|南宁|银川|太原|长春|南京|合肥'
                                           '|南昌|郑州|长沙|海口|贵阳|西安|西宁|呼和浩特|拉萨|乌鲁木齐', o)\
                        or abroad.get(o, "") != "":
                    flag = 1
                    break
            if flag == 1:
                break
        if flag == 1:
            num += 1
            update_list.append((str(flag), teacher["id"]))

    print(num)

    print(len(update_list))
    u_sql = "update teacher_edu_description set abroad = %s where id = %s"
    print(dbs.exe_many(u_sql, update_list))


if __name__ == "__main__":
    f()
    pass
