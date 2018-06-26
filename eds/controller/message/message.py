
#  author   ：feng
#  time     ：2018/6/22
#  function :留言
import hashlib
from eds.error import MyError
from eds.service.message.messageService import messageService
from flask import Blueprint,request,render_template,redirect,json,session

message_message = Blueprint('message_message', __name__)

@message_message.route('/message/save',methods=['GET','POST'])
def register():
        title = request.form.get('title')
        message = request.form.get('message')
        item={}
        if "account" in session:
            item["user"]= session['account']
        else:
            item["user"] = "匿名"
        item["title"]=title
        item["message"]=message
        messageService.insertMessage(item)

        ajax = {}
        ajax['success'] = True

        ajax['msg'] = ''
        ajax['obj'] = item
        s = json.jsonify(ajax)
        return s