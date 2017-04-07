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
    # def __init__(self):
    # self.conn = MySQLdb.connect(user=dbuser, db=dbname, passwd=dbpass, host=dbhost, charset="utf8",
    #                             use_unicode=True)
    # self.cursor = self.conn.cursor()
    # self.conn.commit()

    def process_item(self, item, spider):
        # today = datetime.date.today()
        # create_time = time.mktime(today.timetuple())
        create_time = int(time.time())
        try:
            if item['content']:
                spider.sql_query("""INSERT INTO wx_article_copy (account, title, author, datetime, source_url, create_time, content_url, copyright_stat, biz, digest, fileid, cover, subtype,read_num,like_num, content)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                 (
                                     item['account'],
                                     item['title'],
                                     item['author'],
                                     item['datetime'],
                                     item['source_url'],
                                     create_time,
                                     item['content_url'],
                                     item['copyright_stat'],
                                     item['biz'],
                                     item['digest'],
                                     item['fileid'],
                                     item['cover'],
                                     item['subtype'],
                                     item.get('read_num', '0'),
                                     item.get('like_num', '0'),
                                     item.get('content', ''),
                                 )
                                 )

            else:
                spider.sql_query(
                    """INSERT INTO wx_article_violation (biz, title, author, datetime, content_url, create_time) VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        item['account'],
                        item['title'],
                        item['author'],
                        item['datetime'],
                        item['content_url'],
                        create_time,
                    )
                )
            spider.sql_commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item
