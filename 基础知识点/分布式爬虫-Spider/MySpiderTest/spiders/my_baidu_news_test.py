# -*- coding: utf-8 -*-
"""
Created on 2023-01-17 16:30:07
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from items.my_spider_test_item import MySpiderTestItem
import datetime


class MyBaiduNewsTest(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="localhost:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    # )
    def download_midware(self, request):
        request.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        print("------自定义下载中间件，这里配置了headers参数------")
        return request

    def start_requests(self):
        yield feapder.Request("https://top.baidu.com/board?tab=realtime")

    def parse(self, request, response):
        # # 提取网站title
        # print(response.xpath("//title/text()").extract_first())
        # # 提取网站描述
        # print(response.xpath("//meta[@name='description']/@content").extract_first())
        # print("网站地址: ", response.url)
        div_list = response.xpath('..//div[contains(@class,"category-wrap_iQLoo") and contains(@class,"horizontal_1eKyQ")]')
        for per_div in div_list:
            item = MySpiderTestItem()
            # 标题
            item["title"] = per_div.xpath('.//div[@class="c-single-text-ellipsis"]/text()').extract_first().strip()
            # 热度值
            item["hot_search_index"] = per_div.xpath('.//div[@class="hot-index_1Bl1a"]/text()').extract_first().strip()
            # 插入时间
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # yield item
            yield item


if __name__ == "__main__":
    # MySpiderTest(redis_key="feapder:spider_test").start()
    
    # 调试模式：通常结合断点来进行调试，debug模式下，运行产生的数据默认不入库
    spider = MyBaiduNewsTest.to_DebugSpider(
        redis_key="feapder:spider_baidu_news_test",request=feapder.Request("https://top.baidu.com/board?tab=realtime")
    )
    spider.start()
