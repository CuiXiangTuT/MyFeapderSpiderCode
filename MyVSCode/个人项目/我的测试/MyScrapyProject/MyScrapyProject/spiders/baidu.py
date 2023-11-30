import scrapy
from ..settings import IP_LIST
import random


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.ccgp-liaoning.gov.cn']
    # start_urls = []
       

    def start_requests(self):
        url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList'
        data = {
            "current": '1',  
            "rowCount": "10",
            "infoTypeCode": "1002",
            "privateOrCity": "1",
        }
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        }
        yield scrapy.FormRequest(url=url,formdata=data,headers=headers,callback=self.parse)
    
    def parse(self, response):
        print(response.text)
        print("----------------------------------------------------")
