
import re,io
from flask import Blueprint, render_template, request,json,Response,send_file
from eds.service.platform.platformservice import platformService

main_platform = Blueprint('main_platform', __name__)


@main_platform.route('/main/platform/<id>')
def show_platform(id):
    baseinfo,infolist = platformService.get_info(id)

    return render_template('/main/platform.html',baseinfo = baseinfo,infolist = infolist)

