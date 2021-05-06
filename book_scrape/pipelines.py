# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from scrapy.exceptions import DropItem
import ebooklib
from ebooklib import epub
# from mobi import Mobi
# import textract


class ExtractTextPipeline:
    def process_item(self, item, spider):
        if not item['files']:
            raise DropItem("Missing content for %s" % item['title'])
        else:
            # print(item['files'])
            # print(item['files'][0])
            file_path = './downloaded/' + item['files'][0]['path']
            file_name = file_path.split('/')[-1]
            sidx = file_name.rfind('.')
            if sidx < 0:
                raise DropItem("Missing content for %s" % item['title'])
            else:
                file_format = file_name[sidx+1:]
                if file_format == 'txt':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        item['content'] = f.read()

                elif file_format == 'epub':
                    book = epub.read_epub(file_path)
                    item['content'] = ''
                    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                        item['content'] += doc.get_content().decode('utf-8')

                elif file_format == 'mobi':
                    raise DropItem("Missing content for %s" % item['title'])
                    # book = Mobi(file_path)
                    # book.parse()
                    # item['content'] = ''
                    # for record in book:
                    #     item['content'] += record

                elif file_format == 'pdf':
                    raise DropItem("Missing content for %s" % item['title'])
                    # item['content'] = textract.process(file_path)
        
        return item


class SaveAsJsonPipeline:
    def open_spider(self, spider):
        self.file = open('books.jl', 'w')
    
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
