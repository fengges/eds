
from eds.dao.school.schooldao import school_dao
from eds.config import environment


class SchoolService:

    def get_info(self, params):
        infoEty = school_dao.get_info(params)
        if not infoEty:
            return None
        import re
        info_dict = infoEty[0]

        info = dict()
        info["id"] = info_dict["id"]
        info["name"] = info_dict["name"]
        info["english_name"] = info_dict["english_name"]
        info["characteristic"] = info_dict["characteristic"]
        info["logo"] = "/main/schpic/" + str(info_dict["id"])

        abstract = info_dict["abstract"]
        abstract_list = re.findall(r'.*?。', abstract)
        info["abstract"] = abstract_list[0]
        info["school_type"] = info_dict["school_type"]
        info["establish"] = info_dict["establish"]
        info["subjection"] = info_dict["subjection"]
        key_list = ["name", "english_name", "establish", "school_type", "subjection",
                    "national_disciplines", "master_point", "doctoral_point", "school_motto"]
        word_list = ["中文名", "外文名", "创办时间", "类别", "主管部门", "国家重点学科", "硕士点", "博士点", "校训"]
        info_list = []
        for i in range(0, len(key_list)):
            content = info_dict.get(key_list[i], "")
            # import re
            # content = re.sub(" ", "", content)
            if content != "":

                if key_list[i] in ["master_point", "national_disciplines", "doctoral_point"]:
                    value = content.split(',')
                    for j in range(0, len(value)):
                        item = dict()
                        if j == 0:
                            item["title"] = word_list[i]
                        else:
                            item["title"] = ""
                        item["content"] = value[j]
                        info_list.append(item)
                else:
                    item = dict()
                    item["title"] = word_list[i]
                    item["content"] = content
                    info_list.append(item)

        iter_info = eval(info_dict["info"])
        for key, value in iter_info.items():
            if key not in word_list:
                if type(value) == list:
                    for i in range(0, len(value)):

                        item = dict()
                        if i == 0:
                            item["title"] = key
                        else:
                            item["title"] = ""
                        item["content"] = value[i]
                        info_list.append(item)
                else:
                    item = dict()
                    item["title"] = key
                    item["content"] = value
                    info_list.append(item)

        length = len(info_list)
        mid = int(length/2)
        while mid <= length and info_list[mid]["title"] == "":
            mid += 1

        info["info_list_l"] = info_list[0: mid]
        info["info_list_r"] = info_list[mid:]

        l_len = len(info["info_list_l"])
        r_len = len(info["info_list_r"])
        if l_len > r_len:
            max_len = l_len
        else:
            max_len = r_len
        info["max_len"] = max_len
        info["l_len"] = l_len
        info["r_len"] = r_len
        return info

    def get_teacher(self, params):
        result = school_dao.get_teacher(params)
        return result

    def get_discipline(self, params):
        result = school_dao.get_discipline(params)
        dis_words = ["人文社科类", "理学", "工学", "管理学", "医学", "农学", "艺术学"]
        dis_dict = dict()
        for word in dis_words:
            level_list = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-"]
            i_list = list()
            for level in level_list:
                if i_list:
                    i_list.extend([i for i in result if i["xueke1"] == word and i["level"] == level])
                else:
                    i_list = [i for i in result if i["xueke1"] == word and i["level"] == level]
            if i_list:
                dis_dict[word] = i_list
        return dis_dict

    def get_pic(self, params):
        try:
            image = open(environment['file']["pic_url"] + 'SchoolImgs/' + str(params) + '.jpg', 'rb')
        except:
            image = open(environment['file']["pic_url"] + 'SchoolImgs/demo.jpg', 'rb')
        return image


schoolService = SchoolService()

if __name__ == "__main__":
    schoolService.get_discipline("清华大学")
    pass