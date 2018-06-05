
#  author   ：feng
#  time     ：2018/6/5
#  function : 主页面

from flask import Blueprint,render_template

main_main = Blueprint('index_index', __name__)

@main_main.route('/index/index')
def index():
    return render_template('/index/index.html')