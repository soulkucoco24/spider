# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from spider.items import *
import urllib2
import urllib
import base64
import random


class accountSpider(CrawlSpider):
    name = "account"
    allowed_domains = ['xiguaji.com', 'qq.com']

    cookiejson = {
        'ASP.NET_SessionId': 'zwvgyvuglhkwpdlggsh15lfq'
    }

    url = 'http://www.xiguaji.com/Login/Login'
    values = {
        'email': "13061917819",
        'password': "jieJIE123",
        'chk': "6ebbea",
    }
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data)
    cookies = 'Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1470972121,1471082145,1471226103,1471412823; XIGUASTATE=XIGUASTATEID=e2296ebbeaf74e1890ff15c2b981ba20; chl=key=FromBaiDu&word=6KW/55Oc5YWs5LyX5Y+35Yqp5omL; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa =1471484156; ASP.NET_SessionId=hrg52bdx5phuhtfvx4nbpnb4; XIGUA=UserId=103dad732c906557'
    request.add_header('Cookie', cookies)
    request.add_header('Host', 'www.xiguaji.com')
    request.add_header('Origin', 'www.xiguaji.com')
    request.add_header('Referer', 'www.xiguaji.com/Login')
    response = urllib2.urlopen(request)
    cookies2 = 'Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1470972121,1471082145,1471226103,1471412823; XIGUASTATE=XIGUASTATEID=e2296ebbeaf74e1890ff15c2b981ba20; chl=key=FromBaiDu&word=6KW/55Oc5YWs5LyX5Y+35Yqp5omL; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa =1471484156; ASP.NET_SessionId=hrg52bdx5phuhtfvx4nbpnb4'
    cookie = cookies2 + "; " + response.headers.get('Set-Cookie')[:-7]
    headers = {
        "Cookie": cookie,
        'Host': 'www.xiguaji.com',
        'Origin': 'www.xiguaji.com',
        'Referer': 'http://www.xiguaji.com/Member',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }

    def start_requests(self):
        file_object = open('dict.txt', 'rb')
        list_of_all_the_lines = file_object.readlines()
        for word in list_of_all_the_lines:
            keyword = word.split('\r\n')[0]
            print keyword
            for page in range(1, 5):
                url = "http://www.xiguaji.com/MyMBiz/MBizAsyncSearch/?page="+str(page)+"&keyword="+str(keyword)
                yield Request(url, cookies=self.cookiejson, headers=self.headers, callback=self.parse_main, dont_filter=True)

    def parse_main(self, response):
        print response.status
        Sel = Selector(response)
        link = Sel.xpath('//h3/a/@href').extract()
        for url in link:
            real_url = "http://www.xiguaji.com"+url.split("#")[1]
            accountKey = real_url.split('/')[6]
            yield Request(real_url, cookies=self.cookiejson, headers=self.headers, meta={'accountKey': accountKey}, callback=self.parse_account, dont_filter=True)

    def parse_account(self, response):
        sel = Selector(response)
        name = sel.xpath("//h3[@class=\"mpName\"]/text()").extract()
        account = sel.xpath("//h4[@class=\"mpId\"]/text()").extract()
        intro = sel.xpath("//div[@class=\"mpIntro\"]/text()").extract()
        info = sel.xpath("//dd/text()").extract()
        items = []
        item = AccountItem()
        item['name'] = name[0]
        item['account'] = account[0].split(u"：")[1]
        item['fans'] = info[0]
        item['transmission'] = info[1]
        if intro:
            item['intro'] = intro[0]
        else:
            item['intro'] = ''
        items.append(item)
        dataKey = sel.xpath('//a[@id=\"btnLoadMore\"]/@data-key').extract()[0]
        real_url = "http://www.xiguaji.com/MBiz/GetMBizHistory/" + str(dataKey) + '/' + str(response.meta['accountKey']) + '/1'
        return scrapy.Request(real_url, cookies=self.cookiejson, headers=self.headers, callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        sel = Selector(response)
        item = response.meta['item']
        url = sel.xpath('//td/a/@href').extract()
        if url:
            item['biz'] = base64.decodestring(url[0].split('&')[0].split("biz=")[1])
        else:
            item['biz'] = '100000'+str(random.uniform(10000000, 99999999))
        return item
