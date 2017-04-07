# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from spider.items import *
import MySQLdb
import base64
import simplejson
import re
import sys
import urllib
import time
import traceback

dbuser = 'root'
dbpass = 'qwerasdf'
dbname = 'wx_helper'
dbhost = '127.0.0.1'
dbport = '3306'


class articleTaskSpider(CrawlSpider):
    name = "articleTask"
    allowed_domains = ['qq.com']

    conn = None
    cursor = None

    def __init__(self):
        self.connect_db()

    def connect_db(self):
        self.conn = MySQLdb.connect(user=dbuser, db=dbname, passwd=dbpass, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def sql_query(self, sql, parameters=None):
        try:
            self.cursor.execute(sql, parameters)
        except MySQLdb.Error, e:
            if 'MySQL server has gone away' in str(e):
                self.connect_db()

    def sql_commit(self):
        self.conn.commit()

    def start_requests(self):
        while 1:
            try:
                self.sql_query("select * from `spider_article_task` limit 1")
                self.sql_commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

            empty_pool = 0
            # print self.cursor.fetchall()
            for info in self.cursor.fetchall():
                empty_pool = 1
                print "id:" + str(info[0])
                self.sql_query("delete from spider_article_task where `id` = " + str(info[0]))
                self.sql_commit()
                if info[3]:
                    try:
                        jsonFormat = simplejson.loads(info[3])

                        for i in jsonFormat:
                            datetime = i['comm_msg_info']['datetime']
                            app_msg = i['app_msg_ext_info']
                            subtype = app_msg['subtype']
                            if app_msg['content_url']:
                                title = app_msg['title']
                                digest = app_msg['digest']
                                fileid = app_msg['fileid']
                                content_url = app_msg['content_url']
                                source_url = app_msg['source_url']
                                cover = app_msg['cover']
                                author = app_msg['author']
                                if app_msg.has_key('copyright_stat'):
                                    copyright_stat = app_msg['copyright_stat']
                                else:
                                    copyright_stat = 0

                                yield Request(content_url + info[2], meta={
                                    'id': info[0],
                                    'content_url': content_url,
                                    'auth_param': info[2],
                                    'biz': content_url.split('&')[0].split("biz=")[1],
                                    'title': title,
                                    'digest': digest,
                                    'fileid': fileid,
                                    'source_url': source_url,
                                    'cover': cover,
                                    'author': author,
                                    'copyright_stat': copyright_stat,
                                    'datetime': datetime,
                                    'subtype': subtype,
                                    'create_time': info[1],
                                }, callback=self.parse_first, dont_filter=True)

                            is_multi = i['app_msg_ext_info']['is_multi']
                            if is_multi:
                                for j in i['app_msg_ext_info']['multi_app_msg_item_list']:
                                    if j['content_url']:
                                        title = j['title']
                                        digest = j['digest']
                                        fileid = j['fileid']
                                        content_url = j['content_url']
                                        source_url = j['source_url']
                                        cover = j['cover']
                                        author = j['author']
                                        if j.has_key('copyright_stat'):
                                            copyright_stat = j['copyright_stat']
                                        else:
                                            copyright_stat = 0

                                        yield Request(content_url + info[2], meta={'id': info[0],
                                                                                   'content_url': content_url,
                                                                                   'auth_param': info[2],
                                                                                   'biz':
                                                                                       content_url.split('&')[0].split(
                                                                                           "biz=")[1],
                                                                                   'title': title,
                                                                                   'digest': digest,
                                                                                   'fileid': fileid,
                                                                                   'source_url': source_url,
                                                                                   'cover': cover,
                                                                                   'author': author,
                                                                                   'copyright_stat': copyright_stat,
                                                                                   'datetime': datetime,
                                                                                   'subtype': subtype,
                                                                                   'create_time': info[1],
                                                                                   }, callback=self.parse_first,
                                                      dont_filter=True)
                    except Exception, e:
                        print info[3]
                        type, value, tb = sys.exc_info()
                        print traceback.format_exception(type, value, tb)
            if not empty_pool:
                print "Sleep 5 Second ..."
                time.sleep(5)
                # for i in jsonFormat:
                #     print i
                # yield Request(info[1], meta={'id': info[0], 'url': info[1], 'auth_param': info[2], 'biz':info[1].split('&')[0].split("biz=")[1]}, callback=self.parse_main, dont_filter=True)

    def parse_first(self, response):
        # items = []
        item = ArticleItem()
        item['id'] = response.meta['id']
        item['content_url'] = response.meta['content_url']
        item['biz'] = base64.decodestring(response.meta['biz'])
        item['title'] = response.meta['title']
        item['digest'] = response.meta['digest']
        item['fileid'] = response.meta['fileid']
        item['source_url'] = response.meta['source_url']
        item['cover'] = response.meta['cover']
        item['author'] = response.meta['author']
        item['copyright_stat'] = response.meta['copyright_stat']
        item['datetime'] = response.meta['datetime']
        item['subtype'] = response.meta['subtype']
        # items.append(item)
        return [scrapy.Request(item['content_url'], callback=self.parse_content,
                               meta={'item': item, 'auth_param': response.meta['auth_param'],
                                     'create_time': response.meta['create_time']})]

    def parse_content(self, response):
        item = response.meta['item']
        auth_param = response.meta['auth_param']
        sel = Selector(response)
        content = sel.xpath('//div[@id=\"js_content\"]').extract()
        account = sel.xpath('//a[@id=\"post-user\"]/text()').extract()
        if content:
            item['content'] = content[0]
        else:
            violation = sel.xpath('//p[@class=\"tips\"]/text()').extract()
            item['violation'] = violation[0]
        if account:
            item['account'] = account[0]
        else:
            item['account'] = ''

        m = re.search(r'window\.wxtoken = "(\w*?)"', response.text)
        if m:
            wxtoken = m.group(1)
        else:
            wxtoken = ''

        m = re.search(r'comment_id = "(\w*?)"', response.text)
        if m:
            comment_id = m.group(1)
        else:
            comment_id = ''

        m = re.search(r'req_id\s*=\s*[\'"](\w*?)[\'"]', response.text)
        if m:
            req_id = m.group(1)
        else:
            req_id = '1'
        articleParam = response.url.split("?")[1]

        msgExtUrl = "http://mp.weixin.qq.com/mp/getappmsgext?" + articleParam + \
                    'title=' + urllib.quote_plus(item['title'].encode('utf8')) + \
                    "&ct=" + str(item['datetime']) + \
                    "&version=/mmbizwap/zh_CN/htmledition/js/appmsg/index2fb0b1.js" + \
                    "&appmsg_type=" + str(item['subtype']) + \
                    "&f=json" + \
                    "&r=0." + str(item['datetime']) + \
                    "&is_need_ad=0" + \
                    "&comment_id=" + comment_id + \
                    "&is_need_reward=0" + \
                    "&both_ad=1" + \
                    "&reward_uin_count=0" + \
                    "&wxtoken=" + wxtoken + \
                    "&clientversion=61030004" + \
                    "&x5=0" + auth_param + '#wechat_webview_type=1'

        postData = {
            "is_only_read": "1",
            "req_id": req_id,
            "is_temp_url": "0"
        }
        yield Request(msgExtUrl, method="POST",
                      body=urllib.urlencode(postData),
                      callback=self.parse_read_total_ok,
                      errback=self.parse_read_total_failed,
                      meta={"item": item}, headers={"X-Requested-With": "XMLHttpRequest"})

    def parse_read_total_ok(self, response):
        item = response.meta['item']
        res = simplejson.loads(response.text)
        if res:
            if res.has_key('appmsgstat'):
                item['read_num'] = res['appmsgstat']['read_num']
                item['like_num'] = res['appmsgstat']['like_num']
        return item

    def parse_read_total_failed(self, response):
        item = response.meta['item']
        return item
