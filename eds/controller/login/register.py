
#  author   ：feng
#  time     ：2018/1/25
#  function : 注册测试
import hashlib
from eds.error import MyError
from eds.service.login.loginservice import userService
from flask import Blueprint,request,render_template,redirect,json

login_register = Blueprint('login_register', __name__)

@login_register.route('/login/register',methods=['GET','POST'])
def register():
        account = request.form.get('account')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #-----账户唯一-----
        param = (account,)
        user = userService.getUser(param)
        if user:
            raise  MyError(604)
        else:
            #---密码要一样---
            if password1 != password2:
                raise MyError(605)
            else:

                m = hashlib.md5()
                m.update(bytes(password1, encoding = "utf8"))
                password1 = m.hexdigest()
                param = (account,username,password1)
                userService.addUser(param)
                ajax = {}
                ajax['success'] = True
                ajax['msg'] = ''
                s = json.jsonify(ajax)
                return s