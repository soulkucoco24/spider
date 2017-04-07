# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import datetime
import time

dbuser = 'root'
dbpass = 'qwerasdf'
dbname = 'wx_helper'
dbhost = '127.0.0.1'
dbport = '3306'

class RankPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser,db=dbname,passwd=dbpass,host=dbhost,charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        today = datetime.date.today()
        create_time = time.mktime(today.timetuple())

        try:
            for i in range(0, 25):
                for j in range(0, 10):
                    self.cursor.execute("""INSERT INTO wx_rank (tips, account, sevenRead, rank, create_time)
                                    VALUES (%s, %s, %s, %s, %s)""",
                                        (
                                            item['tips'][i][0],
                                            item['accounts'][i][j],
                                            item['sevenReads'][i][j],
                                            j+1,
                                            create_time,
                                        )
                    )
                    self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item

