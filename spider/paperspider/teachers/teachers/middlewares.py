# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class TeachersSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TeachersDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import time


class MyDownloaderMiddleware(HttpProxyMiddleware):
    def __init__(self, ip=''):
        """
            初始化
        """
        # self.db = mysql.Aliyun()
        self.iplist = []

    def process_request(self, request, spider):
        """
        处理request
        """

        # 如果是chinakaoyan的链接，需要加头信息
        import re
        if re.search(r'www\.chinakaoyan\.com', request.url) is not None:
            from spider.paperspider.teachers.teachers.settings import CHINAKAOYAN_HEADERS
            timestamp = str(int(time.time()) * 1000)
            CHINAKAOYAN_HEADERS["Cookie"] = "__utmz = 265731536.1527562520.4.4.utmcsr = baidu|utmccn = (organic)|utmcmd = organic; lang = zh; PHPSESSID = ps7bpdphqd6orpna465oadmkr2; __utmc = 265731536; Hm_lvt_b39c8daefe867a19aec651fe9bb57881 = 1530363672; __utma = 265731536.317589922.1525416185.1530363672.1530368888.7; __utmt = 1; __utmb = 265731536.1.10.1530368888; Hm_lpvt_b39c8daefe867a19aec651fe9bb57881 = %s" % timestamp

            for k, v in CHINAKAOYAN_HEADERS.items():
                request.headers.setdefault(k, v)
