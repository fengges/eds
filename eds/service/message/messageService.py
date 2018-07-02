
#  author   ：feng
#  time     ：2018/6/22
#  function : 留言


from eds.dao.message.messageDao import  messageDao


class MessageService:

    def insertMessage(self,item):
        return messageDao.insertMessage(item)

messageService=MessageService()

