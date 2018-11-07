from algorithm.li.extract.utils.dbutils import dbs


def get_age():
    """
    1.年龄-age
    age值:(0,20,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100)
    范围	    权重
    NULL    0
    0		0
    20-30	1
    30-55	5
    55-65	3
    >65		2
    :return: None
    """
    sql_intial = '''
        UPDATE teacher_rank
        SET teacher_rank.age = 0
    '''
    sql_1 = '''
        UPDATE teacher_rank, teacher_age
        SET teacher_rank.age = 1
        WHERE teacher_age.id = teacher_rank.teacher_id AND teacher_age.age >= 20 AND teacher_age.age < 30
    '''
    sql_5 = '''
        UPDATE teacher_rank, teacher_age
        SET teacher_rank.age = 5
        WHERE teacher_age.id = teacher_rank.teacher_id AND teacher_age.age >= 30 AND teacher_age.age < 55
    '''
    sql_3 = '''
        UPDATE teacher_rank, teacher_age
        SET teacher_rank.age = 3
        WHERE teacher_age.id = teacher_rank.teacher_id AND teacher_age.age >= 55 AND teacher_age.age < 65
    '''
    sql_2 = '''
        UPDATE teacher_rank, teacher_age
        SET teacher_rank.age = 1
        WHERE teacher_age.id = teacher_rank.teacher_id AND teacher_age.age >= 65
    '''
    print(dbs.exe_sql(sql_intial))
    print(dbs.exe_sql(sql_1))
    print(dbs.exe_sql(sql_5))
    print(dbs.exe_sql(sql_3))
    print(dbs.exe_sql(sql_2))
    pass


def get_integrity():
    """
    2.信息完整度-integrity
    title,institution,theme,eduexp,email
    情况	    权重
    存在	    1
    不存在	0
    :return: None
    """

    sql_initial = '''
        UPDATE teacher_rank
        SET integrity = 0
    '''
    sql_title = '''
        UPDATE teacher_rank, teacher
        SET integrity = integrity + 1
        WHERE teacher_rank.teacher_id = teacher.id and teacher.title IS NOT NULL AND teacher.title != ""
    '''
    sql_institution = '''
        UPDATE teacher_rank, teacher
        SET integrity = integrity + 1
        WHERE teacher_rank.teacher_id = teacher.id and teacher.institution IS NOT NULL AND teacher.institution != ""
    '''
    sql_theme = '''
        UPDATE teacher_rank, teacher
        SET integrity = integrity + 1
        WHERE teacher_rank.teacher_id = teacher.id and teacher.theme IS NOT NULL AND teacher.theme != ""
    '''
    sql_eduexp = '''
        UPDATE teacher_rank, teacher
        SET integrity = integrity + 1
        WHERE teacher_rank.teacher_id = teacher.id and teacher.eduexp IS NOT NULL AND teacher.eduexp != ""
    '''
    sql_email = '''
        UPDATE teacher_rank, teacher
        SET integrity = integrity + 1
        WHERE teacher_rank.teacher_id = teacher.id and teacher.email IS NOT NULL AND teacher.email != ""
    '''
    print(dbs.exe_sql(sql_initial))
    print(dbs.exe_sql(sql_title))
    print(dbs.exe_sql(sql_institution))
    # print(dbs.exe_sql(sql_theme))
    print(dbs.exe_sql(sql_eduexp))
    print(dbs.exe_sql(sql_email))

    pass


def get_title():
    """
    3.title值:(副教授,副研究员,助教,助理教授,助理研究员,实验师,工程师,微软亚洲研究院副院长,教授,研究员,讲师,设备管理员,辅导员,高工,高级实验师,高级工程师)
    值			权重
    教授		    4
    副教授		3
    助理教授	    2
    助理研究员	1
    其他		    0
    :return: None
    """
    sql_initial = '''
            UPDATE teacher_rank
            SET title = 0
    '''
    sql_4 = '''
            UPDATE teacher_rank, teacher
            SET teacher_rank.title=4
            WHERE teacher_rank.teacher_id = teacher.id and teacher.title="教授"
    '''
    sql_3 = '''
            UPDATE teacher_rank, teacher
            SET teacher_rank.title=3
            WHERE teacher_rank.teacher_id = teacher.id and teacher.title="副教授"
    '''
    sql_2 = '''
            UPDATE teacher_rank, teacher
            SET teacher_rank.title=4
            WHERE teacher_rank.teacher_id = teacher.id and teacher.title="助理教授"
    '''
    sql_1 = '''
            UPDATE teacher_rank, teacher
            SET teacher_rank.title=4
            WHERE teacher_rank.teacher_id = teacher.id and teacher.title="助理研究员"
    '''

    print(dbs.exe_sql(sql_initial))
    print(dbs.exe_sql(sql_4))
    print(dbs.exe_sql(sql_3))
    print(dbs.exe_sql(sql_2))
    print(dbs.exe_sql(sql_1))
    pass


def get_school():
    """
    4.学校评价-school
    值  权重
    985 2
    211 1
    非  0
    :return: None
    """
    sql_initial = '''
        UPDATE teacher_rank
        SET school = 0
    '''
    print(dbs.exe_sql(sql_initial))

    s_sql = '''
        SELECT teacher.id as id, school_info.characteristic as characteristic
        FROM `teacher`, `school_info`
        WHERE teacher.school_id = school_info.id AND teacher.school_id != 0;
    '''
    import re
    teacher_list = dbs.getDics(s_sql)
    print(len(teacher_list))
    u_list = []
    for teacher in teacher_list:
        if teacher['characteristic'] is None or teacher['characteristic'] == "":
            continue
        if re.findall('985', teacher['characteristic']):
            u_list.append((2, teacher['id']))
        elif re.findall('211', teacher['characteristic']):
            u_list.append((1, teacher['id']))
    print(len(u_list))
    u_sql = '''
        UPDATE teacher_rank
        SET school=%s
        WHERE teacher_id=%s
    '''
    print(dbs.exe_many(u_sql, u_list))
    pass


def get_institution():
    """
    5.学院评价-institution
    值				权重
    一级重点学科	    2
    二级重点学科	    1
    无				0
    :return:
    """
    sql_initial = '''
            UPDATE teacher_dis_code
            SET dis_rank = 0
        '''
    print(dbs.exe_sql(sql_initial))

    s_sql = '''
        SELECT teacher_dis_code.school, teacher_dis_code.discipline_code, discipline_school.`code`
        FROM `teacher_dis_code`,`discipline_school` 
        WHERE teacher_dis_code.discipline_code != '' 
        AND teacher_dis_code.discipline_code IS NOT NULL 
        AND teacher_dis_code.discipline_code = discipline_school.root
        AND teacher_dis_code.school = discipline_school.school
        GROUP BY teacher_dis_code.school, teacher_dis_code.discipline_code, discipline_school.`code`;
    '''
    data_list = dbs.getDics(s_sql)
    u_list = []
    for data in data_list:
        if len(data['code']) == 4:
            u_list.append((5, data['school'], data['discipline_code']))
        elif len(data['code']) == 6:
            u_list.append((1, data['school'], data['discipline_code']))

    print(len(u_list))
    u_sql = '''
        UPDATE teacher_dis_code
        SET dis_rank = dis_rank + %s
        WHERE school=%s AND discipline_code=%s
    '''
    print(dbs.exe_many(u_sql, u_list))

    sql_initial_rank = '''
        UPDATE teacher_rank, teacher_dis_code
        SET teacher_rank.institution = teacher_dis_code.dis_rank
        WHERE teacher_rank.teacher_id = teacher_dis_code.id;
    '''
    print(dbs.exe_sql(sql_initial_rank))


def get_main_lab():
    """
    6.重点实验室-main_lab
    值	权重
    yes	1
    no	0
    :return: None
    """

    pass


def get_abroad():
    """
    6.留学经历-abroad
    值   权重
    yes 1
    no  0
    :return: None
    """
    sql = '''
        UPDATE teacher_edu_description, teacher_rank
        SET teacher_rank.abroad=teacher_edu_description.abroad
        WHERE teacher_edu_description.id = teacher_rank.teacher_id
    '''

    print(dbs.exe_sql(sql))

    pass


def get_total():
    """
    1：各维度归一化后相加
    2：非985/211的总分为0, 985学校总分*2
    3：重点实验室
    :return:
    """
    import pandas as pd

    s_sql = '''
        SELECT teacher_id, age, integrity, title, school, institution, main_lab, abroad FROM teacher_rank
    '''
    df = dbs.get_teacher_dataframe(s_sql)
    df_id = df['teacher_id']
    df_normal = df / df.max()
    df_normal['total'] = df_normal['age'] + df_normal['integrity'] + df_normal['title'] + df_normal['school'] + df_normal['institution'] + df_normal['main_lab'] + df_normal['abroad']

    u_list = []
    for index in df_normal.index:
        total = df_normal.loc[index].total
        id = df_id[index]

        # 非985/211的总分为0, 985学校总分*2
        if df_normal.loc[index].school == 0.0:
            total = 0
        elif df_normal.loc[index].school == 1.0:
            total = total + df_normal.loc[index].total

        # 重点实验室
        total = total + df_normal.loc[index].total * df_normal.loc[index].main_lab

        u_list.append((float(total), int(id)))

    print(len(u_list))
    u_sql = 'UPDATE teacher_rank SET total = %s WHERE teacher_id = %s'
    print(dbs.exe_many(u_sql, u_list))
    pass


if __name__ == "__main__":
    # get_age()
    # get_integrity()
    # get_title()
    # get_school()
    # get_institution()
    # get_abroad()
    get_total()
    pass
