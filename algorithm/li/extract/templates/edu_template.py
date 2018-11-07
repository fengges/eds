
# 通过正则匹配re_edu
# 得到长度为 7 的字符串 表示
# 时间 毕业 大学 学院/学系 博士/硕士/学士 学位 研究生
# 教育经历模板
# 句子中存在为1, 不存在为0

re_edu = [r'[1-2][9,0][0-9]{2}', r'毕业', r'大学', r'学院|学系', r'博士|硕士|学士|访问学者', r'学位', r'研究生']
re_title_name = []


# gravities满足
# 1111111 >= 3 and
# 1100110 >= 3 or 0100111 >= 2

# 时间 毕业 大学 学院/学系 博士/硕士/学士 学位 研究生

# 大学 博士/硕士/学士
#   0   0    1     0        1           0       0   :   2

# 年份 博士/硕士/学士
#   1   0    0     0        1           0       0   :   3

# 年份 毕业
#   1   1    0     0        0           0       0   :   2

# 年份 学位
#   1   0    0     0        0           1       0   :   2

# 博士/硕士/学士 学位
#   0   0    0     0        1           0       0   :   2

sentence_template = {
    "0010100": 3, "1000100": 3, "1100000": 2, "1000010": 2, "0000100": 2
}


"""
--- 初步抽取 ---

-问题-

# 出生描述
# 备注 年份与“出生”之间没有, ：。等符号的为出生年份

# ***工作经历描述***
# 任
# 任教
# 留校
# 含有职称:  "副教授", "助理教授", "教授", "讲师", "助教", "副研究员", 
#           "助理研究员", "研究员", "高级工程师", "高级实验师", "高工", "工程师", "实验师"
# 年份 大学 博士生*导师*
# 年份较迟

# ***学历与工作经历一起描述***
# 博士/硕士/学士学位
# 学历
# 工作经历年份较迟

# ***出版物描述***
# 年份较迟
# 《 》
# 出版
# 杂志
# 学报

# ***长句子***
# 按，；分句

# ***课程描述***
# 主讲课程
# 授课

-专业描述特征-

# 1.最后一个字为“学”
# 2.位于“专业”的前面（优先）
# 3.位于学位(学士/硕士/博士)描述的前面
# 4.获(.*?)学士/硕士/博士
# 5.学院/系(.*?)专业

"""

"""
--- 抽取 2 ---
部分机构实体识别效果不好
"""

format_org = ['于', ',', '，', '在', '[0-9]', ' ', '获']
re_org = r'{0}([\u4E00-\u9FA5]+?大学)'
