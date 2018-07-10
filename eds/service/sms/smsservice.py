
import time
from eds.util.sms_send import send
from flask import json
from eds.dao.task.taskdao import taskDao
class SmsService:
    def __init__(self):
        self.num=3
        self.second=60

    def sendCode(self,phone,code):
        print("send: "+str(phone)+"-- code:"+str(code))
        nums,second=self.getNumAndTime(phone)
        if nums>=self.second:
            return {"success": False, "msg": "当天发送短信次数过多", "code": code, "phone": phone}
        elif nums!=0 and second<self.second:
            return {"success": False, "msg": "发送太频繁", "code": code, "phone": phone,"second":self.second-second}
        item={}
        item["phone"]=phone
        item["params"] = {"code":code}
        item["code"]="SMS_139227084"
        r=send(item)
        if r["Code"]=="OK":
            return {"success":True,"msg":"","code":code,"phone":phone}
        else:
            return {"success":False,"msg":r["Message"],"code":code,"phone":phone}
    def seletSmsByPhone(self,phone):
        param={"phone":phone,"type":"手机验证码"}
        reslut=taskDao.selectSmsByPhone(param)
        return reslut

    def getNumAndTime(self,phone):
        r=self.seletSmsByPhone(phone)
        if len(r)==0:
            return 0,0
        else:
            now = time.time()
            timeNum=time.mktime(r[0]["time"].timetuple())
            return len(r),now-timeNum

smsService = SmsService()
