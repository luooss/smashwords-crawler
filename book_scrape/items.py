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
    file_urls = scrapy.Field()
    files = scrapy.Field()

    def __repr__(self):
        ###Keep your shell clean###
        return '\n' + repr({'title': self['title'],
                            'author': self['author'],
                            'word_count': self['word_count'],
                            'file_urls': self['file_urls']}) + '\n'