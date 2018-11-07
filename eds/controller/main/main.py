
#  author   ：feng
#  time     ：2018/1/25
#  function : 主页面

from flask import Blueprint,render_template

main_main = Blueprint('main_main', __name__)


@main_main.route('/main/main')
def index():
    return render_template('/main/index.html')

