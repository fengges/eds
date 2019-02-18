

#  author   ：feng
#  time     ：2018/7/4
#  function : 管理员
import os
import hashlib
from eds.error import *
from flask import Blueprint,render_template,request,session,json,current_app
from eds.controller.sci.service import scis


sic_sci = Blueprint('sic_sci', __name__)

@sic_sci.route('/sci/getQuery',methods=['GET','POST'])
def index():
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = scis.getQuery()
    s=json.jsonify(ajax)
    # 跨域设置
    s.headers['Access-Control-Allow-Origin'] = '*'
    return s

@sic_sci.route('/sci/updataPage',methods=['GET','POST'])
def index2():
    page= request.form.get('page')
    id = request.form.get('id')
    all_page = request.form.get('all_page')
    scis.updataPage(id,page,all_page)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] =None
    s=json.jsonify(ajax)
    # 跨域设置
    s.headers['Access-Control-Allow-Origin'] = '*'
    return s
#      接收搜索参数
@sic_sci.route('/sci/addPaper',methods=['GET','POST'])
def index3():
    t=request.form.get('data')
    data = json.loads(t)
    scis.addPaper(data )
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = None
    s=json.jsonify(ajax)
    # 跨域设置
    s.headers['Access-Control-Allow-Origin'] = '*'
    return s
#      接收搜索参数
@sic_sci.route('/sci/endPaper',methods=['GET','POST'])
def index4():
    id=request.form.get('id')
    scis.endPaper(id)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = None
    s=json.jsonify(ajax)
    # 跨域设置
    s.headers['Access-Control-Allow-Origin'] = '*'
    return s