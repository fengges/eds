
#  author   ：feng
#  time     ：2018/6/5
#  function : 主页面

from flask import Blueprint,render_template

index_index = Blueprint('index_index', __name__)
@index_index.route('/')
@index_index.route('/index/index')
def index():
    return render_template('/index/index.html')