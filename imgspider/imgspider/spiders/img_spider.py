#encoding:utf-8
import scrapy
from imgspider.items import imgspiderItem
class imgSpider(scrapy.Spider):
    name = "img"
    allowed_domains = ["gamersky.com"]
    start_urls = [
        "http://tag.gamersky.com/news/653.html"
    ]
    def parse (self,response):
        for soup in response.xpath('//div[@class="con"]/div[@class="tit"]'):
            item = imgspiderItem()
            item['title'] = soup.xpath('a/@title')[0].extract()
            item['link'] = soup.xpath('a/@href')[0].extract()
            yield item
        for links in response.xpath('//span[@id="pe100_page_allnews"]/a/@href'):
                url=response.urljoin(links.extract())
                yield scrapy.Request(url,self.parse)
