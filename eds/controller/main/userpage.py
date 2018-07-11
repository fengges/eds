
import re,io
from flask import Blueprint, render_template, request,json,Response,send_file
from eds.service.user.userservice import userService

main_user = Blueprint('main_user', __name__)


@main_user.route('/main/usercenter')
def show_expert():
    return render_template('/main/userpage.html')




