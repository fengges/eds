

#  author   ：feng
#  time     ：2018/6/6
#  function : 主页面
import os
import hashlib
from flask import Blueprint,render_template,request,session,json,current_app
from eds.service.login.loginservice import userService
from eds.error import *
login_login = Blueprint('login_login', __name__)

@login_login.route('/login/gologin')
def index():
    return render_template('/login/login.html')

@login_login.route('/login/login',methods=['GET','POST'])
def login():
        account = request.form.get('account')
        password = request.form.get('password')
        m = hashlib.md5()
        m.update(bytes(password, encoding="utf8"))
        password = m.hexdigest()
        param=(account,)
        user = userService.getUser(param)
        if user and user['password']==password:
            session['username'] = user['username']
            session['account'] = user['account']
            #---cookie时间---
            session.permanent = True
            ajax = {}
            ajax['success'] = True
            ajax['msg'] = ''
            s = json.jsonify(ajax)
            return s
        else:
            raise  MyError(606)

@login_login.route('/login/logout/')
def logout():
    session.clear()
    ajax = {}
    ajax['success'] = True
    ajax['msg'] = ''
    s = json.jsonify(ajax)
    return s

