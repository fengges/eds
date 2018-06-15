

#  author   ：feng
#  time     ：2018/6/14
#  function : 图表

from flask import Blueprint, request,json,render_template
from eds.service.task.taskservice import taskService

statistics_statistics = Blueprint('statistics_statistics', __name__)

#  接收搜索参数
@statistics_statistics.route('/statistics/statistics')
def index():
    return render_template('/statistics/statistics.html')

@statistics_statistics.route('/statistics/search',methods=['GET','POST'])
def index2():
    params = ['type','startDate','endDate']
    search_params = {}
    t = request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p] = data[p]
        else:
            search_params[p] = None
    result = taskService.getSearch(search_params)
    ajax = {}
    ajax['success'] = True
    ajax['msg'] = ''
    ajax['obj'] = result
    s = json.jsonify(ajax)
    return s
