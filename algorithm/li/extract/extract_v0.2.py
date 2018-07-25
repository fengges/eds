import os
import sys
import re
from algorithm.li.extract.utils.dbutils import dbs
from algorithm.li.extract.templates.edu_template import *

# word_bag = ["留学", "毕业", "学位", "硕士", "博士", "学士", "研究生", "专业", "方向"]
# school_dict = {}.fromkeys(open(DIR + '\\dicts\\in.txt', 'r', encoding='utf-8').read().split('\n'))


class TextAttribute:
    def __init__(self, text=""):
        self.text = text
        self.lines = []
        self.gravities = []

    # 计算句子权重
    def compute_gravity(self):
        for line in self.lines:
            s = ""
            for r in re_edu:
                if re.findall(r, line):
                    s += "1"
                else:
                    s += "0"
            self.gravities.append(s)

    # 分句
    def seg_sentence(self, r=r'\n'):
        lines = re.split(r, self.text)
        self.lines = lines

    # 得到准确的描述学历的句子
    def filter_sentence(self):

        pass

    def set_text(self, text=""):
        self.text = text
        self.lines = []
        self.gravities = []

    def get_edu_long_item(self):

        pass

    def get_edu_items(self):
        reList = r'教育经历|学习经历|教育背景|教育及培训经历|教育简历'
        start = 0
        for i in range(0, len(self.lines)):
            if re.findall(reList, self.lines[i]):
                start = i
                break
        index_list = []
        if start + 1 < len(self.lines) and similarity_gravities(self.gravities[start + 1], "1111111") > 2:
            index_list.append(start)
        if re.findall(reList, self.lines[start]) and start + 1 < len(self.lines):

            if start + 1 >= len(self.lines):
                return None, None
            if similarity_gravities(self.gravities[start + 1], "1111111") < 2:
                return None, None
            index_list.append(start + 1)
            end = start + 7 + 1 if start + 7 + 1 < len(self.lines) else len(self.lines)
            for i in range(start + 2, end):
                if similarity_gravities(self.gravities[i-1], self.gravities[i]) > 1 or similarity_gravities(self.gravities[i], "1111111") > 1:
                    index_list.append(i)
                else:
                    break
            try:
                return 1, [self.lines[i] for i in index_list]
            except:
                print(index_list)
                pass
            pass
        else:
            #
            start = 0
            for i in range(0, len(self.lines)):
                if similarity_template(self.gravities[i]):
                    start = i
                    break
            if start == 0:
                return None, None
            index_list = []
            index_list.append(start)
            end = start + 5 if start + 5 <= len(self.lines) else len(self.lines)
            for i in range(start + 1, end):
                if similarity_template(self.gravities[i]):
                    index_list.append(i)
            return 2, [self.lines[i] for i in index_list]
            pass


def similarity_template(line=""):
    for tem, value in sentence_template.items():
        if similarity_gravities(line, tem) >= value:
            return True

    return False


def similarity_gravities(line1, line2):
        num = 0
        for i in range(0, len(line1)):
            if line1[i] == line2[i] and line1[i] == '1':
                num += 1
        return num


def get_edu_exp():
    select_sql = "select id, info_clear from teacher_eduexp where type = 0"

    teacher_list = dbs.getDics(select_sql)
    print(len(teacher_list))
    ta = TextAttribute()

    num = 0
    update_list = []
    for teacher in teacher_list:
        if teacher["info_clear"] is None or teacher["info_clear"] == "":
            continue
        # print(teacher["id"])
        ta.set_text(teacher["info_clear"])

        ta.seg_sentence("\n")
        ta.compute_gravity()
        t, edu_items = ta.get_edu_items()
        if edu_items:
            print(teacher["id"])
            print(t, edu_items)
            num += 1
            update_list.append(("\n".join(edu_items), t, teacher["id"]))
            continue
        # ta.get_edu_long_item()

    print(num)
    print(len(update_list))
    update_sql = "update teacher_eduexp set edu_exp=%s, type=%s where id = %s"
    print(dbs.exe_many(update_sql, update_list))


if __name__ == "__main__":

    # get_age()
    # get_overseas_exp()
    # institution_email()
    # get_email()
    # test()
    get_edu_exp()
    pass
