
#  author   ：feng
#  time     ：2018/6/5
#  function : 主页面
from eds.service.field.fieldService import fieldService
from eds.service.index.indexservice import indexService
from flask import Blueprint,render_template

index_index = Blueprint('index_index', __name__)
@index_index.route('/')
@index_index.route('/index/index')
def index():

    infoEty985 = indexService.get_school_info(985)
    infoEty211 = indexService.get_school_info(-211)
    fieldTeacher=fieldService.getFieldTeacher()
    return render_template('/index/index.html', info_985_dict=infoEty985, info_211_dict=infoEty211,fieldTeacher=fieldTeacher)
