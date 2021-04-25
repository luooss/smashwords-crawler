# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    word_count = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    detail_url = scrapy.Field()
    txt_url = scrapy.Field()