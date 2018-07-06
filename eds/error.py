#  author   ：feng
#  time     ：2018/1/25
#  function : 错误类型定义

# 异常描述
def error_0(self=None):
    print('0错误')
def error_600(self=None):
    print('600错误')
ErrorCode={'0':{'method':error_0,"description":"发生了某些错误"},
           '600':{'method':error_600,"description":"发生了某些错误"},
           '601': {"description": "账户参数个数不对"},
           '602': {"description": "未设置账户名"},
           '603': {"description": "未设置密码"},
           '604': {"description": "该用户已经存在"},
           '605': {"description": "两次密码不一致"},
           '606': {"description": "账号密码不一致"},

           '701': {"description": "领域个数应大于等于3"},
           '702': {"description": "领域个数应小于等于3"},
           }

class MyError(Exception):
    """自定义错误类"""
    def __init__(self,code=None):
        if code is not None :
            code=str(code)
            self.code=code
            if code in ErrorCode.keys():
                self.description=ErrorCode[code]['description']
                if 'method' in ErrorCode[code].keys():
                    self.method=ErrorCode[code]['method']
    def __str__(self):
        s='code:%r\ndescription:%r'%(self.code,self.description)
        return s

    code=0
    description='发生了某些错误'
    method=None

