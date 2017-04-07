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
    name = Field()
    author = Field()
    publish_date = Field()
    summary = Field()
    content_url = Field()
    tips = Field()
    read = Field()
    rank = Field()
    url = Field()
    account = Field()