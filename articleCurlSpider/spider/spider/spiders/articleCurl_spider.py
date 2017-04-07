# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
import urllib2
import urllib
from spider.items import *

class articleCurlSpider(CrawlSpider):
    name = "articleCurl"
    allowed_domains = ['xiguaji.com']
    start_urls = [
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=35&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=33&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=27&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=26&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=1443&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=1500&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=97&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=32&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=34&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=30&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=31&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=36&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=1434&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=128&page=1',
        'http://www.xiguaji.com/Mbiz/Rank/?partial=1&tagId=37&page=1',
    ]
    cookiejson = {
        'ASP.NET_SessionId': 'hrg52bdx5phuhtfvx4nbpnb4'
    }

    url = 'http://www.xiguaji.com/Login/Login'
    values = {
        'email': "13061917819",
        'password': "jieJIE123",
        'chk': "6ebbea",
    }
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data)
    cookies = 'Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1470972121,1471082145,1471226103,1471412823; XIGUASTATE=XIGUASTATEID=e2296ebbeaf74e1890ff15c2b981ba20; chl=key=FromBaiDu&word=6KW/55Oc5YWs5LyX5Y+35Yqp5omL; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa =1471484156; ASP.NET_SessionId=tbg40sfiwhub0mnwh52mulg0; XIGUA=UserId=103dad732c906557'
    request.add_header('Cookie', cookies)
    request.add_header('Host', 'www.xiguaji.com')
    request.add_header('Origin', 'www.xiguaji.com')
    request.add_header('Referer', 'www.xiguaji.com/Login')
    response = urllib2.urlopen(request)
    cookies2 = 'Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1470972121,1471082145,1471226103,1471412823; XIGUASTATE=XIGUASTATEID=e2296ebbeaf74e1890ff15c2b981ba20; chl=key=FromBaiDu&word=6KW/55Oc5YWs5LyX5Y+35Yqp5omL; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa =1471484156; ASP.NET_SessionId=tbg40sfiwhub0mnwh52mulg0'
    cookie = cookies2 + "; " + response.headers.get('Set-Cookie')[:-7]
    headers = {
        "Cookie": cookie,
        'Host': 'www.xiguaji.com',
        'Origin': 'www.xiguaji.com',
        'Referer': 'http://www.xiguaji.com/Member',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }

    def start_requests(self):
        for url in self.start_urls:
            tips = url.split('&')[1].split('=')[1]
            yield Request(url, cookies=self.cookiejson, headers=self.headers, callback=self.parse_main, dont_filter=True, meta={'tips':tips})

    def parse_main(self, response):
        sel = Selector(response)
        items = []
        wx_accounts = sel.xpath('//div[@class=\"rankMpName\"]/a/text()').extract()
        pics = sel.xpath('//div[@class=\"rankMpCover\"]/img/@src').extract()
        accounts = sel.xpath('//div[@class=\"rankMpName\"]/em/text()').extract()
        urls = sel.xpath('//div[@class=\"rankMpName\"]/a/@href').extract()

        for i in range(0,50):
            item = ArticleItem()
            item['tips'] = response.meta['tips']
            if pics[i]:
                item['pic'] = pics[i]
            else:
                item['pic'] = ''

            if accounts[i]:
                item['account'] = accounts[i]
            else:
                item['account'] = ''

            if wx_accounts[i]:
                item['wx_account'] = wx_accounts[i]
            else:
                item['wx_account'] = ''

            if urls[i][2:]:
                item['spider_link'] = "http://www.xiguaji.com/Member#/"+str(urls[i][2:])
                item['url'] = "http://www.xiguaji.com/"+str(urls[i][2:])
            else:
                item['spider_link'] = ''
                item['url'] = ''
            items.append(item)
        for item in items:
            yield scrapy.Request(item['url'], cookies=self.cookiejson, callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):
        sel = Selector(response)
        item = response.meta['item']
        if sel.xpath('//div[@class=\"mpStat clearfix\"]/dl[@class=\"col col-lg-6\"]/dd/text()').extract()[0]:
            item['fans_number'] = sel.xpath('//div[@class=\"mpStat clearfix\"]/dl[@class=\"col col-lg-6\"]/dd/text()').extract()[0]
        else:
            item['fans_number'] = 0

        if sel.xpath('//div[@class=\"mpStat clearfix\"]/dl[@class=\"col col-lg-6\"]/dd/text()').extract()[1]:
            item['transmission'] = sel.xpath('//div[@class=\"mpStat clearfix\"]/dl[@class=\"col col-lg-6\"]/dd/text()').extract()[1]
        else:
            item['transmission'] = 0
        return item

    def test(self, response):
        print response.headers
        print response.body