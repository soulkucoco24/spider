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
dbname = 'testpy'
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
            self.cursor.execute("""INSERT INTO tgh (`name`, account, topRead, fans, topPrice, unTopPrice, tag, orderRate, credit, costRate, fTag)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                item['name'],
                                item['account'],
                                item['topRead'],
                                item['fans'],
                                item['topPrice'],
                                item['unTopPrice'],
                                item['tag'],
                                item['orderRate'],
                                item['credit'],
                                item['costRate'],
                                item['fTag'],
                            )
            )
            self.conn.commit()
        except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
        return item

