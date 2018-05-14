
import re,io
from flask import Blueprint, render_template, request,json,Response,send_file
from eds.service.profile.profileservice import profileService

main_profile = Blueprint('main_profile', __name__)


@main_profile.route('/main/profile/<id>')
def show_profile(id):
    infoEty = profileService.get_info(id)
    try:
        infoEty[0]['email'] = infoEty[0]['email'].split(";")[0]
    except:
        infoEty[0]['email'] = ''
    if not infoEty:
        return render_template('/main/notfound.html')
    if not infoEty[0]["homepage"] and not re.search(r'^http', infoEty[0]["homepage"]):
        infoEty[0]["homepage"] = "http://" + infoEty[0]["homepage"]
    return render_template('/main/profile.html', info_dict=infoEty[0])

@main_profile.route('/main/propic/<id>')
def show_pic(id):
    img= profileService.get_pic(id)
    return send_file(io.BytesIO(img.read()),
                     attachment_filename=str(id)+'.jpg',
                     mimetype='image/jpg')

@main_profile.route('/getdrawdata', methods=['POST'])
def get_draw_data():
    id=request.form.get('id')
    radarEty = profileService.get_radar(id)
    themeEty = profileService.get_theme(id)
    egoEty = profileService.get_ego(id)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] ={}
    ajax['obj']['radar']=radarEty
    ajax['obj']['theme'] = themeEty
    ajax['obj']['ego'] = egoEty
    return json.jsonify(ajax)


