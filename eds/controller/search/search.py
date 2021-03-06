

#  author   ：feng
#  time     ：2018/2/28
#  function : 返回搜索结果

from flask import Blueprint, request,json,render_template
from eds.service.search.searchservice import searchService

main_main = Blueprint('search_search', __name__)

#      接收搜索参数
@main_main.route('/search/search',methods=['GET','POST'])
def index():
    params=['keyword','name','institution','h_index','field','order','page','pPageNum','accurate_search']
    search_params={}
    t=request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p]=data[p]
        else :
            search_params[p]=None
    if search_params['order']=='all':
        search_params['order']=''
    result=searchService.getSearchResult(search_params)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s
#      接收搜索参数
@main_main.route('/search/search3',methods=['GET','POST'])
def index8():
    t=request.form.get('data')
    data = json.loads(t)
    result = searchService.getSearchResult2(data)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s
@main_main.route('/search/searchall')
def index3():
    return render_template('/search/searchreasult.html')
@main_main.route('/search/searchall2')
def index4():
    return render_template('/search/searchreasult2.html')
@main_main.route('/search/searchall3')
def index5():
    return render_template('/search/searchreasult3.html')
@main_main.route('/search/index',methods=['GET','POST'])
def index2():
    params = ['keyword', 'name', 'institution', 'h_index', 'field', 'order', 'page', 'pPageNum', 'accurate_search']
    search_params={}
    t=request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p]=data[p]
        else :
            search_params[p]=None
    result=searchService.getIndexSearchResult(search_params)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s

@main_main.route('/search/hotsearch',methods=['GET','POST'])
def index6():
    params = ['type', 'page', 'pPageNum']
    search_params={}
    t=request.form.get('data')
    data = json.loads(t)
    for p in params:
        if p in data.keys():
            search_params[p]=data[p]
        else :
            search_params[p]=None
    result=searchService.getHotSearch(search_params)
    ajax={}
    ajax['success']=True
    ajax['msg']=''
    ajax['obj'] = result
    s=json.jsonify(ajax)
    return s