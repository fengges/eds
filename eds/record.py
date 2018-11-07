from flask import request,session,json
import time
from eds.dao.base import dbs

class Record:
    def __init__(self):
        self.map={
            "login":self.login,
            "search":self.search,
            "main":self.expert,
            "message": self.message,
            "code":self.code,

        }
        self.catalog={

            "search":{"search":"搜索全部","index":"搜索前5","search3":"搜索全部"},
            "login":{"login":"登陆","register":"注册","phonelogin":"登陆"},
            "main":{"expert":"专家","school":"学校"},
            "message":{"save": "留言"},
            "code": {"sendSms": "手机验证码"}
        }
    def code(self, list, response):
        if list[1] in self.catalog[list[0]]:
            data = self.getData(response)
            item = self.getItem(data)
            item["type"] = self.catalog[list[0]][list[1]]
            true=True
            false=False
            obj=eval(response.data.decode())['obj']
            if 'phone' in obj:
                item["value"]=obj["phone"]
            else:
                item["value"] =""
            item["other"] = str({})
            records = {"table": "records", "params": item}
            dbs.insertItem(records)
    def message(self, list, response):
        if list[1] in self.catalog[list[0]]:
            data = self.getData(response)
            item = self.getItem(data)
            item["type"] = self.catalog[list[0]][list[1]]
            true=True
            item["value"] =eval(response.data.decode())['obj']['user']
            item["other"] = str({})
            records = {"table": "records", "params": item}
            dbs.insertItem(records)
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
    def login(self,list,response):
        if list[1] in self.catalog[list[0]]:
            data = self.getData(response)
            item = self.getItem(data)
            item["type"] = self.catalog[list[0]][list[1]]
            obj=json.loads(response.data.decode())
            if "msg" in obj:
                if obj["msg"]=="登陆" or "注册"==obj["msg"]:
                    item["type"]=obj["msg"]
            item["value"] = obj["obj"]['account']
            item["other"] = str({})
            records={"table":"records","params":item}
            dbs.insertItem(records)
    def search(self,list,response):
        if list[1] in self.catalog[list[0]]:
            data = self.getData(response)
            item=self.getItem(data)
            item["type"] = self.catalog[list[0]][list[1]]
            item["value"] = json.loads(request.form['data'])['keyword']
            item["other"] = str({})
            records={"table":"records","params":item}
            dbs.insertItem(records)

    def getCatalog(self):
        url=request.url.replace(request.url_root,"")
        index=url.find('?')
        if index>=0:
            return url[:index].split("/")
        else:
            return url.split("/")
    def getData(self,response):
        temp=response.response[0]
        if type(temp)==str:
            try:
                return {"status_code":response._status_code,"resp":json.loads(temp),"type":"dict"}
            except:
                return {"status_code": response._status_code, "type": "html"}
        else:
            return {"status_code": response._status_code, "type": "html"}
    def getItem(self,data):
        item = {}
        item["ip"]=request.remote_addr
        item["agent"]=request.headers.environ['HTTP_USER_AGENT']
        if data["type"]=="dict":
            item["success"] = data["resp"]["success"]
            item["info"]=data["resp"]["msg"]
        else:
            item["success"] = data["status_code"]==200
            item["info"] = data["status_code"]
        dic={}
        for k in request.form:
            dic[k]=request.form[k]
        item["form"] = str(dic)
        item["url"] = request.url
        if  'username' in session:
            item["user"] = session['account']
        else:
            item["user"] ="未登陆人员"
        item["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return item
r=Record()



