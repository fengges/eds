"""

org, date, degree, country, state_or_province, major, discipline_category, graduate
org:机构
date:时间
degree:学位信息
country:国家
state_or_province:省、州
major:专业
discipline_category:学科
graduate:“毕业”


"org,date,degree": "{0} {1}，获得{2}学位"
"org,date,degree,major": "{0} {1}{2}专业，获得{3}学位"
"org,degree": "{0} 获得{1}学位"
"org,degree,state_or_province": "{0}{1}，获得{2}学位"
"org,date,degree,country": "{0} {1}{2}，获得{3}学位"
"org,date,degree,state_or_province": "{0} {1}{2}，获得{3}学位"
"org,date,major": "{0} {1}{2}专业"
"org,date,degree,country,state_or_province": "{0} {1}{2}{3}，获得{4}学位"
"org,degree,country": "{0}{1}，获得{2}学位"
"org,degree,major": "{0}{1}，获得{2}学位"
"org,date,graduate": "{0} 毕业于{1}"
"org,date,state_or_province,graduate": "{0} 毕业于{1}{2}"
"org,date,degree,country,major": "{0} {1} {2}{3}专业，获得{4}学位"
"org,date,major,graduate": "{0} 毕业于{1}{2}专业"
"date,degree": "="
"org,date,degree,state_or_province,major": "{0} {1} {2}{3}专业，获得{4}学位"
"org,degree,country,state_or_province": "{1} {2} {3}，获得{4}学位"
"date,degree,state_or_province": "="
"date,degree,major": "{0} 获得{1}{2}学位"
"org,degree,state_or_province,major": "{0} {1} 学习{2}专业，获得{3}学位"
"date,major,graduate": "{0} 毕业于{2}专业"
"org,degree,country,major": "{0} {1} 学习{2}专业，获得{3}学位"
"org,date,state_or_province": "{0} 进入{1}学习"
"org,date,degree,country,state_or_province,major": "{0} {1}{2}专业，获得{3}学位"
"date,state_or_province,major,graduate": "{0} 毕业于{1}{2}专业"
"org,date,country,state_or_province,graduate": "{0} 毕业于{1}"
"org,date,degree,discipline_category": "{0} {1}，获得{2}{3}学位"
"org,degree,discipline_category": "{1}，获得{2}{3}学位"
"org,degree,state_or_province,discipline_category": "{1}，获得{2}{3}学位"
"org,date,degree,state_or_province,discipline_category": "{0} {1}，获得{2}{3}学位"
"org,date,degree,major,discipline_category": "{0} {1}{2}专业，获得{3}{4}学位"
"org,date,degree,country,discipline_category": "{0} {1}，获得{2}{3}学位"
"org,date,degree,country,major,discipline_category": "{0} {1}，获得{2}{3}学位"
"org,date,degree,country,state_or_province,discipline_category": "{0} {1}，获得{2}{3}学位"
"org,date,degree,state_or_province,major,discipline_category": "{0} {1}{2}专业，获得{3}{4}学位"
"org,degree,country,discipline_category": "{0}，获得{1}{2}学位"
"org,degree,major,discipline_category": "{0}{1}专业，获得{1}{2}学位"
"org,degree,country,major,discipline_category": "{0}{1}专业，获得{1}{2}学位"
"org,date,degree,country,state_or_province,major,discipline_category": "{0} {1}{2}专业，获得{3}{4}学位"
"org,degree,state_or_province,major,discipline_category": "{0}{1}专业，获得{1}{2}学位"
"org,date,country,graduate": "{0} 毕业于{1}"

"""

sentence_template = [
    "org,date,degree",
    "org,date,degree,major",
    "org,degree",
    "org,degree,state_or_province",
    "org,date,degree,country",
    "org,date,degree,state_or_province",
    "org,date,major",
    "org,date,degree,country,state_or_province",
    "org,degree,country",
    "org,degree,major",
    "org,date,graduate",
    "org,date,state_or_province,graduate",
    "org,date,degree,country,major",
    "org,date,major,graduate",
    "date,degree",
    "org,date,degree,state_or_province,major",
    "org,degree,country,state_or_province",
    "date,degree,state_or_province",
    "date,degree,major",
    "org,degree,state_or_province,major",
    "date,major,graduate",
    "org,degree,country,major",
    "org,date,country",
    "date",
    "org,date,state_or_province",
    "org,date,degree,country,state_or_province,major",
    "state_or_province,graduate",
    "date,state_or_province,major,graduate",
    "org,date,country,state_or_province,graduate",
    "date,degree,state_or_province,major",
    "org,date,degree,discipline_category",
    "org,degree,discipline_category",
    "org,degree,state_or_province,discipline_category",
    "org,date,degree,state_or_province,discipline_category",
    "org,date,degree,major,discipline_category",
    "org,date,degree,country,discipline_category",
    "org,date,degree,country,major,discipline_category",
    "org,date,degree,country,state_or_province,discipline_category",
    "org,date,degree,state_or_province,major,discipline_category",
    "org,degree,country,discipline_category",
    "org,date",
    "org,degree,major,discipline_category",
    "org,degree,country,major,discipline_category",
    "org,date,degree,country,state_or_province,major,discipline_category",
    "org,degree,state_or_province,major,discipline_category",
    "org,date,country,graduate"
]

sentence_format = {
    "org,date,degree": "{0} {1}，获得{2}学位",
    "org,date,degree,major": "{0} {1}{2}专业，获得{3}学位",
    "org,degree": "{0} 获得{1}学位",
    "org,degree,state_or_province": "{0}{1}，获得{2}学位",
    "org,date,degree,country": "{0} {1}，获得{2}学位",
    "org,date,degree,state_or_province": "{0} {1}，获得{2}学位",
    "org,date,major": "{0} {1}{2}专业",
    "org,date,degree,country,state_or_province": "{0} {1}，获得{2}学位",
    "org,degree,country": "{0}{1}，获得{2}学位",
    "org,degree,major": "{0}{1}，获得{2}学位",
    "org,date,graduate": "{0} 毕业于{1}",
    "org,date,state_or_province,graduate": "{0} 毕业于{1}{2}",
    "org,date,degree,country,major": "{0} {1}{2}专业，获得{3}学位",
    "org,date,major,graduate": "{0} 毕业于{1}{2}专业",
    "org,date,degree,state_or_province,major": "{0} {1} {2}{3}专业，获得{4}学位",
    "org,degree,country,state_or_province": "{0} {1} {2}，获得{3}学位",
    "date,degree,state_or_province": "=",
    "date,degree,major": "{0} 获得{1}{2}学位",
    "org,degree,state_or_province,major": "{0} {1} 学习{2}专业，获得{3}学位",
    "date,major,graduate": "{0} 毕业于{1}专业",
    "org,degree,country,major": "{0} {1} 学习{2}专业，获得{3}学位",
    "org,date,state_or_province": "{0} 进入{1}学习",
    "org,date,degree,country,state_or_province,major": "{0} {1}{2}专业，获得{3}学位",
    "date,state_or_province,major,graduate": "{0} 毕业于{1}{2}专业",
    "org,date,country,state_or_province,graduate": "{0} 毕业于{1}",
    "org,date,degree,discipline_category": "{0} {1}，获得{2}{3}学位",
    "org,degree,discipline_category": "{0}，获得{1}{2}学位",
    "org,degree,state_or_province,discipline_category": "{0}，获得{1}{2}学位",
    "org,date,degree,state_or_province,discipline_category": "{0} {1}，获得{2}{3}学位",
    "org,date,degree,major,discipline_category": "{0} {1}{2}专业，获得{3}{4}学位",
    "org,date,degree,country,discipline_category": "{0} {1}，获得{2}{3}学位",
    "org,date,degree,country,major,discipline_category": "{0} {1}，获得{2}{3}学位",
    "org,date,degree,country,state_or_province,discipline_category": "{0} {1}，获得{2}{3}学位",
    "org,date,degree,state_or_province,major,discipline_category": "{0} {1}{2}专业，获得{3}{4}学位",
    "org,degree,country,discipline_category": "{0}，获得{1}{2}学位",
    "org,degree,major,discipline_category": "{0}{1}专业，获得{1}{2}学位",
    "org,degree,country,major,discipline_category": "{0}{1}专业，获得{1}{2}学位",
    "org,date,degree,country,state_or_province,major,discipline_category": "{0} {1}{2}专业，获得{3}{4}学位",
    "org,degree,state_or_province,major,discipline_category": "{0}{1}专业，获得{1}{2}学位",
    "org,date,country,graduate": "{0} 毕业于{1}"
}

