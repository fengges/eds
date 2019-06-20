# import random
# randint = random.randint(1,10)
# print(randint)

# from baiduxueshu.spiders import mysql
# db = mysql.LocalDB()
#
# a = db.getAuthor()
# print('a',a)

# import re
# url = 'http://xueshu.baidu.com/s?wd=%22%E6%9D%8E%E5%81%A5%22%20%22%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%22%20author%3A%28%E6%9D%8E%E5%81%A5%29&pn=5550&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1&rsv_page=1'
# page = re.findall(r"pn=([0-9]+)", url)[0]
# print(page)

# dic = {
#    '1':'知网',
#    '2':'维普',
#    '3':'万方'
# }
#
# a = dic.setdefault('4',None)
# print(a)

# import time
# time.sleep(3)
# print('kljkl')
#
# import requests
#
# url = 'http://47.106.180.108:8081/Index-generate_api_url.html?packid=7&fa=5&qty=10&port=1&format=txt&ss=1&css=&pro=&city='
# data = requests.get(url).text
# f1 = open('ippool.txt','w')
# f1.write(data)
# f1.close()

# s = "课程设置是诊所法律教育的核心。实证的数据表明,在课程目标上我们有必要适当调整学生的目标定位,强调职业道德的培养。在课程结构上,值班指导部分和课堂教学部分按70:3..."
#
# print(s[-3:])

# import uuid
# # while 1:
# #     print(uuid.uuid1())
#
# print(str(uuid.uuid1()))


# from spider.baiduxueshu.baiduxueshu.spiders import mysql
# db = mysql.TestDB()
#
# teacherlist = db.getAuthor()
# print(teacherlist)

import time
import requests
# url = "http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="
# data = requests.get(url).text
# iplist = data.split('\r\n')
# print('iplist')
# print(iplist)
# print(iplist[0].find('当前用户可用的有效IP数量不够'))
# if iplist[0].find('当前用户可用的有效IP数量不够'):
#     time.sleep(2)
#     print('时间ip不够用')

# iplist = ['saf:当前用户可用的有效IP数量不够']
# print(iplist[0].find('当前用户可用的有效IP数量不够'))