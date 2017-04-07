# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
import urllib2
import urllib
from spider.items import *

class XgSpider(CrawlSpider):
    name = "xg"
    allowed_domains = ['xiguaji.com']
    start_urls = [
        'http://www.xiguaji.com/Home/Dashboard'
    ]
    cookies = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; XIGUA=UserId=103dad732c906557; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
    headers = {
        "Cookie":cookies,
        'Host':'www.xiguaji.com',
        'Origin':'www.xiguaji.com',
        'Referer': 'www.xiguaji.com/Login'
    }

    def start_requests(self):
        # formdata = {
        #     'email': '18616152909',
        #     'password': 'norman92',
        #     "chk": "4247fc"
        # }
        # return  [Request("http://www.xiguaji.com/Login/Login",
        #                  meta={'cookiejar': 1,
        #                        'email': '18616152909',
        #                        'password': 'norman92',
        #                        'chk': '4247fc'
        #                        },
        #                  body="email=18616152909&password=norman92&chk=4247fc",
        #                  method="POST",
        #                  headers=self.headers,
        #                 callback=self.test)]
        # return [FormRequest("http://www.xiguaji.com/Login/Login", headers=self.headers, method="POST", callback=self.test, formdata=formdata)]

        url = 'http://www.xiguaji.com/Login/Login'
        values = {
            'chk': "4247fc",
            'email': "18616152909",
            'password': "norman92"
        }
        data = urllib.urlencode(values)
        # print data
        request = urllib2.Request(url, data)
        cookies = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; XIGUA=UserId=103dad732c906557; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
        request.add_header('Cookie', cookies)
        request.add_header('Host', 'www.xiguaji.com')
        request.add_header('Origin', 'www.xiguaji.com')
        request.add_header('Referer', 'www.xiguaji.com/Login')
        response = urllib2.urlopen(request)
        # print response.headers.get('Set-Cookie')
        # the_page = response.read()
        # print the_page
        cookies2 = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
        cookie = cookies2+"; "+response.headers.get('Set-Cookie')[:-7]
        print cookie
        print "------------------------"
        headers = {
            "Cookie": cookie,
            'Host': 'www.xiguaji.com',
            'Origin': 'www.xiguaji.com',
            'Referer': 'http://www.xiguaji.com/Member',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
        }
        cookiejson = {
            'ASP.NET_SessionId' : 'tcpj5v4o2jcigri3m5xz4dgr'
        }
        print headers
        return  [Request("http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=35&DateCode=20160811&page=1", cookies=cookiejson, headers=headers, callback=self.parse_main, dont_filter=True)]

    def test(self, response):
        print response.headers
        print response.body

    def parse_main(self, response):
        sel = Selector(response)
        items = []
        wx_accounts = sel.xpath('//div[@class=\"rankMpName\"]/a/text()').extract()
        pics = sel.xpath('//div[@class=\"rankMpCover\"]/img/@src').extract()
        accounts = sel.xpath('//div[@class=\"rankMpName\"]/em/text()').extract()
        urls = sel.xpath('//div[@class=\"rankMpName\"]/a/@href').extract()

        for i in range(0,50):
            item = XgItem()
            # item['pic'] = pics[i]
            item['account'] = accounts[i]
            item['wx_account'] = wx_accounts[i]
            item['url'] = "http://www.xiguaji.com/Member"+str(urls[i])
            print item
            exit()
            items.append(item)
        for item in items:
            yield scrapy.Request(item['url'], callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['fans_number'] = sel.xpath('//div[@class=\"mpStat clearfix\"]/dl[@class=\"col col-lg-6\"]/dd/text()').extract()[0]
        item['transmission'] = sel.xpath('//div[@class=\"mpStat clearfix\"]/dl[@class=\"col col-lg-6\"]/dd/text()').extract()[1]
        print item
        exit()



    def get_cookie(self):
        url = 'http://www.xiguaji.com/Login/Login'
        values = {
            'chk': "4247fc",
            'email': "18616152909",
            'password': "norman92"
        }
        data = urllib.urlencode(values)
        # print data
        request = urllib2.Request(url, data)
        cookies = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; XIGUA=UserId=103dad732c906557; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
        request.add_header('Cookie', cookies)
        request.add_header('Host', 'www.xiguaji.com')
        request.add_header('Origin', 'www.xiguaji.com')
        request.add_header('Referer', 'www.xiguaji.com/Login')
        response = urllib2.urlopen(request)
        # print response.headers.get('Set-Cookie')
        # the_page = response.read()
        # print the_page
        cookies2 = 'chl=key=www.jsform.com; ASP.NET_SessionId=tcpj5v4o2jcigri3m5xz4dgr; XIGUASTATE=XIGUASTATEID=236d4247fcef45f7bd328e9178999ebc; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1469413619,1470297426,1470908268; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1470909225'
        return cookies2+"; "+response.headers.get('Set-Cookie')[:-7]

    # def post_login(self, response):
    #     print 'Preparing login====', response.url
    #     return [FormRequest.from_response(response,
    #                                       meta={'cookiejar': response.meta['cookiejar']},
    #                                       formdata={
    #                                           'email' : '18616152909',
    #                                           'password' : 'norman92',
    #                                           "chk": "6ebbea"
    #                                       },
    #                                       headers=self.headers,
    #                                       callback=self.after_login,
    #                                       dont_filter=True
    #                                       )]

    def after_login(self, response):
        print response.header
        exit()
        # xmlHeader = {
        #     "Accept": "text/html, */*; q=0.01",
        #     "Accept-Encoding": "gzip,deflate",
        #     "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        #     "Host": "www.xiguaji.com",
        #     "Referer": "http://www.xiguaji.com/Member",
        #     "X-Requested-With" : "XMLHttpRequest",
        # }
        for url in self.start_urls:
            print '============url'
            yield Request('http://www.xiguaji.com/Member#/Home/Dashboard',meta={'cookiejar':response.meta['cookiejar']}, callback=self.parse_rank)

    def parse_rank(self, response):
        print '============stats'
        print response

    #
    # def parse(self, response):
    #     print "-------------------"
    #     print self.get_cookie()
    #     print "-------------------"
    #     return  [Request("http://www.xiguaji.com/Home/Dashboard",
    #                      headers={
    #                          'Cookie':self.get_cookie,
    #                          'Host':'www.xiguaji.com',
    #                          'Referer': 'www.xiguaji.com/Login',
    #                          'Origin': 'www.xiguaji.com'
    #                      },
    #                     callback=self.test)]
    #
    # def test(self, response):
    #     print response.body