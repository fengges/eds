
#  author   ：feng
#  time     ：2018/1/25
#  function : 应用初始化

#       注册蓝图
import jieba.posseg as pseg
import  os
from eds import config
from flask import Flask,redirect,json,render_template
from eds.controller import bp_list
from eds.error import *

app = Flask(__name__)

app.config.from_object(config)
for bp in bp_list:
    app.register_blueprint(bp)

#      捕获全局异常
@app.errorhandler(MyError)
def error(error):
    f=error.method
    if f:
        f()
    ajax = {}
    ajax['success'] = False
    ajax['msg'] = error.description
    return json.jsonify(ajax)

@app.route('/index.html')
def index():
    return redirect('/static/index.html')


#      设置上下文
@app.context_processor
def my_context_processor():
    return {}

app.config['SECRET_KEY'] = os.urandom(24)



