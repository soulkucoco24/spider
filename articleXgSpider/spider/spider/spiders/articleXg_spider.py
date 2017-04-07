# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
import urllib2
import urllib
from spider.items import *
import MySQLdb
import time
import datetime
import re

dbuser = 'root'
dbpass = 'qwerasdf'
dbname = 'wx_helper'
dbhost = '127.0.0.1'
dbport = '3306'

class articleXgSpider(CrawlSpider):
    name = "articleXg"
    allowed_domains = ['xiguaji.com', 'qq.com']

    cookiejson = {
        'ASP.NET_SessionId': 'hrg52bdx5phuhtfvx4nbpnb4'
    }

    url = 'http://www.xiguaji.com/Login/Login'
    values = {
        'chk': "4247fc",
        'email': "18616152909",
        'password': "norman92"
    }
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data)
    cookies = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; XIGUA=UserId=103dad732c906557; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
    request.add_header('Cookie', cookies)
    request.add_header('Host', 'www.xiguaji.com')
    request.add_header('Origin', 'www.xiguaji.com')
    request.add_header('Referer', 'www.xiguaji.com/Login')
    response = urllib2.urlopen(request)
    cookies2 = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
    cookie = cookies2 + "; " + response.headers.get('Set-Cookie')[:-7]

    headers = {
        "Cookie": cookie,
        'Host': 'www.xiguaji.com',
        'Origin': 'www.xiguaji.com',
        'Referer': 'http://www.xiguaji.com/Member',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser,db=dbname,passwd=dbpass,host=dbhost,charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def start_requests(self):
        today = datetime.date.today()
        create_time = time.mktime(today.timetuple())
        try:
            self.cursor.execute("select `url` from `xg_hot_account` where `create_time` = "+str(create_time))
            self.conn.commit()
        except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
        for url in self.cursor.fetchall():
            accountKey = url[0].split('/')[6]
            yield Request(url[0], cookies=self.cookiejson, headers=self.headers, meta={'accountKey': accountKey}, callback=self.parse_main, dont_filter=True)

    def parse_main(self, response):
        sel = Selector(response)
        dataKey = sel.xpath('//a[@id=\"btnLoadMore\"]/@data-key').extract()[0]
        for i in range(1, 20):
            realUrl = "http://www.xiguaji.com/MBiz/GetMBizHistory/"+str(dataKey)+'/'+str(response.meta['accountKey'])+'/'+str(i)
            yield Request(realUrl, cookies=self.cookiejson, headers=self.headers, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        sel = Selector(response)
        items = []
        trContent = sel.xpath('//tr').extract()
        for tr in trContent:
            newText = "<html><body>"+tr+"</body></html>"
            trSel = Selector(text=newText)
            if trSel.xpath('//span[@class=\"artRank rank5\"]/text()').extract():
                item = ArticleItem()
                transmission = trSel.xpath('//span[@class=\"artRank rank5\"]/text()').extract()
                text = trSel.xpath('//td/text()').extract()
                item['transmission'] = transmission[0]
                item['title'] = trSel.xpath('//td/a/text()').extract()[0]
                item['read'] = text[0]
                item['like'] = text[1]
                item['publish_date'] = text[2]
                item['update_date'] = text[3]
                item['articleId'] = trSel.xpath('//td/a/@data-articleid').extract()[0]
                item['url'] = trSel.xpath('//td/a/@href').extract()[0]
                items.append(item)

            for item in items:
                yield Request(item['url'], callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        sel = Selector(response)
        item = response.meta['item']
        items = []
        content = sel.xpath('//div[@id=\"js_content\"]').extract()
        source_url = sel.xpath('//div[@id=\"js_sg_bar\"]/a[@class=\"media_tool_meta meta_primary\"]/@href').extract()
        author = sel.xpath('//em[@class=\"rich_media_meta rich_media_meta_text\"][2]/text()').extract()
        account = sel.xpath('//a[@id=\"post-user\"]/text()').extract()
        if account:
            item['account'] = account[0]
        else:
            item['account'] = ''
        if content:
            item['content'] = content[0]
        else:
            item['content'] = ''
        if source_url:
            item['source_url'] = source_url[0]
        else:
            item['source_url'] = ''
        if author:
            item['author'] = author[0]
        else:
            item['author'] = ''
        detailUrl = "http://www.xiguaji.com/Analyse/ArticleDetail/?articleId="+str(item['articleId'])
        items.append(item)
        yield Request(detailUrl, cookies=self.cookiejson, headers=self.headers, callback=self.parse_detail, meta={'item': item},
                      dont_filter=True)

    def parse_detail(self, response):
        sel = Selector(response)
        items = []
        item = response.meta['item']
        item['related'] = sel.xpath('//div[@class=\"mpArticleRelated\"]').extract()[0]
        item['compare'] = sel.xpath('//div[@class=\"mpArticleCompare\"]').extract()[0]
        bizDataRe = re.compile('var bizData = JSON.parse\(\'(.*)\'\);')
        tagDataRe = re.compile('var tagData = JSON.parse\(\'(.*)\'\);')
        biz_data = bizDataRe.findall(response.body)
        tag_data = tagDataRe.findall(response.body)
        item['biz_data'] = biz_data[0]
        item['tag_data'] = tag_data[0]
        items.append(item)
        analyseUrl = "http://www.xiguaji.com/Analyse/ArticleAnalyse?articleId="+str(item['articleId'])

        yield Request(analyseUrl, cookies=self.cookiejson, headers=self.headers, callback=self.parse_analyse,
                      meta={'item': item},
                      dont_filter=True)

    def parse_analyse(self, response):
        item = response.meta['item']
        item['analyse'] = response.body
        return item