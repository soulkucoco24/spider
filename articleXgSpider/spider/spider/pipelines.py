# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import time
import datetime

dbuser = 'root'
dbpass = 'qwerasdf'
dbname = 'wx_helper'
dbhost = '127.0.0.1'
dbport = '3306'

class ArticlePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser,db=dbname,passwd=dbpass,host=dbhost,charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        today = datetime.date.today()
        create_time = time.mktime(today.timetuple())
        try:
            self.cursor.execute("""INSERT INTO xg_wx_article (account, title, author, publish_date, update_date, source_url, content, create_time, url, `read`, `like`, transmission, articleId, related, compare, biz_data, tag_data, analyse)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                item['account'],
                                item['title'],
                                item['author'],
                                item['publish_date'],
                                item['update_date'],
                                item['source_url'],
                                item['content'],
                                create_time,
                                item['url'],
                                item['read'],
                                item['like'],
                                item['transmission'],
                                item['articleId'],
                                item['related'],
                                item['compare'],
                                item['biz_data'],
                                item['tag_data'],
                                item['analyse'],
                            )
            )
            self.conn.commit()
        except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
        return item

