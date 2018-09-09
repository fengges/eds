from algorithm.li.extract.utils.dbutils import dbs
import re
from urllib import parse as pa


def data_clean():
    """
    将javascript的链接转换为正常
    :return:
    """
    data_list = dbs.getDics("SELECT * FROM `eds_985teacher` WHERE link like '%javascript%' AND school = '中南大学';")
    print(len(data_list))
    u_list = []
    for data in data_list:
        id = data['id']
        '''javascript:window.open('/blog/content2?name='+encodeURI('周雄伟'))'''
        link = data['link']
        if link != "":
            p_tuple = re.findall(r"open\('(.+?)'\+encodeURI\('(.+?)'\)\)", link)[0]

            link = p_tuple[0] + pa.quote(p_tuple[1])
            # print(pa.urljoin(data['institution_url'], link))
            link = pa.urljoin(data['institution_url'], link)
            print(link)
            u_list.append((link, id))

    print(len(u_list))
    u_sql = "UPDATE eds_985teacher SET all_link=%s WHERE id = %s"
    print(dbs.exe_many(u_sql, u_list))


if __name__ == "__main__":
    data_clean()
