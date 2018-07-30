from flask import Blueprint, render_template, send_file
import io
from eds.service.school.schoolservice import schoolService

main_school = Blueprint('main_school', __name__)


@main_school.route('/main/schpic/<param>')
def show_pic(param):
    img = schoolService.get_pic(param)
    return send_file(io.BytesIO(img.read()),
                     attachment_filename=str(param)+'.jpg',
                     mimetype='image/jpg')


@main_school.route('/main/school/<param>')
def show_school(param):
    info = schoolService.get_info(param)
    if info is None:
        return render_template('/main/notfound.html')
    discipline = schoolService.get_discipline(param)
    return render_template('/main/schoolpage.html', info=info, discipline=discipline)
