#  author   ：feng
#  time     ：2018/6/22
#  function ：留言
from eds.dao.base import dbs


class MessageDao:
    def insertMessage(self,params):
        item={}
        item["table"]="messages"
        item["params"]=params
        dbs.insertItem(item)
messageDao=MessageDao()