# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from spider.items import *
from scrapy.http import Request, FormRequest

class ArticleSpider(CrawlSpider):
    name = "article"
    allowed_domains = ['wxb.com', 'qq.com']

    headers = {
        'Host': 'top.wxb.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }

    def start_requests(self):
        url = 'http://top.wxb.com/'
        return [Request(url, callback=self.parse_main, headers=self.headers, dont_filter=True)]

    def parse_main(self, response):
        sel = Selector(response)
        tips = []
        titles = []
        reads = []
        urls = []
        summarys = []
        items = []
        for i in range(0,25):
            tips.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/h3/a/text()').extract())
            titles.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/ul/li/div[@class=\"normal clearfix\"]/a/text()').extract())
            reads.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/ul/li/div[@class=\"normal clearfix\"]/span[@class=\"read-num\"]/text()').extract())
            urls.append(sel.xpath('//div[@id=\"part'+ str(i) +'\"]/ul/li/div[@class=\"normal clearfix\"]/a/@href').extract())
            summarys.append(sel.xpath('//div[@class=\"detail clearfix\"]/div/text()').extract())
            for j in range(0, 10):
                item = ArticleItem()
                item['tips'] = tips[i][0]
                item['title'] = titles[i][j]
                item['read'] = reads[i][j]
                item['url'] = urls[i][j]
                item['summary'] = summarys[i][j]
                item['rank'] = j+1
                items.append(item)

        for item in items:
            yield scrapy.Request(item['url'], callback=self.parse_content, meta={'item': item})


    def parse_content(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['content'] = sel.xpath('//div[@id=\"js_content\"]').extract()[0]
        item['account'] = sel.xpath('//a[@id=\"post-user\"]/text()').extract()[0]
        if sel.xpath('//em[@class=\"rich_media_meta rich_media_meta_text\"][2]/text()').extract():
            item['author'] = sel.xpath('//em[@class=\"rich_media_meta rich_media_meta_text\"][2]/text()').extract()[0]
        else:
            item['author'] = ''
        if sel.xpath('//em[@id=\"post-date\"]/text()').extract():
            item['publish_date'] = sel.xpath('//em[@id=\"post-date\"]/text()').extract()[0]
        else:
            item['publish_date'] = ''
        item['source_url'] = ''

        return item
