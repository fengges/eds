from algorithm.li.extract.utils.dbutils import dbs
import re
from urllib import parse as pa


def counter(name_list=[]):
    from collections import Counter

    count_list = Counter(name_list).most_common()

    s = []
    for c in count_list:
        s.append(c[0] + "(" + str(c[1]) + ")")
    return "，".join(s)


def data_clean():
    """
    将javascript的链接转换为正常
    :return:
    """
    data_list = dbs.getDics("SELECT * FROM `eds_985teacher` WHERE link like '%javascript%' AND school = '中南大学';")
    print(len(data_list))
    u_list = []
    for data in data_list:
        id = data['id']
        '''javascript:window.open('/blog/content2?name='+encodeURI('周雄伟'))'''
        link = data['link']
        if link != "":
            p_tuple = re.findall(r"open\('(.+?)'\+encodeURI\('(.+?)'\)\)", link)[0]

            link = p_tuple[0] + pa.quote(p_tuple[1])
            # print(pa.urljoin(data['institution_url'], link))
            link = pa.urljoin(data['institution_url'], link)
            print(link)
            u_list.append((link, id))

    print(len(u_list))
    u_sql = "UPDATE eds_985teacher SET all_link=%s WHERE id = %s"
    print(dbs.exe_many(u_sql, u_list))


def honor_clean():
    """
    清华国家科技奖励 清洗
    :return:
    """
    in_lines = open('.\\qinghua\\清华_国家科学技术进步奖.csv', 'r', encoding='utf-8').read().split('\n')
    teacher_lines = open('.\\qinghua\\清华教师名单.csv', 'r', encoding='utf-8').read().split('\n')
    teacher_dict = dict()
    for i in range(0, len(teacher_lines)):
        info = teacher_lines[i].split(',')
        if teacher_dict.get(info[1]):
            teacher_dict[info[1]].append(i)
        else:
            teacher_dict[info[1]] = [i]

    out_lines = open('.\\qinghua\\清华_国家科学技术进步奖_clean.csv', 'a', encoding='utf8')
    for line in in_lines:
        info = line.split(',')
        name = info[2]
        index_list = teacher_dict.get(name)

        if index_list:
            for index in index_list:
                print(line + ',' + teacher_lines[index])
                out_lines.write(line + ',' + teacher_lines[index]+'\n')
        else:
            print(line)
            out_lines.write(line + '\n')
    out_lines.close()


def match_title():
    title_dict = eval(open('.\\qinghua\\title.txt', 'r', encoding='utf-8').read())
    id_list = open('.\\qinghua\\id.txt', 'r', encoding='utf-8').read().split('\n')
    out_lines = open('.\\qinghua\\id_title.csv', 'a', encoding='utf8')
    result_list = []
    for id in id_list:
        if id == "":
            print(",")
            result_list.append(",")
        else:
            title = title_dict.get(id, "")
            print(id+","+title)
            result_list.append(id+","+title)

    out_lines.write('\n'.join(result_list))
    out_lines.close()


def match_level():
    level = {}

    level_list = open('.\\qinghua\\02.csv', 'r', encoding='utf-8').read().split('\n')
    for line in level_list:
        info = line.split(',')
        level[info[1]+info[2]] = info[0]
    print(len(level))
    teacher_list = open('.\\qinghua\\01.csv', 'r', encoding='utf-8').read().split('\n')
    for line in teacher_list:
        teacher = line.split(',')
        key = teacher[1] + teacher[0]
        value = level.get(key, "")
        print(teacher[1], teacher[0], value)


def match_teacher():
    import pandas as pd
    import numpy as np

    honor_df = pd.read_csv('.\\qinghua\\qinghua_jianglihuizong.csv')
    """
    honor     189 non-null object
    level     189 non-null object
    code      189 non-null object
    p_name    176 non-null object
    name      189 non-null object
    school    117 non-null object
    year      189 non-null int64
    """
    honor_dict = dict()
    for index in honor_df.index:
        honor = str(honor_df.loc[index].honor)
        level = str(honor_df.loc[index].level)
        code = str(honor_df.loc[index].code)
        p_name = str(honor_df.loc[index].p_name)
        t_name = str(honor_df.loc[index].t_name)
        school = str(honor_df.loc[index].school)
        year = str(honor_df.loc[index].year)

        the_honor = honor + "," + level + "," + code + "," + p_name + "," + school + "," + year

        the_list = honor_dict.get(t_name, [])
        if the_list:
            the_list.append(the_honor)
            honor_dict[t_name] = the_list
        else:
            the_list = [the_honor]
            honor_dict[t_name] = the_list

    mentor_df = pd.read_csv('.\\qinghua\\yuanshihezuoxuezhe.csv')
    """
    mentor        86 non-null object
    co_author     82 non-null object
    num1          86 non-null int64
    db_teahcer    82 non-null object
    num2          86 non-null int64
    """

    # for index in mentor_df.index:
    #     mentor = str(mentor_df.loc[index].mentor)
    #
    #     the_honor = honor_dict.get(mentor, "")
    #     for h in the_honor:
    #         print(mentor+","+h)

    # for index in mentor_df.index:
    #     db_teahcer = str(mentor_df.loc[index].db_teahcer)
    #     if db_teahcer == "nan":
    #         continue
    #     teacher_list = db_teahcer.split(',')
    #     for teacher in teacher_list:
    #
    #         the_honor = honor_dict.get(teacher, "")
    #         for h in the_honor:
    #             print(teacher+","+h)

    for index in mentor_df.index:
        co_author = str(mentor_df.loc[index].co_author)
        if co_author == "nan":
            continue
        teacher_list = co_author.split(',')
        for teacher in teacher_list:

            the_honor = honor_dict.get(teacher, "")
            for h in the_honor:
                print(teacher+","+h)


def zhuanli_duplicate():
    s_sql = "SELECT * FROM `pss_zhuanli` GROUP BY TIVIEW, INVIEW, APD"
    info_list = dbs.getDics(s_sql)

    update_list = []
    for info in info_list:
        update_list.append((info['TIVIEW'], info['INVIEW'], info['APD'], info['id']))

    for i in update_list:
        print(i)
    print(len(update_list))
    d_sql = '''
            DELETE FROM `pss_zhuanli_copy`
            WHERE TIVIEW=%s
            AND INVIEW=%s
            AND APD=%s
            AND id !=%s
    '''
    print(dbs.exe_many(d_sql, update_list))


def mentor_extract():
    s_sql = "SELECT * FROM `pss_zhuanli_clean`;"
    info_list = dbs.getDics(s_sql)
    mentor_dict = {}.fromkeys(open('.\\qinghua\\mentor_list.txt', 'r', encoding='utf-8').read().split('\n'))
    print(mentor_dict)
    print("*" * 10)
    update_list = []
    for item in info_list:
        author_list = item['INVIEW'].split(';')
        mentor_list = []
        for author in author_list:
            if mentor_dict.get(author, "") != "":
                mentor_list.append(author)
        print(author_list, mentor_list)
        update_list.append((";".join(mentor_list), item['id']))

    u_sql = "UPDATE `pss_zhuanli_clean` SET MENTOR = %s WHERE id=%s"
    print(len(update_list))
    print(dbs.exe_many(u_sql, update_list))


def create_sheet():

    import xlwt

    s_sql = "SELECT * FROM `pss_zhuanli_clean`;"
    info_list = dbs.getDics(s_sql)
    teacher_dict = {}.fromkeys(open('.\\qinghua\\teacher_list.txt', 'r', encoding='utf-8').read().split('\n'))
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('sheet1')
    row = 0
    sum = 0
    for info in info_list:

        author_list = info['INVIEW'].split(';')
        teacher_list = []
        for author in author_list:
            if teacher_dict.get(author, "") != "":
                teacher_list.append(author)

        mentor_list = info['MENTOR'].split(';')
        sum += len(mentor_list)
        for mentor in mentor_list:
            if len(mentor_list) > 1:
                print("======")
            print(mentor, ";".join(teacher_list), info['TIVIEW'], info['PAVIEW'], info['APD'], info['PD'])

            sheet.write(row, 0, mentor)
            sheet.write(row, 1, ";".join(teacher_list))
            sheet.write(row, 2, info['TIVIEW'])
            sheet.write(row, 3, info['PAVIEW'])
            sheet.write(row, 4, info['APD'])
            sheet.write(row, 5, info['PD'])
            row += 1

    wbk.save('.\\qinghua\\清华院士_专利信息_2018.9.30.xls')
    print(sum)


def mentor_team_year_honor():
    import pandas as pd
    import xlrd
    import xlwt

    teacher_dict = {}.fromkeys(open('.\\qinghua\\teacher_list.txt', 'r', encoding='utf8').read().split('\n'))
    mentor_dict = {}.fromkeys(open('.\\qinghua\\mentor_list.txt', 'r', encoding='utf8').read().split('\n'))
    mentor_dict_clean = {}.fromkeys(open('.\\qinghua\\mentor_list_clean.txt', 'r', encoding='utf8').read().split('\n'))

    honor_dict = dict()
    yuanshi_list = []

    wb_rd_1 = xlrd.open_workbook('.\\qinghua\\processed\\清华大学_奖励汇总.xls')
    wb_rd_1_sheet1 = wb_rd_1.sheet_by_index(0)

    for row in range(1, wb_rd_1_sheet1.nrows):
        line = wb_rd_1_sheet1.row_values(row)
        honor = line[0]
        level = line[1]
        code = line[2]
        p_name = line[3]
        name = line[4]
        year = str(int(line[6]))

        # honor_dict
        if teacher_dict.get(name, "") == "":
            continue
        the_list = honor_dict.get(str(code) + str(p_name), [])
        the_list.append(name)
        honor_dict[str(code) + str(p_name)] = the_list

        # yuanshi_list
        if mentor_dict.get(name, "") != "":
            yuanshi_list.append((honor, level, code, p_name, name, year))

    print(honor_dict)
    print("=" * 10)
    print(yuanshi_list)

    yuanshi_dict = dict()
    for the in yuanshi_list:
        honor = the[0]
        level = the[1]
        code = the[2]
        p_name = the[3]
        name = the[4]
        year = the[5]

        team_list = honor_dict.get(code + p_name, [])
        team_list = [i for i in team_list if i != name]
        team_str = counter(team_list)
        p_list = yuanshi_dict.get(name, [])
        if p_list:
            p_list.append((year, team_str, honor, level, p_name))
        else:
            p_list = [(year, team_str, honor, level, p_name)]
        yuanshi_dict[name] = p_list

    wb_rd_2 = xlrd.open_workbook('.\\qinghua\\tuandui\\清华院士团队及其成果.xls')
    wb_rd_2_sheet1 = wb_rd_2.sheet_by_index(0)

    wb_wt = xlwt.Workbook(encoding='utf-8')
    sheet = wb_wt.add_sheet('sheet1')
    sum = 1
    for row in range(1, wb_rd_2_sheet1.nrows):
        line = wb_rd_2_sheet1.row_values(row)
        ins = line[0]
        name = line[1]

        if mentor_dict_clean.get(name, "") == "":
            continue

        the_yuanshi = yuanshi_dict.get(name, [])

        if the_yuanshi:
            for i in the_yuanshi:
                year = i[0]
                team = i[1]
                achi = i[2] + i[3]
                p_name = i[4]
                # (year, team_str, honor, level, p_name)

                sheet.write(sum, 0, ins)
                sheet.write(sum, 1, name)
                sheet.write(sum, 2, year)
                sheet.write(sum, 3, team)
                sheet.write(sum, 4, achi)
                sheet.write(sum, 5, p_name)

                sum += 1
        else:
            year = ""
            team = ""
            achi = ""
            p_name = ""

            sheet.write(sum, 0, ins)
            sheet.write(sum, 1, name)
            sheet.write(sum, 2, year)
            sheet.write(sum, 3, team)
            sheet.write(sum, 4, achi)
            sheet.write(sum, 5, p_name)

            sum += 1

        wb_wt.save('.\\qinghua\\tuandui\\清华院士团队及其成果_国家科技奖_2018.9.30.xls')


def mentor_team_year_zhuanli():
    import xlwt
    import xlrd
    import re

    mentor_dict = {}.fromkeys(open('.\\qinghua\\mentor_list_clean.txt', 'r', encoding='utf-8').read().split('\n'))

    zhuanli_dict = dict()

    wb_rd_zhuanli = xlrd.open_workbook('.\\qinghua\\清华院士_专利信息_2018.9.30.xls')
    sheet_zhuanli = wb_rd_zhuanli.sheet_by_index(0)
    for row in range(1, sheet_zhuanli.nrows):
        line = sheet_zhuanli.row_values(row)
        mentor = line[0]

        team_list = [i for i in line[1].split(';') if i != mentor]
        p_name = line[2]
        year = int(re.findall(r'[0-9]{4}', line[5])[0])

        m_dict = zhuanli_dict.get(mentor, {})
        if m_dict:
            y_dict = m_dict.get(year, {})
            if y_dict:
                y_dict["team"].extend(team_list)
                y_dict["p_list"].append(p_name)
            else:
                y_dict["team"] = team_list
                y_dict["p_list"] = [p_name]
            m_dict[year] = y_dict
        else:
            y_dict = dict()
            y_dict["team"] = team_list
            y_dict["p_list"] = [p_name]
            m_dict[year] = y_dict

        zhuanli_dict[mentor] = m_dict

    workbook = xlrd.open_workbook('.\\qinghua\\tuandui\\清华院士团队及其成果.xls')
    sheet1 = workbook.sheet_by_index(0)

    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('sheet1')

    sum = 0
    for row in range(1, sheet1.nrows):
        line = sheet1.row_values(row)
        ins = line[0]
        name = line[1]

        if mentor_dict.get(name, "") == "":
            continue

        the_dict = zhuanli_dict.get(name, {})

        if the_dict:
            for k, value in the_dict.items():
                year = k
                team = counter(value.get('team', []))
                achi = ';'.join(value.get('p_list', []))
                print(sum, year, team, achi)
                sheet.write(sum, 0, ins)
                sheet.write(sum, 1, name)
                sheet.write(sum, 2, year)
                sheet.write(sum, 3, team)
                sheet.write(sum, 4, achi)
                sum += 1
            pass
        else:
            year = ""
            team = ""
            achi = ""
            print(sum, year, team, achi)
            sheet.write(sum, 0, ins)
            sheet.write(sum, 1, name)
            sheet.write(sum, 2, year)
            sheet.write(sum, 3, team)
            sheet.write(sum, 4, achi)
            sum += 1

    wbk.save('.\\qinghua\\tuandui\\清华院士团队及其成果_专利_2018.9.30.xls')


def t():
    import os
    import xlwt
    import xlrd
    dir_list = os.listdir('.\\qinghua\\process\\')
    print(dir_list)

    for file in dir_list:
        print(file)
        wb_rd = xlrd.open_workbook('.\\qinghua\\process\\' + file)
        sheet1_rd = wb_rd.sheet_by_index(0)

        wbk = xlwt.Workbook(encoding='utf-8')
        sheet = wbk.add_sheet('sheet1')

        sum = 0
        for row in range(1, sheet1_rd.nrows):
            line = sheet1_rd.row_values(row)
            level = line[0]
            code = line[1]
            p_name = line[2]
            name_list = line[3].split('、')
            for name in name_list:
                print(level, code, p_name, name)
                sheet.write(sum, 0, level)
                sheet.write(sum, 1, code)
                sheet.write(sum, 2, p_name)
                sheet.write(sum, 3, name)
                sheet.write(sum, 4, "")
                sum += 1

        wbk.save('.\\qinghua\\processed\\' + file)


def merge_table():
    import os
    import xlwt
    import xlrd
    dir_list = os.listdir('.\\qinghua\\技术发明\\')
    print(dir_list)

    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('sheet1')

    sum = 0
    for file in dir_list:
        print(file)
        wb_rd = xlrd.open_workbook('.\\qinghua\\技术发明\\' + file)
        sheet1_rd = wb_rd.sheet_by_index(0)
        year = re.findall(r'[0-9]{4}', file)[0]

        for row in range(1, sheet1_rd.nrows):
            line = sheet1_rd.row_values(row)
            level = line[0]
            code = line[1]
            p_name = line[2]
            name_list = line[3].split('、')
            if len(line) <= 4:
                school = ""
            else:
                school = line[4]
            for name in name_list:
                print(level, code, p_name, name)
                sheet.write(sum, 0, "技术发明奖")
                sheet.write(sum, 1, level)
                sheet.write(sum, 2, code)
                sheet.write(sum, 3, p_name)
                sheet.write(sum, 4, name)
                sheet.write(sum, 5, school)
                sheet.write(sum, 6, year)
                sum += 1

    wbk.save('.\\qinghua\\processed\\' + "技术发明奖.xls")


def honor_huizong():
    import os
    import xlwt
    import xlrd
    dir_list = os.listdir('.\\qinghua\\processed\\')
    print(dir_list)

    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('sheet1')

    sum = 0
    for file in dir_list:
        print(file)
        wb_rd = xlrd.open_workbook('.\\qinghua\\processed\\' + file)
        sheet1_rd = wb_rd.sheet_by_index(0)

        for row in range(1, sheet1_rd.nrows):
            # honor	level   code    p_name	name	school	year
            line = sheet1_rd.row_values(row)
            honor = line[0]
            level = line[1]
            code = line[2]
            p_name = line[3]
            name = line[4]
            school = line[5]
            year = line[6]

            if school == "" and not re.findall('清华大学', school):
                continue
            print(honor,level,code,p_name,name,school,year)
            sheet.write(sum, 0, honor)
            sheet.write(sum, 1, level)
            sheet.write(sum, 2, code)
            sheet.write(sum, 3, p_name)
            sheet.write(sum, 4, name)
            sheet.write(sum, 5, school)
            sheet.write(sum, 6, year)
            sum += 1

    wbk.save('.\\qinghua\\processed\\' + "清华大学_奖励汇总.xls")


def t_():
    id_list = open('.\\qinghua\\id_list.txt', 'r', encoding='utf-8').read().split('\n')
    print(len(id_list))
    u_sql = "UPDATE zhuanli_search SET status=0 where id = %s"
    print(dbs.exe_many(u_sql, id_list))
    pass


if __name__ == "__main__":
    # zhuanli_duplicate()
    # mentor_extract()
    # create_sheet()
    # mentor_team_year_zhuanli()
    # merge_table()
    # honor_huizong()
    # mentor_team_year_honor()
    t_()
    pass
