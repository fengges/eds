
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

    return render_template('/main/expert.html', info_dict=infoEty[0])

@main_expert.route('/main/propic/<id>')
def show_pic(id):
    img= expertService.get_pic(id)
    return send_file(io.BytesIO(img.read()),
                     attachment_filename=str(id)+'.jpg',
                     mimetype='image/jpg')

@main_expert.route('/getdrawdata', methods=['POST'])
def get_draw_data():
    id=request.form.get('id')
    radarEty = expertService.get_radar(id)
    themeEty = expertService.get_theme(id)
    egoEty = expertService.get_ego(id)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] ={}
    ajax['obj']['radar']=radarEty
    ajax['obj']['theme'] = themeEty
    ajax['obj']['ego'] = egoEty
    return json.jsonify(ajax)


