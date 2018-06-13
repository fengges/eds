
#  author   ：feng
#  time     ：2018/1/25
#  function : 应用初始化

#       注册蓝图
import jieba.posseg as pseg
import  os
from eds import config
from flask_apscheduler import APScheduler
from flask import Flask,redirect,json,render_template,request
from eds.controller import bp_list
from eds.error import *
from eds.record import *
from eds.task import *
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

#      统计
@app.after_request
def record(response):
    list=r.getCatalog()
    if list[0] in r.map:
        method=r.map[list[0]]
        method(list,response)
    return response



@app.before_request
def filter():
    pass
    # name=r.getName()
    # if name in r.map:
    #     method=r.map[name]
    #     method()

if config.taskOpen:
    scheduler = APScheduler()
    scheduler.add_job(func=task.statistics, id='1', trigger='cron',hour = 17,minute =52 ,second = 00, replace_existing=True)
    scheduler.init_app(app=app)
    scheduler.start()



app.config['SECRET_KEY'] = os.urandom(24)



