
#  author   ：feng
#  time     ：2018/6/5
#  function : 主页面
from eds.util.code import code
from eds.util.re_util import  reTest
from eds.service.sms.smsservice import  smsService
from flask import Blueprint,render_template,current_app,session,request,json

code_code = Blueprint('code_code', __name__)

@code_code.route('/code/getCode')
def get_code():
    # 把strs发给前端,或者在后台使用session保存
    strs,code_img = code.create_validate_code()
    response = current_app.make_response(code_img)
    response.headers['Content-Type'] = 'image/gif'
    session['code'] = strs.lower()
    session['codeCheck']=False
    return response
@code_code.route('/code/validate_code',methods=['GET','POST'])
def validate_code():
    ajax = {}
    code = request.form.get('code')
    if 'code' in session:
        if code is not None and code.lower()==session['code']:
            ajax['success'] = True
            session['codeCheck'] = True
            ajax['msg'] = 'right'
        else:
            ajax['success'] = False
            ajax['msg'] = '验证码不正确'
    else:
        ajax['success'] = False
        ajax['msg'] = '没有验证码'
    s = json.jsonify(ajax)
    return s

@code_code.route('/code/sendSms',methods=['GET','POST'])
def sendSms():
    ajax = {}
    phone = request.form.get('phone')
    if not reTest.iscellphone(phone):
        ajax['success'] = False
        ajax['msg'] = '手机输入不正确'
    elif 'codeCheck' not in session or session["codeCheck"]==False:
        ajax['success'] = False
        ajax['msg'] = '请输入验证码'
    else:
        text=code.create_code()
        r=smsService.sendCode(phone,text)
        ajax['success'] = r["success"]
        session['phone_code'] = {"phone": phone, "code": text}
        ajax["obj"] = session['phone_code']
        if r["success"]:
            ajax['msg'] = r["msg"]
        else:
            ajax['msg'] =r["msg"]
            if "second" in r:
                ajax["obj"]["second"]=r["second"]
    s = json.jsonify(ajax)
    return s

