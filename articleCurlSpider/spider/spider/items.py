# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    title = Field()
    content = Field()
    source_url = Field()
    account = Field()
    wx_account = Field()
    author = Field()
    publish_date = Field()
    summary = Field()
    url = Field()
    tips = Field()
    read = Field()
    rank = Field()
    pic = Field()
    spider_link = Field()
    fans_number = Field()
    transmission = Field()
    articleId = Field()
    related = Field()
    compare = Field()