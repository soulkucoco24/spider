# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    title = Field()
    read_num = Field()
    like_num = Field()
    source_url = Field()
    account = Field()
    author = Field()
    publish_date = Field()
    content_url = Field()
    tips = Field()
    digest = Field()
    rank = Field()
    cover = Field()
    copyright_stat = Field()
    datetime = Field()
    biz = Field()
    id = Field()
    fileid = Field()
    subtype = Field()
    violation = Field()
    content = Field()
