# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    transmission = Field()
    title = Field()
    read = Field()
    like = Field()
    publish_date = Field()
    update_date = Field()
    url = Field()
    content = Field()
    source_url = Field()
    author = Field()
    account = Field()
    articleId = Field()
    related = Field()
    compare = Field()
    biz_data = Field()
    tag_data = Field()
    analyse = Field()
