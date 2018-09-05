from flask import Blueprint, render_template, send_file
import io
from eds.service.school.schoolservice import schoolService

main_test = Blueprint('main_test', __name__)


@main_test.route('/test')
def test():
    return render_template('/search/search_result4.html')
