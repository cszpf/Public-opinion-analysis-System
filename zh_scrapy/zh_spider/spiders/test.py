# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/question/275098818']

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    #                    (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    #     'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    # }

    def parse(self, response):
        inspect_response(response, self)
        # then in ipython
        # print(response.xpath('//strong/@title').extract())


'''
in this folder
scrapy runspider test
'''

''' another way

# in cmd 
scrapy shell

# in pyhton
test_url = 'https://www.zhihu.com/question/275098818'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
}

req = scrapy.Request(test_url, headers=headers)
fetch(req)
# fetch a new response from the given request and update all related objects accordingly.

response.xpath('//strong/@title').extract()
'''
