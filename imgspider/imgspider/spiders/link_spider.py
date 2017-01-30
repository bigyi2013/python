#encoding:utf-8
import scrapy
from imgspider.items import imgspiderItem
class imgSpider(scrapy.Spider):
    name = "meiziimg"
    download_delay = 0.2
    allowed_domains = ["meizitu.com"]
    start_urls = [
        "http://www.meizitu.com/a/list_1_2.html"
    ]


    # def parse(self, response):
    #     for href in response.xpath('//a[@class="p1 nexe"]/@href'):
    #         url = response.urljoin(href.extract())
    #         print url
    #         yield scrapy.Request(url, callback=self.parse)
    def parse (self, response):
        for soup in response.xpath('//ul[@class="wp-list clearfix"]/li[@class="wp-item"]'):
            item = imgspiderItem()
            item['title'] = soup.xpath('div/div[@class="pic"]/a/img/@alt')[0].extract()
            item['link'] = soup.xpath('div/div[@class="pic"]/a/@href')[0].extract()
            item['src'] = soup.xpath('div/div[@class="pic"]/a/img/@src')[0].extract()
            taglink = soup.xpath('div/div[@class="pic"]/a/@href')[0].extract()
            tagurl=response.urljoin(taglink)
            yield scrapy.Request(tagurl, callback=self.gettag)
            yield item
        for links in response.xpath('//div[@id="wp_page_numbers"]//a/@href'):
                url=response.urljoin(links.extract())
                yield scrapy.Request(url,self.parse)
    def gettag(self, response):
        item = imgspiderItem()
        item['link']=response.url
        item['tag'] = response.xpath('//div[@class="metaRight"]/p/text()')[0].extract()
        return item