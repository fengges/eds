
#  author   ：feng
#  time     ：2018/6/22
#  function : 留言

import time
from eds.dao.message.messageDao import  messageDao


class MessageService:

    def insertMessage(self,item):
        item["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return messageDao.insertMessage(item)
    def getMessage(self,params):
        result=messageDao.getMessage(params)
        for r in result["result"]:
            if r["time"]:
                r["time"]=r["time"].strftime("%Y-%m-%d %H:%M:%S")
        return result
messageService=MessageService()

