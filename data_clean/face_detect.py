import pymysql.cursors
import re
from aip import AipFace
import requests
import os
import hashlib
import shutil
import time
from PIL import Image,ImageDraw
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='eds',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    def get_img_url(self):
        sql = "SELECT * FROM teacher_img"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def InsertBaiduface(self, item):
        sql = "INSERT INTO teacher_img_baiduface VALUES(%s,%s)"
        self.cursor.execute(sql, item)
        self.connect.commit()

    def get_img_info(self):
        sql = "SELECT * FROM teacher_img_baiduface"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

def cutimg(img,location):
    x_len, y_len = img.size
    x = location['left'] + location['width'] / 2
    y = location['top']

    if x_len == y_len: return img
    if x_len > y_len:
        D = x_len - y_len
        x1 = D * x / x_len
        x2 = x_len - D * (1 - x / x_len)
        box = (x1, 0, x2, y_len)
        cropImg = img.crop(box)
        return cropImg
    if y_len > x_len:
        D = y_len - x_len
        y1 = D * y / y_len
        y2 = y_len - D * (1 - y / y_len)
        box = (0, y1, x_len, y2)
        cropImg = img.crop(box)
        return cropImg

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

""" 你的 APPID AK SK """
APP_ID = '10909275'
API_KEY = 'q1jLbdVpVbLmM7cIGiw2O0kt'
SECRET_KEY = 'yzB9cHPyCHPGTPztUFTqYonGw6vThssR'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def getPicinfo(imagename):
    image = get_file_content(imagename)
    # """ 调用人脸检测 """
    # a = client.detect(image);

    """ 如果有可选参数 """
    options = {}
    options["max_face_num"] = 10
    # options["face_fields"] = "age"

    """ 带参数调用人脸检测 """
    a = client.detect(image, options)
    if a['result']==1:
        b = a['result'][0]['location']
        b ['result_num'] = a['result_num']
    else:
        b = a
    return b

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        # print("move %s -> %s"%( srcfile,dstfile))

def get_md5(file_path):
  md5 = None
  if os.path.isfile(file_path):
    f = open(file_path,'rb')
    md5_obj = hashlib.md5()
    md5_obj.update(f.read())
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
  return md5


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        # print(files) #当前路径下所有非目录子文件
        return files

def getDomain(url):
    reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
    m = re.match(reg, url)
    uri = m.groups()[0] if m else ''
    temp = uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
    index = url.index(temp) + len(temp)
    return url[0:index]

def getTeacherUrl(url,image_url):
    image_url = image_url.strip()
    domain=getDomain(url)
    if len(image_url) == 0:
        return ' '
    if image_url[0:4] == 'http':
        return image_url
    if image_url[0] == '/':
        return domain + image_url
    elif url[-1] == '/' and image_url[0] == '.':
        return url + image_url
    elif url[-1] == '/':
        index = url[0:-1].rfind('/')
        if index == -1:
            l = url + image_url
        else:
            l = domain + '/' + image_url
        return l
    else:
        index = url.rfind('/')
        return url[0:index + 1] + image_url


def download_pic(path=''):
    """
    下载图片到 path
    注：数据请求与格式产生变化需要修改
    """
    db = Mysql()
    #获取图片链接
    data = db.get_img_url()
    data = data[::-1]
    for node in data:
        id = node['id']
        homepage = node['homepage']
        im_url_list = node['image'].split('-link-')

        i = 1
        for im_url in im_url_list:
            if im_url=="":continue
            url = getTeacherUrl(homepage, im_url)
            print(url)

            try:
                pic_url = url
                req = requests.get(pic_url,timeout=3)
                # pic_md5 = hashlib.md5(pic_url.encode('utf - 8')).hexdigest()
                fp = open("%s//%s.jpg" % (path,str(id)+"-"+str(i)), 'wb')
                fp.write(req.content)
                fp.close()
            except:
                print('url错误')
            i+=1

def clean_pic(source_path,new_path):
    """
    把source_path中的图片中重复不超过两次的图片移动到new_path中
    """
    im_data = file_name(source_path)
    im_md5_dic = {}
    for im in im_data:
        imd5 = get_md5(source_path+'/'+im)
        if imd5 in im_md5_dic.keys():
            im_md5_dic[imd5].append(im)
        else:im_md5_dic[imd5] = [im]
    for v in im_md5_dic.values():
        if len(v)<3:
            mymovefile(source_path+'/'+v[0],new_path+'/'+v[0])

def baiduface(file_dir):
    """
    调用百度人脸识别接口对file_dir中的所有图片进行识别
    速度为1s/张
    识别信息存放在数据库中
    """
    db = Mysql()
    imglist = file_name(file_dir)
    for imgname in imglist:
        try:
            picid = imgname.split('-')[0]
            resultdir = getPicinfo(file_dir+ '/'+imgname)
            resultdir['picid'] = picid
            resultdir['imgname'] = imgname
            print(imgname)
            # print(resultdir)
            db.InsertBaiduface((imgname,str(resultdir)))
            time.sleep(1)
        except Exception as e:
            print(imgname+'错误')
            print(e)

def pick_pic(file_dir,face_dir,cut_dir):
    db = Mysql()
    imglist = file_name(file_dir)
    imginfodata = db.get_img_info()
    imginfodic = {}
    for node in imginfodata:
        imginfodic[node['id']] = eval(node['info'])

    for imgname in imglist:
        try:
            print(imgname,imginfodic[imgname])
            if imginfodic[imgname]['result_num'] == 1:
                id = imgname.split('-')[0]

                mycopyfile(file_dir+'/'+imgname,face_dir+'/'+id + '.jpg')

                img = Image.open(file_dir+'/'+imgname).convert('RGB')
                newpic = cutimg(img, imginfodic[imgname]['result'][0]['location'])
                newpic.save(cut_dir+'/' +id + '.jpg')
                newpic.close()
        except Exception as e:
            print(imgname,e)

if __name__ == '__main__':
    #---下载图片---
    # download_pic('F:/edsimgs/1download_imgs_r')

    #---清洗去重---
    # clean_pic('F:/edsimgs/1download_imgs','F:/edsimgs/2clean_imgs')

    #---百度人脸识别---
    # baiduface('F:/edsimgs/2clean_imgs')

    #---挑选图片&&剪裁图片---
    pick_pic('F:/edsimgs/2clean_imgs','F:/edsimgs/3face_imgs','F:/edsimgs/4cut_imgs')


    pass