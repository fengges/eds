from flask import request,session,json
import time
from eds.dao.base import dbs

class Authority:
    def __init__(self):
        self.map={
            "login":self.login,

        }
        self.catalog={
            "search":{"search":"搜索全部","index":"搜索前5"},

        }


    def school(self,list,response):

        if list[1] in self.catalog[list[0]]:
            data = self.getData(response)
            item = self.getItem(data)
            item["type"] = self.catalog[list[0]][list[1]]
            item["value"]=list[2]
            item["other"] = str({})
            records={"table":"records","params":item}
            dbs.insertItem(records)
    def expert(self,list,response):
        if list[1] in self.catalog[list[0]]:
            data = self.getData(response)
            item = self.getItem(data)
            item["type"] = self.catalog[list[0]][list[1]]
            item["value"] = list[2]
            item["other"] = str({})
            records={"table":"records","params":item}
            dbs.insertItem(records)

r=Record()



