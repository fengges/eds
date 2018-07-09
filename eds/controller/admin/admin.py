

#  author   ：feng
#  time     ：2018/7/4
#  function : 管理员
import os
import hashlib
from eds.error import *
from flask import Blueprint,render_template,request,session,json,current_app
from eds.service.admin.adminservice import adminService
from eds.service.login.loginservice import userService
from eds.service.message.messageService import messageService
from eds.service.field.fieldService import fieldService

admin_admin = Blueprint('admin_admin', __name__)

@admin_admin.route('/admin/admin')
def index():
    return render_template('/admin/admin.html')

@admin_admin.route('/admin/user')
def index2():
    return render_template('/admin/user.html')

#      接收搜索参数
@admin_admin.route('/admin/getUser',methods=['GET','POST'])
def index3():
    params=['field','order','page','pPageNum']
    search_params={}
    t=request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p]=data[p]
        else :
            search_params[p]=None
    result=userService.getUsers(search_params)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s


@admin_admin.route('/admin/message')
def index4():
    return render_template('/admin/message.html')

#      接收搜索参数
@admin_admin.route('/admin/getMessage',methods=['GET','POST'])
def index5():
    params=['field','order','page','pPageNum']
    search_params={}
    t=request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p]=data[p]
        else :
            search_params[p]=None
    result=messageService.getMessage(search_params)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s


@admin_admin.route('/admin/field')
def index6():
    return render_template('/admin/field.html')

#      接收搜索参数
@admin_admin.route('/admin/getField',methods=['GET','POST'])
def index7():
    result=fieldService.getField()
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s

#      接收搜索参数
@admin_admin.route('/admin/getTeacherByField',methods=['GET','POST'])
def index8():
    params=['field','order','page','pPageNum']
    search_params={}
    t=request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p]=data[p]
        else :
            search_params[p]=None
    result=fieldService.getTeacgerByXueKe(search_params)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s

#      接收搜索参数
@admin_admin.route('/admin/setField',methods=['GET','POST'])
def index9():
    t=request.form.get('data')
    data = json.loads(t)
    fieldService.setField(data)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    s=json.jsonify(ajax)
    return s


@admin_admin.route('/admin/changeTeacherField',methods=['GET','POST'])
def index10():
    t=request.form.get('data')
    data = json.loads(t)
    fieldService.changeTeacherField(data)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    s=json.jsonify(ajax)
    return s
