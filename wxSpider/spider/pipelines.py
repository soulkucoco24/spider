# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import datetime
import time
import datetime

dbuser = 'root'
dbpass = 'qwerasdf'
dbname = 'wx_helper'
dbhost = '127.0.0.1'
dbport = '3306'

class WxPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser,db=dbname,passwd=dbpass,host=dbhost,charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        today = datetime.date.today()
        create_time = time.mktime(today.timetuple())
        try:
            self.cursor.execute("""INSERT INTO wx_media (account, title, author, publish_date, source_url, content, summary, create_time, cover_pic, url, tips, `read`)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                item['account'],
                                item['title'],
                                item['author'],
                                item['publish_date'],
                                item['source_url'],
                                item['content'],
                                item['summary'],
                                create_time,
                                item['cover_pic'],
                                item['url'],
                                item['tips'],
                                item['read']
                            )
            )
            self.conn.commit()
        except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
        return item

