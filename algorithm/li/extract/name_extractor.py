
import re
from algorithm.li.extract.utils.dbutils import dbs


def ex_name(text=""):
    if text == "" or text is None:
        return ""

    CHNAME = {}.fromkeys(open('.\\dicts\\CN_LNAME.txt', 'r', encoding='utf8').read().split('\n'))
    reNAME = r'({0}[\u4E00-\u9FA5]+)'
    chunk = text
    # 缩小遍历的块
    try:
        size = 50
        start = re.search(r'姓名|个人简历', text).start()
        if start >= 0:
            length = len(text)
            chunk = text[start:start + size if start + size < length else length]
    except:
        print("")

    try:
        for i in range(0, len(chunk)):
            if CHNAME.get(text[i], "") != "":
                the_name = re.findall(reNAME.format(text[i]), chunk)
                if the_name and len(the_name) <= 3:
                    the_name = the_name[0]
                    print(the_name)
                    return the_name
    except:
        print("出错")

    return ""


def get_name():
    s_sql = "SELECT id, name, info FROM `teacherdata_info` LIMIT 1000;"
    teacher_data = dbs.getDics(s_sql)
    sum = 0
    for teacher in teacher_data:
        info = teacher['info']
        name = ex_name(info)
        if name == teacher['name']:
            sum += 1
            print(True)
        else:
            print(False)

    print(len(teacher_data))
    print(sum)


if __name__ == "__main__":
    get_name()
    pass
