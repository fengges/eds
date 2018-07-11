
import re,io
import hashlib
from flask import Blueprint, render_template, session,request,json
from eds.service.usercenter.usercenterservice import userService

usercenter_usercenter = Blueprint('usercenter_usercenter', __name__)


@usercenter_usercenter.route('/usercenter')
def show_expert():
    if session.get("account"):
        login_records = userService.get_login_record(session['account'])
        return render_template('/main/userpage.html',records = login_records)
    else:return render_template('/login/login.html')

@usercenter_usercenter.route('/usercenter/repassword',methods=['GET','POST'])
def rePassword():
    account = request.form.get('account')
    password = request.form.get('password')
    m = hashlib.md5()
    m.update(bytes(password, encoding="utf8"))
    password = m.hexdigest()
    userService.re_password((password, account))

    ajax = {}
    ajax['success'] = True
    ajax['msg'] = ''
    ajax["obj"] = {"account": account}
    s = json.jsonify(ajax)
    return s







