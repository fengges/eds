# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

class BaiduxueshuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # Scrapy使用此方法来创建您的爬虫
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider  针对通过蜘蛛的每个响应调用
        # middleware and into the spider. 中间件和蜘蛛。 

        # Should return None or raise an exception. 应该返回None或引发异常。

        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after  之后，从蜘蛛返回的结果中调用
        # it has processed the response.            它已处理回复。

        # Must return an iterable of Request, dict or Item objects.     必须返回Request，dict或Item对象的迭代。
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method     调用spider或process_spider_input（）方法时
        # (from other spider middleware) raises an exception.   （来自其他蜘蛛中间件）引发异常。

        # Should return either None or an iterable of Response, dict        应该返回None或迭代响应，字典或项目对象。
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works   调用蜘蛛的启动请求，并工作
        # similarly to the process_spider_output() method, except   与process_spider_output（）方法类似，除外
        # that it doesn’t have a response associated.   它没有关联的响应。

        # Must return only requests (not items).    只能返回请求（不是项目）。
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import requests
import time
import random
import threading
class IPPOOLS(HttpProxyMiddleware):

    def __init__(self,ip=''):
        '''初始化'''
        # self.db = mysql.Aliyun()
        self.lock = threading.Lock()
        self.iplist = []

    def get_ip_from_web(self):
        """
        去代理网站接口请求新的iplist
        :return: iplist  例: [{'ip': '171.11.137.159:14330', 'success': 0, 'failure': 0}, {'ip': '112.113.154.145:17478', 'success': 0, 'failure': 0}]
        """
        time.sleep(random.randint(2,10))
        url = "http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="
        data = requests.get(url).text
        iplist = data.split('\r\n')
        if iplist[0].find('false')!=-1:
            time.sleep(random.randint(2,10))
            print('时间ip不够用')
            url = "http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="
            data = requests.get(url).text
            iplist = data.split('\r\n')

        result = []
        for ip in iplist:
            result.append({'ip': ip, 'success': 0, 'failure': 0})

        print('从网站获取list')
        return result

        # tempresult = [{'ip': '171.11.137.159:14330', 'success': 0, 'failure': 0}, {'ip': '112.113.154.145:17478', 'success': 0, 'failure': 0}, {'ip': '2.113.154.145:17478', 'success': 0, 'failure': 0}, {'ip': '3.113.154.145:17478', 'success': 0, 'failure': 0}]
        # return tempresult

    def getIP(self):
        """
        从 iplist中获取一个ip，如果iplist为空，则去代理网站接口请求新的iplist
        :return: ip  例: {'ip': '171.11.137.159:14330', 'success': 20, 'failure': 2}
        """
        if len(self.iplist)>0:
            iplist = sorted(self.iplist, key=lambda k: k["success"], reverse=True)
            return iplist[-1]['ip']
        else:
            self.iplist = self.get_ip_from_web()
            iplist = sorted(self.iplist, key=lambda k: k["success"], reverse=True)
            return iplist[-1]['ip']

    def process_request(self, request, spider):
        """
        处理request，即设置request代理
        """
        self.lock.acquire()
        ip = self.getIP()
        self.lock.release()
        request.meta["proxy"] = "http://" + ip

    def process_response(self, request, response, spider):
        """
        检查response.status,
        如果不是200，则failure+1，若failure>3，则删除这条ip
        如果是200，则success+1
        """
        if response.status == 407 or response.status == 502 or response.status == 503:

            ip = request.meta["proxy"][7:]
            x = self.get_list_index(ip,self.iplist)

            if self.iplist[x]['failure']>3:
                del self.iplist[x]
            else:self.iplist[x]['failure']+=1
            return request
        elif response.status == 200:
            ip = request.meta["proxy"][7:]
            x = self.get_list_index(ip, self.iplist)
            self.iplist[x]['success'] += 1

            return response
        elif response.status==403:
            return response
        else:
            return response

    def process_exception(self, request, exception, spider):
        """
        处理由于使用代理导致的连接异常
        """
        print(exception)

        if "exception_num" in request.meta.keys():
            if request.meta["exception_num"]>2:
                return None
        else:request.meta["exception_num"] = 1

        ip = request.meta["proxy"][7:]
        x = self.get_list_index(ip, self.iplist)

        if self.iplist[x]['failure'] > 3:
            del self.iplist[x]
        else:
            self.iplist[x]['failure'] += 1
        return request

    def get_list_index(self,ip, iplist):
        """
        获取list中对应ip的索引
        """
        iplist = sorted(iplist, key=lambda k: k["success"], reverse=True)
        x = -1
        for i in range(len(iplist)):
            if iplist[i]['ip'] == ip:
                x = i
                break
        return x


