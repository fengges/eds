from flask import Blueprint, render_template, send_file
import io
from eds.service.school.schoolservice import schoolService
from eds.service.search.searchservice import searchService
from urllib import parse
main_test = Blueprint('main_test', __name__)

@main_test.route('/search/test/<param>')
def test(param):
    data={}
    data['keyword']=parse.unquote(param)
    result = searchService.getSearchResult2(data)
    return render_template('/search/search_result4.html',result=result)