from book_scrape.items import BookItem
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book_spider'
    start_urls = [
        'https://www.smashwords.com/books/category/1/downloads/0/free/any/',
    ]

    def parse(self, response):
        for book_item in response.xpath('//div[@class="library-book row p-2"]'):
            item = BookItem()
            # book_item is a Selector in SelectorList
            item['title'] = book_item.xpath('.//a[@class="library-title"]/text()').get()
            item['author'] = book_item.xpath('.//a[@itemprop="author"]/span/text()').get()
            date = book_item.xpath('.//div[@class="subnote"]/span[3]/text()').get()
            item['publish_date'] = date[date.index(':')+1:].strip()
            count = book_item.xpath('.//div[@class="subnote"]/span[1]/text()').get()
            item['word_count'] = count[count.index(':')+1:count.index('.')].strip()
            item['description'] = book_item.xpath('.//div[@class="card bg-light border-light p-2"]/text()').get().strip()

            # enter inner page and download txt file
            item['detail_url'] = book_item.xpath('.//a[@class="library-title"]/@href').get()
            yield scrapy.Request(item['detail_url'], callback=self.parse_detail, meta={'item':item})
        
        # this is not the only one page-link is this page, attention!!!
        # next_page_url = response.xpath('//a[@class="page-link"]/@href').get()
        next_page_url = response.xpath('.//ul[@class="pagination"]/li[@class="page-item"][last()]/a[@class="page-link"]/@href').get()
        if next_page_url is not None:
            print('\nNext Page:\n' + '*'*90 + '\n' + next_page_url + '\n' + '*'*90 + '\n')
            # important to use response.urljoin, otherwise may go wrong
            # yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_detail(self, response):
        item = response.meta['item']
        # some books don't have txt files available
        post_fix = response.xpath('.//a[@title="Plain text; contains no formatting"]/@href').get()
        if(post_fix == None):
            item['txt_url'] = 'Not available.'
            item['content'] = 'No txt format available.'
            yield item
        else: 
            item['txt_url'] = 'https://www.smashwords.com' + post_fix
            yield scrapy.Request(item['txt_url'], callback=self.download_txt, meta={'item':item})

    def download_txt(self, response):
        item = response.meta['item']
        item['content'] = response.text
        yield item