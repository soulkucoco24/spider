# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AccountItem(Item):
    transmission = Field()
    name = Field()
    fans = Field()
    account = Field()
    biz = Field()
    intro = Field()