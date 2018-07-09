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

    def getMessage(self,params):
        sql_num = 'SELECT count(*) as num FROM `messages` a LEFT JOIN user b on  a.user=b.account'
        sql = 'SELECT a.*,b.account,b.username FROM `messages` a LEFT JOIN user b on  a.user=b.account order by time desc limit %s,%s'
        param=(params['pPageNum']*(params['page']-1),params['pPageNum'])
        s=dbs.getDics(sql,param)
        n = dbs.getDics(sql_num)
        return {"result":s,"num":n[0]["num"]}
messageDao=MessageDao()