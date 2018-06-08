from flask import Blueprint, render_template
from eds.service.school.schoolservice import schoolService

main_school = Blueprint('main_school', __name__)


@main_school.route('/main/school/<param>')
def show_school(param):
    infoEty = schoolService.get_info(param)
    print(infoEty)
    if not infoEty:
        return render_template('/main/notfound.html')
    info_dict = infoEty[0]
    info_1 = dict()
    info_1["name"] = info_dict["name"]
    info_1["english_name"] = info_dict["english_name"]
    info_1["url"] = info_dict["url"]
    info_1["province"] = info_dict["province"]
    info_1["logo"] = info_dict["logo"]
    info_1["abstract"] = info_dict["abstract"]

    info_2 = []
    key_list = ["school_type", "level", "characteristic", "subjection", "school_motto", "attribute", "establish", "address"]
    word_list = ["类型", "级别", "特质", "主管部门", "校训", "属性", "创办时间", "学校地址"]
    for i in range(0, len(key_list)):
        label = info_dict.get(key_list[i])
        import re
        label = re.sub(" ", "", label)
        if label is not None and label != "":
            info_2.append((word_list[i], label))
    print(info_2)

    teacher_list = schoolService.get_teacher(info_1["name"])
    teachers = []
    print(teacher_list)
    for t in teacher_list:
        teacher = dict()
        teacher["name"] = t["name"]
        teacher["title"] = "" if t["title"] is None else t["title"]
        teacher["pic"] = t["pic"]
        teacher["institution"] = t["institution"]
        teacher["fields"] = "" if t["fields"] is None else t["fields"]
        teacher["url"] = "/main/profile/%s" % t["id"]
        teachers.append(teacher)

    return render_template('/main/schoolpage.html', info_dict=info_1, info_list=info_2, teachers=teachers)
