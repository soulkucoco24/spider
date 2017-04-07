# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from spider.items import *
import urllib2
import urllib
import base64
import random


class tghSpider(CrawlSpider):
    name = "tgh"
    allowed_domains = ['taogonghao.com']

    def start_requests(self):
        for i in range(38, 100):
            for j in range(1, 70):
                url = "http://www.taogonghao.com/wemedia.html?page="+str(j)+"&weixin_tags="+str(i)
                yield Request(url, callback=self.parse_main, dont_filter=True, meta={'fTag': i})

    def parse_main(self, response):
        sel = Selector(response)
        trContent = sel.xpath('//tr').extract()
        for tr in trContent:
            newText = "<html><body>" + tr + "</body></html>"
            trSel = Selector(text=newText)
            account = trSel.xpath('//div[@class=\"wx\"]/text()').extract()
            if account:
                item = ArticleItem()
                item['name'] = trSel.xpath('//a/@title').extract()[0]
                item['account'] = account[0]
                item['topRead'] = trSel.xpath('//td/text()').extract()[2]
                item['fans'] = trSel.xpath('//td/text()').extract()[3]
                item['topPrice'] = trSel.xpath('//td/text()').extract()[4]
                item['unTopPrice'] = trSel.xpath('//td/text()').extract()[5]
                item['tag'] = trSel.xpath('//td/text()').extract()[6]
                item['orderRate'] = trSel.xpath('//td/text()').extract()[7].split('%')[0]
                item['credit'] = trSel.xpath('//td/text()').extract()[8]
                item['costRate'] = trSel.xpath('//td/text()').extract()[9]
                item['fTag'] = response.meta['fTag']
                yield item