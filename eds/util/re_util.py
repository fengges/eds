

import re


class ReTest():

    def __init__(self):
        self.phone = re.compile(r'[1][^1269]\d{9}')
        self.mail = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')

    def iscellphone(self, number):
        res = self.phone.match(number)
        if res:
            return True
        else:
            return False

    def ismail(self, str):
        res = self.mail.match(str)
        if res:
            return True
        else:
            return False

reTest=ReTest()