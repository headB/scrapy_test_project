from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import CrawlSpider
from example.items import SogouItem
import re


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'sogou'
    allowed_domains = ['sogou.com']
    start_urls = ['https://pinyin.sogou.com/dict/cate/index/',]

    ##xpath匹配 所有 中国省份,行政区.  //*[@id="city_list_show"]/table/tbody/tr/td/div/a/text()
    ##xpath匹配 对应方言词库的数量     //*[@id="dict_cate_show"]/table/tbody/tr/td[6]/div/a//text()

    rules = [
        Rule(LinkExtractor(restrict_xpaths=(r'//*[@id="city_list_show"]/table')),callback='splitDictInfo')
        #采用新的规则,获取所有省份信息
        #Rule(LinkExtractor(allow=(r'dict/cate/index')), callback='parse_directory',follow=True),

    ]

    #def collectProvinceInfo(self,response):
    #黑龙江//*[@id="dict_cate_show"]/table/tbody/tr/td[5]/div/a//text()


    def splitDictInfo(self,response):
        items = SogouItem()
        items['province'] = response.xpath('//*[@id="city_input"]//@value').extract()
        #items['title'] = response.xpath("//title/text()").extract()
        items['languageNum'] = ''.join(response.xpath('//*[@id="dict_cate_show"]/table/tbody/tr/td[6]/div/a//text()').extract())


        if  items['languageNum']:
            x1 = re.search(r'方言',items['languageNum'])
            if 'group' not in dir(x1):
                items['languageNum'] = ''.join(response.xpath('////*[@id="dict_cate_show"]/table/tbody/tr/td[5]/div/a//text()').extract())
        yield items

    def parse_directory(self, response):
        items = SogouItem()
        title = response.xpath("//title/text()").extract()

        items['urlLink'] = response.url
        items['title'] = title
        yield items


