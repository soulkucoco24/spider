# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    name = Field()
    account = Field()
    topRead = Field()
    fans = Field()
    topPrice = Field()
    unTopPrice = Field()
    tag = Field()
    orderRate = Field()
    credit = Field()
    costRate = Field()
    fTag = Field()
