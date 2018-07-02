
import re,io
from flask import Blueprint, render_template, request,json,Response,send_file
from eds.service.expert.expertservice import expertService

main_expert = Blueprint('main_expert', __name__)


@main_expert.route('/main/expert/<id>')
def show_expert(id):
    infoEty = expertService.get_info(id)
    try:
        infoEty[0]['email'] = infoEty[0]['email'].split(";")[0]
    except:
        infoEty[0]['email'] = ''
    if not infoEty:
        return render_template('/main/notfound.html')
    if not infoEty[0]["homepage"] and not re.search(r'^http', infoEty[0]["homepage"]):
        infoEty[0]["homepage"] = "http://" + infoEty[0]["homepage"]

    paperEty = expertService.get_paper(id)
    return render_template('/main/expert.html', info_dict=infoEty[0] ,paperlist = paperEty)


@main_expert.route('/main/propic/<id>')
def show_pic(id):
    img= expertService.get_pic(id)
    return send_file(io.BytesIO(img.read()),
                     attachment_filename=str(id)+'.jpg',
                     mimetype='image/jpg')

@main_expert.route('/getdrawdata', methods=['POST'])
def get_draw_data():
    id=request.form.get('id')

    # #河流图数据获取
    # themeEty = expertService.get_theme(id)
    # ajax={}
    # ajax['success']=True
    # ajax['msg']=''
    # ajax['obj'] ={}
    # ajax['obj']['theme'] = themeEty

    # 单轴图数据获取
    themeSingleaxis = expertService.get_single_axis(id)
    ajax = {}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] ={}
    ajax['obj']['theme'] = themeSingleaxis
    return json.jsonify(ajax)


