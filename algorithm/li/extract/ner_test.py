from algorithm.li.extract.utils.dbutils import dbs
from stanfordcorenlp.corenlp import nlp_zh
import re
import json


def get_data():
    """
    从数据库中取出数据
    :return:
    """
    s_sql = "select id, exp_clear from teacher_eduexp where clear=2 and exp_clear != ''"
    data = dbs.getDics(s_sql)
    return data


def ner(data=None):
    """
    实体识别,非实体用词性填充
    :param data:
    :return:
    """
    if not type(data) == list:
        data = [].append(data)
    result = []
    for d in data:
        try:
            ner_text = nlp_zh.ner(d)
            pos_tag_text = nlp_zh.pos_tag(d)
        except:
            ner_text = []
            pos_tag_text = []

        d_list = []
        for i in range(0, len(ner_text)):
            if ner_text[i][1] == 'O':
                d_list.append((ner_text[i][0], pos_tag_text[i][1]))
            else:
                d_list.append(ner_text[i])
        result.append(d_list)
    return result


def parse(data):
    """
    nlp.parse(sentence)
    :return:
    """
    if type(data) == list:
        result = []
        for d in data:
            try:
                text = nlp_zh.parse(d)
            except:
                text = ""
            result.append(text)
        return result
    try:
        result = nlp_zh.parse(data)
    except:
        result = ""

    return result
    pass


def pos_tag(data=None):
    """
        nlp.pos_tag(sentence)
        :return:
        """
    if type(data) == list:
        result = []
        for d in data:
            try:
                text = nlp_zh.pos_tag(d)
            except:
                text = ""
            result.append(text)
        return result
    try:
        result = nlp_zh.pos_tag(data)
    except:
        result = ""

    return result
    pass


def ner_test(data=None):
    """
    实体识别,非实体用词性填充
    :param data:
    :return:
    """
    if not type(data) == list:
        data = [].append(data)
    result = []
    ne_list = []
    for d in data:
        if d == "":
            continue
        try:
            ner_text = nlp_zh.ner(d)
        except:
            ner_text = []
        result.append(ner_text)
        ne = get_ne(ner_text)
        if ne.get("org", "") == "":
            country = ne.get("country", "")
            state_or_province = ne.get("state_or_province", "")
            o_l = []
            try:
                if country != "":
                    o_l = re.findall(r'{0}[\u4E00-\u9FA5]*?大学|{0}[\u4E00-\u9FA5]*?学院'.format(country), d)
                if state_or_province != "" and not o_l:
                    o_l = re.findall(r'{0}[\u4E00-\u9FA5]*?大学|{0}[\u4E00-\u9FA5]*?学院'.format(state_or_province), d)
                if len(o_l) > 0:
                    ne["org"] = o_l[0]
                o_t = []
                if not o_l:
                    o_t = re.findall(r'[,，获 在:：][\u4E00-\u9FA5]*?大学|[,获 在:：][\u4E00-\u9FA5]*?学院', d)
                if not o_t:
                    org = re.sub(r'[,，获 在:：]', '', o_t[0])
                    org = re.sub(r'[,，获 在:：]', '', org)
                    ne["org"] = org
            except:
                print()

        # 学科门类discipline_category：获(.*?)学士/硕士/博士
        # 专业major：学院/系(.*?)专业
        try:
            m_l = re.findall(r'学院[\u4E00-\u9FA5]+?专业|系[\u4E00-\u9FA5]+?专业|（[\u4E00-\u9FA5]+?专业', d)
            if m_l:
                ne["major"] = re.sub(r'学院|专业|系|,|，|:|：|（', '', m_l[0])

            dc_l = re.findall(r'[系院获，, :：]([\u4E00-\u9FA5（）]+?){0}'.format(ne.get("degree")), d)
            discipline_category = ""
            if dc_l:
                discipline_category = re.sub(ne.get("org"), "", dc_l[0])
                discipline_category = re.sub(r'系|院|获|，|,| |：|:|的|得|学院', "", discipline_category)
            if discipline_category != "" and not re.findall(r'访问', discipline_category) and re.findall(r'学', discipline_category):
                ne["discipline_category"] = discipline_category
        except:
            print()
        ne_list.append(ne)
    return result, ne_list


def get_ne(line=None):
    if not line:
        return None
    degree_words = ["本科", "硕士", "博士", "学士", "研究生", "博士后", "学者", "研修生", "MSW", "进修"]
    date_words = ["TIME", "DATE"]
    re_dict = dict()
    re_dict["date"] = ""
    re_dict["org"] = ""
    re_dict["state_or_province"] = ""
    re_dict["country"] = ""
    re_dict["degree"] = ""

    l = len(line)
    for i in range(0, l):
        # 处理date
        if line[i][1] in date_words or (line[i][1] == "NUMBER" and (
                len(re.findall(r'[1-2][9,0][0-9]{2}', line[i][0])) > 0 or (len(
                re.findall(r';$', re_dict.get("date", ""))) == 0 and re_dict["date"] != ""))):
            re_dict["date"] += line[i][0]

        elif re_dict["date"] != "" and \
                len(re.findall(r';$', re_dict.get("date", ""))) == 0 and \
                i + 1 < l and (line[i + 1][1] == "NUMBER" or line[i + 1][1] in date_words):
            re_dict["date"] += line[i][0]

        elif re_dict["date"] != "" and len(re.findall(r';$', re_dict.get("date", ""))) == 0:
            re_dict["date"] += ";"

        # 处理org
        if line[i][1] == "ORGANIZATION":
            re_dict["org"] += line[i][0]

        elif re_dict["org"] != "" and len(re.findall(r';$', re_dict.get("org", ""))) == 0:
            re_dict["org"] += ";"

        # 处理state_or_province
        if line[i][1] == "STATE_OR_PROVINCE":
            re_dict["state_or_province"] += line[i][0]

        elif re_dict["state_or_province"] != "" and len(re.findall(r';$', re_dict.get("state_or_province", ""))) == 0:
            re_dict["state_or_province"] += ";"

        # 处理country
        if line[i][1] == "COUNTRY":
            re_dict["country"] += line[i][0]

        elif re_dict["country"] != "" and len(re.findall(r';$', re_dict.get("country", ""))) == 0:
            re_dict["country"] += ";"

        # 处理degree
        if line[i][0] in degree_words:
            re_dict["degree"] += line[i][0]

        elif re_dict["degree"] != "" and len(re.findall(r';$', re_dict.get("degree", ""))) == 0:
            re_dict["degree"] += ";"

    r_d = dict()
    for key, item in re_dict.items():
        item = item.strip(';')
        if item != "":
            r_d[key] = item

    return r_d


def get_ner():
    teacher_list = get_data()
    print(len(teacher_list))
    update_list = []
    for teacher in teacher_list:
        if teacher["exp_clear"] is not None or teacher["edu_exp"] != "":
            print(teacher["id"])
            print(teacher["exp_clear"])
            data, ne = ner_test(teacher["exp_clear"].split('\n'))
            print(ne)
            print("-" * 10)
            print("\n")
            if ne:
                ne_str = json.dumps(ne)
                update_list.append((ne_str, teacher["id"]))
    nlp_zh.close()
    print(len(update_list))
    update_sql = "update teacher_eduexp set ne = %s where id = %s"
    print(dbs.exe_many(update_sql, update_list))
    pass


if __name__ == "__main__":
    get_ner()
    pass
