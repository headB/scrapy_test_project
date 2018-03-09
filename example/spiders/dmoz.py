from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import CrawlSpider
from example.items import SogouItem
import re
from urllib.parse import urljoin

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

        firstDemoUrl = ''

        if  items['languageNum']:
            x1 = re.search(r'方言',items['languageNum'])
            if 'group' not in dir(x1):
                items['languageNum'] = ''.join(response.xpath('//*[@id="dict_cate_show"]/table/tbody/tr/td[5]/div/a//text()').extract())
                firstDemoUrl = response.xpath('//*[@id="dict_cate_show"]/table/tbody/tr/td[5]/div/a/@href').extract()
            else:
                firstDemoUrl = response.xpath('//*[@id="dict_cate_show"]/table/tbody/tr/td[6]/div/a//@href').extract()

        ##准备测试,看看能不能将自己的优秀基因遗传下去

        #firstDemoUrl = response.xpath()
        if firstDemoUrl:
            base_url = response.url
            firstDemoUrl = urljoin(base_url,firstDemoUrl[0])
            yield Request(firstDemoUrl,meta={'sogouItems':items},callback=self.xx1,)

    def xx1(self,response):
        items = response.meta['sogouItems']

        x1 = ''.join(response.xpath('//div[@id="dict_detail_list"]/div[2]//text()').extract())
        x1 = x1.replace(' ','').replace('\r\n','').replace('\t','')
        items['description'] = x1
        yield items


    def parse_directory(self, response):
        items = SogouItem()
        title = response.xpath("//title/text()").extract()

        items['urlLink'] = response.url
        items['title'] = title
        yield items


