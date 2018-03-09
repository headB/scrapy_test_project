from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from example.items import ItcastItem


class DmozSpider(RedisCrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['sogou.com']
    #start_urls = ['https://pinyin.sogou.com/dict/cate/index/']
    #尝试去捉取
    start_urls = ['https://pinyin.sogou.com/dict/cate/index/']

    rules = [
        Rule(LinkExtractor(allow=r'dict/cate/index'), 'parse_directory',follow=True)
        #Rule(LinkExtractor(
         #   restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        #), callback='parse_directory', follow=True),
    ]

    def parse_directory(self, response):
        items =
        title = response.xpath("//title")



