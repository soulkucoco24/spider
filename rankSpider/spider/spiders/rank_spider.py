# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from spider.items import *
from scrapy.http import Request, FormRequest

class RankSpider(CrawlSpider):
    name = "rank"
    allowed_domains = ['wxb.com']

    headers = {
        'Host': 'top.wxb.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }

    def start_requests(self):
        url = 'http://top.wxb.com/account/'
        return [Request(url, callback=self.parse_main, headers=self.headers, dont_filter=True)]

    def parse_main(self, response):
        sel = Selector(response)
        tips = []
        accounts = []
        sevenReads = []
        item = RankItem()
        for i in range(0,25):
            tips.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/h3/a/text()').extract())
            accounts.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/ul/li/div[@class=\"normal clearfix\"]/a/text()').extract())
            sevenReads.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/ul/li/div[@class=\"normal clearfix\"]/span[@class=\"read-num\"]/text()').extract())

        item['tips'] = tips
        item['accounts'] = accounts
        item['sevenReads'] = sevenReads
        return item

