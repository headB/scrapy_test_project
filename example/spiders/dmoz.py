from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import CrawlSpider
from example.items import SogouItem


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'sogou'
    allowed_domains = ['sogou.com']
    #start_urls = ['https://pinyin.sogou.com/dict/cate/index/']
    #尝试去捉取
    start_urls = ['https://pinyin.sogou.com/dict/cate/index/']
    #start_urls = ['https://pinyin.sogou.com/dict/cate/index/']

    rules = [
        Rule(LinkExtractor(allow=r'dict/cate/index'), 'parse_directory',follow=True)
        #Rule(LinkExtractor(
         #   restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        #), callback='parse_directory', follow=True),
    ]

    def parse_directory(self, response):
        items = SogouItem()
        title = response.xpath("//title/text()").extract()
        items['urlLink'] = response.url
        items['title'] = title
        yield items


