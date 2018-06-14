# -*- coding: utf-8 -*-
#---本地存放paper数据的表---
DB_SETTING = {
   'host':'localhost',
   'port':3306,
   'user':'root',
   'passwd':'Cr648546845',
   'db':'eds',
   'charset':'utf8'
}

#---爬取配置---
CRAWL_SETTING = {
   'num':'1',
   'total':'3'
}


#---百度学术检索页面限制---
MAX_PAGE = 20

#---解析优先级设置---
ABSTRACT_PRIORITY = {
   '3':'维普',
   '2':'万方',
   '1':'知网'
}

#---维普请求头---
VIP_HEADERS = {
   "Host": "www.cqvip.com",
   "Accept": "text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
   "Cookie": "cqvip_usersessionid=4f305b05-eae4-4a68-914e-1bc8be727a40; PacketUser:AutoLogin=1; Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313=1527150741; __utma=164835757.1722227508.1527150743.1527150743.1527150743.1; __utmz=164835757.1527150743.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ASP.NET_SessionId=b4inqo1rferwyw4wdyleipbh; Hm_lpvt_69fff6aaf37627a0e2ac81d849c2d313=1527150741; __utmb=164835757.1.10.1527150743; __utmc=164835757; __utmt=1; __utmt_vip2=1",
   "Connection": "keep-alive",
   "Upgrade-Insecure-Requests":"1",
   "Referer":"http://www.cqvip.com/main/search.aspx?k=%E4%BC%A0%E6%84%9F%E5%99%A8%E5%BC%B9%E6%80%A7%E5%85%83%E4%BB%B6%E7%9A%84%E7%BB%93%E6%9E%84%E4%BC%98%E5%8C%96%E8%AE%BE%E8%AE%A1"
}




# Scrapy settings for baiduxueshu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baiduxueshu'

SPIDER_MODULES = ['baiduxueshu.spiders']
NEWSPIDER_MODULE = 'baiduxueshu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baiduxueshu (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'baiduxueshu.middlewares.BaiduxueshuSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'baiduxueshu.middlewares.MyCustomDownloaderMiddleware': 543,
   'baiduxueshu.middlewares.IPPOOLS': 125,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'baiduxueshu.pipelines.BaiduxueshuPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
