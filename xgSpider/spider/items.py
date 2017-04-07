# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class XgItem(Item):
    pic = Field()
    account = Field()
    wx_account = Field()
    fans_number = Field()
    transmission = Field()
