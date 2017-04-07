# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WxItem(Item):
    title = Field()
    content = Field()
    source_url = Field()
    account = Field()
    author = Field()
    publish_date = Field()
    summary = Field()
    url = Field()
    tips = Field()
    read = Field()
    rank = Field()
    cover_pic = Field()