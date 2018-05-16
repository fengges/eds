
#  author   ：feng
#  time     ：2018/1/25
#  function : 主页面

from flask import Blueprint,render_template,request,json
from eds.service.needTopic.needTopicservice import needTopicService
needTopic_needTopic = Blueprint('needtopic_needtopic', __name__)

@needTopic_needTopic.route('/needtopic/getTopic',methods=['GET','POST'])
def getTopic():
    t = request.form.get('topic')
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = needTopicService.getNeedTopicByTopic(t)
    s=json.jsonify(ajax)
    return s
