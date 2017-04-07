# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from spider.items import *

class WxSpider(CrawlSpider):
    name = "wx"
    allowed_domains = ['sogou.com','qq.com']
    # start_urls = ["http://weixin.sogou.com/pcindex/pc/pc_0/pc_0.html"]
    def __init__(self):
        urls = []
        for i in range(0, 20):
            urls.append("http://weixin.sogou.com/pcindex/pc/pc_"+ str(i) +"/pc_"+ str(i) +".html")
            for j in range(1,21):
                urls.append("http://weixin.sogou.com/pcindex/pc/pc_"+ str(i) +"/"+ str(j) +".html")
        self.start_urls = urls

    def parse(self, response):
        sel = Selector(response)
        url = sel.xpath('//a[@class=\"wx-news-info\"]/@href').extract()
        summary = sel.xpath('//a[@class=\"wx-news-info\"]/text()').extract()
        cover_pic = sel.xpath('//div[@class=\"wx-img-box\"]/a/img/@src').extract()
        read_des = sel.xpath('//div[@class=\"wx-news-info2\"]/div[@class=\"s-p\"]').extract()
        items = []
        res_url = response.url
        split_url = res_url.split('/')
        tips = split_url[5]
        for i in range(0, 20):
            item = WxItem()
            item['summary'] = summary[i]
            item['cover_pic'] = cover_pic[i]
            item['url'] = url[i]
            read_split = read_des[i].split(u"\u9605\u8bfb")
            read_detail = read_split[1].split("<bb")
            read = read_detail[0].strip()
            item['read'] = read
            item['tips'] = tips
            items.append(item)
        for item in items:
            yield scrapy.Request(item['url'], callback=self.parse_content, meta={'item':item})

    def parse_content(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['title'] = sel.xpath('//h2/text()').extract()[0].strip()
        item['content'] = sel.xpath('//div[@id=\"js_content\"]').extract()[0]
        item['source_url'] = sel.xpath('//div[@id=\"js_sg_bar\"]/a[@class=\"media_tool_meta meta_primary\"]/@href').extract()[0]
        item['account'] = sel.xpath('//a[@id=\"post-user\"]/text()').extract()[0]
        item['author'] = sel.xpath('//em[@class=\"rich_media_meta rich_media_meta_text\"][2]/text()').extract()[0]
        item['publish_date'] = sel.xpath('//em[@id=\"post-date\"]/text()').extract()[0]
        return item