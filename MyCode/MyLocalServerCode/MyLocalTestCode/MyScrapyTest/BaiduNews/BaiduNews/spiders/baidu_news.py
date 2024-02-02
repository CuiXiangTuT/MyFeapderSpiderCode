import scrapy
from ..items import BaidunewsItem

class BaiduNewsSpider(scrapy.Spider):
    name = 'baidu_news'
    # allowed_domains = []
    # start_urls = ['https://top.baidu.com/board?tab=realtime']

    def start_requests(self):
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(url=url,callback=self.parse,method="GET",headers=headers,dont_filter=True)

    def parse(self, response):

        title_list = response.xpath('//div[@class="c-single-text-ellipsis"]/text()').extract()
        for title in title_list:
            item = BaidunewsItem()
            item['title'] = title.strip()
            # print(item)
            yield item

