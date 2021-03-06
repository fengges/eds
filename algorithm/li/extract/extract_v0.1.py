import os
import sys
import re
from algorithm.li.extract.utils.dbutils import dbs
import jieba
import jieba.posseg as pseg


split_list = ["，", "。", ",", "."]
reSPLIT = r"[。|\n]"
reYEAR = r'[1-2][9,0][0-9]{2}'
reS = r'\n|\r|\0xa0|\a|\t|\\xa0|\u3000|\xa0|◆| '
reEmail = r'([A-Za-z0-9_]+([-+.][A-Za-z0-9_]+)*@[A-Za-z0-9_]+([-.][A-Za-z0-9_]+)*(\.[A-Za-z0-9_])*([-.][A-Za-z0-9_]+)*\.(cn|co m|net|CN|COM|NET|TW|HK|tw|hk))'
word_bag = ["留学", "毕业", "学位", "硕士", "博士", "学士", "研究生", "专业", "方向"]
school_dict = {}.fromkeys(open('\\dicts\\in.txt', 'r', encoding='utf-8').read().split('\n'))


class Extractor:
    def __init__(self, text=""):
        self.text = text
        self.lines = []
        self.gravities = []

    # 去除格式字符串
    def sub(self):
        self.text = re.sub(reS, "", self.text)

    # 计算句子权重
    def compute_gravity(self):
        self.seg_sentence()
        count = []
        for line in self.lines:
            s = 0
            for word in word_bag:
                if not line.find(word) == -1:
                    s += 1
            if re.search(reYEAR, line) is not None:
                s += 1
            count.append(s)
        self.gravities = count
        pass

    # 分句
    def seg_sentence(self):
        lines = re.split(reSPLIT, self.text)
        lines = [re.sub(reS, "", i) for i in lines if i]
        lines = [i for i in lines if len(i) >= 8]
        self.lines = lines

    # 得到准确的描述学历的句子
    def filter_sentence(self):
        if self.gravities is None or self.gravities == []:
            return

        result = [self.lines[i] for i in range(0, len(self.lines)) if self.gravities[i] > 1 or re.search("留学", self.lines[i]) is not None]

        if result:
            return result
        return

    def set_text(self, text=""):
        self.text = text
        self.lines = []
        self.gravities = []

    def cut_from_word(self, pattern, size=50):
        try:
            start = re.search(pattern, self.text).start()
            if start >= 0:
                length = len(self.text)
                return self.text[start:start + size if start + size < length else length]
        except:
            return

    # 取出主体描述
    def cut_blocks(self, re_list=[], size=[]):

        for i in range(len(re_list)):
            text = self.cut_from_word(re_list[i], size[i])
            if text is not None:
                self.text = text
                break

    def get_birthday(self):
        output = {'学士': 2100, '硕士': 2100, '博士': 2100}
        # ---按照年份切割info
        result = re.split('([1-2][9,0][0-9]{2})', self.text)

        # ---优先抽取出生信息，抽取到则return
        for i in range(len(result) - 1):
            if len(result[i]) == 4 and result[i].isdigit():
                checkstr = result[i+1]
                if len(checkstr) > 15:
                    checkstr = checkstr[:15]
                if not checkstr.find('生') == -1:
                    sindex = checkstr.find('生')
                    if sindex > 0 and checkstr[sindex-1] == '士' or checkstr[sindex-1] == '究':
                        break
                    elif int(result[i]) < 1994:
                        return result[i] + '-出生'

        # ---抽取教育经历信息
        for i in range(len(result)-1):
            if len(result[i]) == 4 and result[i].isdigit():
                checkstr = result[i+1]
                if len(checkstr) > 40:
                    checkstr = checkstr[:40]
                if not checkstr.find('毕业') == -1 and checkstr.find('硕士') == -1 and checkstr.find('博士') == -1 and output['学士'] > int(result[i]):
                    output['学士'] = int(result[i])

                if not checkstr.find('硕士') == -1 and output['硕士'] > int(result[i]):
                    output['硕士'] = int(result[i])
                elif not checkstr.find('博士') == -1 and output['博士'] > int(result[i]):
                    output['博士'] = int(result[i])
                elif not checkstr.find('学士') == -1 and output['学士'] > int(result[i]):
                    output['学士'] = int(result[i])
        if output['学士'] < 2100:
            return str(output['学士'])+'-学士'
        elif output['硕士'] < 2100:
            return str(output['硕士'])+'-硕士'
        elif output['博士'] < 2100:
            return str(output['博士'])+'-博士'
        else:
            return ''


def get_age():
    select_sql = "SELECT * from teacherdata_info"
    teacherdata = dbs.getDics(select_sql)
    print(len(teacherdata))

    uplist = []
    extractor = Extractor()
    for teacher in teacherdata:
        if not teacher['homepage'].find('http://ckspkk.eol.cn') == -1:
            info = eval(teacher['info'])
            # print(info)
            birthday = info.get('出生年月', '')
            person_info = info.get('个人简介', None)
            # ---有出生日期
            if len(birthday) > 3 and birthday != "":
                updata = (birthday[:4] + '-出生', teacher['id'])
                uplist.append(updata)
            # ---没有出生日期
            else:
                if person_info is None:
                    continue
                extractor.set_text(person_info)
                birthyear = extractor.get_birthday()
                updata = (birthyear, teacher['id'])
                uplist.append(updata)
        else:
            try:
                info = eval(teacher['info'])
                person_info = "".join(list(info.values()))
            except Exception as e:
                person_info = teacher['info']

            if person_info is None:
                continue
            extractor.set_text(person_info)
            birthyear = extractor.get_birthday()
            updata = (birthyear, teacher['id'])
            uplist.append(updata)

    uplistNew = []
    for node in uplist:
        age_description = node[0]
        age = 0
        if age_description == '':
            age = 0
        else:
            year = int(age_description.split('-')[0])
            year_type = age_description.split('-')[1]
            if year_type == '出生':
                age = 2018 - year
            elif year_type == '学士':
                age = 2018 - year + 22
            elif year_type == '硕士':
                age = 2018 - year + 25
            elif year_type == '博士':
                age = 2018 - year + 30

        if age > 100 or age < 20:
            age = 0
            age_description = ''
        data = (age_description, age, node[1])
        uplistNew.append(data)

    print(len(uplistNew))
    update_sql = "update teacher_age set age_description=%s,age=%s where id=%s"
    print(dbs.exe_many(update_sql, li=uplistNew))


def get_overseas_exp():
    select_sql = "select * from teacherdata_info"

    teacher_list = dbs.getDics(select_sql)
    print(len(teacher_list))
    extractor = Extractor()

    jieba.load_userdict("E:\\shixi\\justcoding\\extract_v1.0\\user_dict.txt")

    result_list = []
    w_list = []
    for teacher in teacher_list:
        if re.search(r'cksp\.eol\.cn', teacher["homepage"]) is not None:
            info_dict = eval(teacher["info"])
            extractor.set_text(info_dict["个人简介"])
        else:
            try:
                info = eval(teacher['info'])
                person_info = "".join(list(info.values()))
            except Exception as e:
                person_info = teacher['info']
            if person_info is None:
                continue
            extractor.set_text(person_info)
            reList = [r'教育经历|学习经历|教育背景', r'个人简介|个人简历', teacher["name"]]
            extractor.cut_blocks(reList)

        extractor.compute_gravity()
        sentences = extractor.filter_sentence()
        if sentences is None:
            continue
        label = ["ns", "nt"]
        description = ""
        wo_list = []
        for sentence in sentences:
            if re.search(r'留学', sentence):
                description = description + ";" + sentence
                continue
            words = pseg.cut(sentence)

            # for w in words:
            #     if w.flag in label and re.search(r'大学|学院|院', w.word) and school_dict.get(w.word):
            #         description = description + ";" + sentence
            #         break
            words = [w for w in words if w.flag in label]
            if len(words) > 0:
                description = description + ";" + sentence
                wo_list = [w.word for w in words]

        if not description == "":
            w_list.extend(wo_list)
            result_list.append(("-".join(wo_list), teacher['id'], description.lstrip(";")))

    print(len(result_list))
    fw = open("5.csv", "a+", encoding="utf-8")
    for i in result_list:
        fw.write("%s,%s,%s\n" % i)
    fw.close()

    print(len(w_list))
    fw1 = open("6.csv", "a+", encoding="utf-8")
    for i in w_list:
        fw1.write("%s\n" % i)
    fw1.close()


def get_email():
    info_sql = "select id, info, homepage from teacherdata_info where id >= 40146 and email=''"
    info = dbs.getDics(info_sql)

    ins_dict = open(DIR + "\\dicts\\institution_email.txt", "r", encoding="utf-8").readlines()
    ins_dict = [ins.strip('\n') for ins in ins_dict]

    update_list = []
    for item in info:
        if not item["info"]:
            continue
        if re.search(r'cksp\.eol\.cn', item["homepage"]) is not None:
            info_dict = eval(item["info"])
            try:
                email_text = [i[0] for i in re.findall(reEmail, info_dict["E-mail"])]
            except:
                continue
            pass
        else:
            info_text = item["info"]
            info_text = info_text.replace("[at]", "@")
            info_text = info_text.replace(" ", "")
            info_text = info_text.replace("\n", "")
            email_text = [i[0] for i in re.findall(reEmail, info_text)]

        if email_text:
            list_email = sorted(set(email_text), key=email_text.index)  # 去除相同邮箱地址
            list_email = [item for item in list_email if item not in ins_dict]  # 去除机构邮箱地址
            if len(list_email) > 0:
                print(";".join(list_email))
                update_list.append((";".join(list_email), item["id"]))
    print(len(update_list))
    update_sql = "update teacherdata_info set email=%s where id = %s"
    print(dbs.exe_many(update_sql, update_list))
    pass


def institution_email():

    file = open(DIR + "\\dicts\\institution_email.txt", "a+", encoding="utf-8")
    email_lines = file.read().split('\n')
    info_sql = "select id, info from teacherdata_info where id >= 40146"
    info = dbs.getDics(info_sql)
    list_ = []
    # 生成机构邮箱词典 判定方法为：重复出现的邮箱暂定为机构邮箱
    for item in info:
        if not item["info"]:
            continue
        info_text = item["info"]
        info_text = info_text.replace("[at]", "@")
        info_text = info_text.replace(" ", "")
        info_text = info_text.replace("\n", "")
        email_text = [i[0] for i in re.findall(reEmail, info_text)]

        if email_text:
            l2 = sorted(set(email_text), key=email_text.index)  # 处理同一个页面重复出现的邮箱地址
            list_.extend(l2)
            print('#'*20)
        else:
            print('*'*20)

    list_1 = []
    l3 = sorted(set(list_))
    for item in l3:
        n = list_.count(item)
        if n > 2 and item not in email_lines:
            list_1.append(item)
    print(list_1)
    print(len(list_1))
    file.write("\n".join(list_1))
    file.close()
    pass


def test():

    info_sql = "select id, info from teacherdata_info where id >= 40146"
    info = dbs.getDics(info_sql)
    list_ = []
    # 生成机构邮箱词典 判定方法为：重复出现的邮箱暂定为机构邮箱
    for item in info:
        if not item["info"]:
            continue
        info_text = item["info"]
        info_text = info_text.replace("[at]", "@")
        info_text = info_text.replace(" ", "")
        info_text = info_text.replace("\n", "")
        email_text = [i[0] for i in re.findall(reEmail, info_text)]

        if email_text:
            l2 = sorted(set(email_text), key=email_text.index)  # 处理同一个页面重复出现的邮箱地址
            list_.extend(l2)
            print('#' * 20)
        else:
            print('*' * 20)

    list_1 = []
    l3 = sorted(set(list_))
    for item in l3:
        n = list_.count(item)
        if n > 3:
            list_1.append(item + "," + str(n))
    print(list_1)
    print(len(list_1))
    file = open("1.csv", "w", encoding="utf8")
    file.write("\n".join(list_1))
    file.close()
    pass
    pass


def get_title():
    title_dict = ["副教授", "助理教授", "教授", "讲师", "助教", "副研究员", "助理研究员", "研究员", "高级工程师", "高级实验师", "高工", "工程师", "实验师"]

    extractor = Extractor()
    result_list = []

    select_sql = "SELECT id, name, info, all_link FROM `eds_985teacher` WHERE school = '清华大学';"
    teacher_list = dbs.getDics(select_sql)
    print(len(teacher_list))

    for teacher in teacher_list:
        if re.search(r'cksp\.eol\.cn', teacher["all_link"]) is not None:
            info_dict = eval(teacher["info"])
            try:
                extractor.set_text(info_dict["个人简介"])
            except:
                person_info = teacher['info']
        else:
            try:
                info = eval(teacher['info'])
                person_info = "".join(list(info.values()))
            except:
                person_info = teacher['info']
            if person_info is None:
                continue
            extractor.set_text(person_info)
        re_list = [r'职称|职务', r'个人简介|个人简历', teacher["name"]]
        # 匹配模式
        size = [50, 200, 200]
        extractor.sub()
        extractor.cut_blocks(re_list, size)
        index = 0
        title = ""
        while index < len(title_dict):
            if title_dict[index] in extractor.text:
                if title_dict[index] == "副教授" and len(re.findall(r'教授', extractor.text)) > 1:
                    title = "教授"
                    break
                title = title_dict[index]
                break
            index += 1

        if title != "":
            # result_list.append((title, teacher["id"]))

            print((teacher["id"], title))
    # print(len(result_list))
    # update_sql = "update teacherdata_info set title=%s where id=%s"
    # dbs.exe_many(update_sql, result_list)


if __name__ == "__main__":

    # get_age()
    # get_overseas_exp()
    # institution_email()
    # get_email()
    # test()
    get_title()
    pass
