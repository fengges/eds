# -*- coding: utf-8 -*-
#---本地存放paper数据的表---
DB_SETTING = {
   'host':'localhost',
   'port':3306,
   'user':'root',
   'passwd':'123456',
   'db':'schoollink',
   'charset':'utf8'
}
name="zhang"
#---爬取配置---
CRAWL_SETTING = {
   'num':'1',
   'total':'3'
}
ENGLISH_PAPER = {
   'zhang':0,
   'li':1,
   'chen':2
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

RETRY_ENABLED=False


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
cookie_str='_abck=E671906EA982528E2C74D3911431ADB2170F01372250000075A3DA5B7CF45303~0~jGNzAIaLv2e0Om8g/s9gzonk/AQ5XllEq7wITUD1zdk=~-1~-1; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; bm_sz=AAD94558DC0F884AA224619A9AB9E1A3~QAAQpdocuLAmi+NmAQAAFj7V58uL54w0BODWhRyzta54eNYCvCXcR/6+Zb8nL2/+KnyjL5IadPplqrtqZm4Z0IPELcji6lqTyTGj3dnjWGSj+f+lCP3EOP9iGg0hF1cNQCpKKgnf17hvcQGFsZ0mxjt6QqkoPxATOv8eNQ98JKbuQtV+gEcp6yxDzqs3vh4wumuPqycQTQ==; SID="5CGhqqQOMCZRiulglrg"; CUSTOMER="Southeast University"; E_GROUP_NAME="Southeast University"; ak_bmsc=2B52C8A1BF88694555F38F10778E8773B81CDAA51D3A0000785AE15B6C848271~pliNLfzcjfFORI6RnwwXyGouW5JYYciGAhJAaR2FPZwu7NYZZWUBgxfzan/Vx9EEPE11KGQrR2goCWxSCIJxfmsbQ+tuNyPi9vSWXdEeuM1XU3QFZk/jkPwEMW0xCJWlaanvDQCV+/i/7gWwonMhBA+edw9PaFPjPZ/THGVoT3cPlqx2eGCEnbeAgwV5w/J1rpjztnByzB4dvXJCoGUaqoXdfQU87hVHsStnBtaSmcsrDcRW552wVLr3cLuEEs3tFp; _sp_ses.630e=*; JSESSIONID=20EB5D9BB160078D68A6B2A0BBE72A1C; bm_sv=0B3AF8F6669F7E4D0C809E7CDFB3CE3D~eocV/NNRBqhcrnPqikNYu9AvxwhjLlg9l0e2efrMrFMZJuvi5B6FXqi+oZofgdNYo4I1tJj7mBJM5AOXaSiU74cSSgatHHxwFvPFGtQO0WBXWqm6/wINKRavYfUlskKczvLWuu5MndclNBvNsg/qsPx8r0G4ouMpqKKsK4+azgY=; _sp_id.630e=5443240d-4ce8-44c2-bae7-fab328f92256.1541487809.2.1541496652.1541490566.f2471a62-f31b-4321-bb94-8798815b81b1'
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
URLLENGTH_LIMIT = 20000
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
