
#  author   ：feng
#  time     ：2018/1/25
#  function : 扫描所有文件，找出所有蓝图并注册
import os,sys

from flask import Blueprint
#------------扫描所有文件----------
bp_file=[]

def eachFile(filepath):
    try :
        pathDir =  os.listdir(filepath)
    except:
        return
    for allDir in pathDir:
        # 忽略__开头的文件和文件夹
        if allDir.startswith('__') :
            continue
        path=filepath+'/'+allDir
        #如果是文件夹
        if not os.path.isfile(path):
            eachFile(path)
        else:
            map=[filepath,allDir]
            bp_file.append(map)

eachFile(sys.path[0]+'/eds/controller')

#------------导入蓝图----------

bp_list=[]
for bp in bp_file:
    dirs=bp[0].replace(sys.path[0]+'/','').replace('/','.')
    if bp[1].find('.txt')>=0:
        continue
    name=bp[1].replace('.py','')
    code="from "+dirs+" import "+name+" as a"
    exec(code)
    list=eval("dir(a)")
    for l in list:
        if l.startswith('__') :
            continue
        temp=eval('a.'+l)
        if type(temp)==Blueprint:
            bp_list.append(temp)

