# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy.crawler import CrawlerProcess


class QaSpider(scrapy.Spider):
    name = 'qa_spider'
    allowed_domains = ['zhihu.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                       (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    }

    def start_requests(self):
        with open('../data/question_urls.txt', 'r') as qa_files:
            urls = qa_files.readlines()
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        resp = response.text
        jo = json.loads(resp)
        is_end = bool(jo.get('paging').get('is_end'))
        ja_data = jo.get('data')

        for jo_answer_item in ja_data:
            content = jo_answer_item.get('content')
            question_id = str(jo_answer_item.get('question').get('id'))
            question_title = jo_answer_item.get('question').get('title')
            question_title = re.sub(r'\W', '', question_title)  # '\W' in re for not word character
            file_url = '../data/[' + question_id + ']' + question_title + '.txt'
            with open(file_url, 'a', encoding='utf-8') as out_file:
                out_file.write(content + '\n\n')

        if not is_end:
            next_page_url = jo.get('paging').get('next')
            yield scrapy.Request(url=next_page_url, callback=self.parse, headers=self.headers)
        else:
            pass


process = CrawlerProcess()
process.crawl(QaSpider)
process.start()  # the script will block here until the crawling is finished
