# -*- coding: utf-8 -*-
"""
Created on 2023-01-19 11:28:17
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import datetime
from items.my_spider_integrated_baidu_news_test_item import MySpiderIntegratedBaiduNewsTestItem
from feapder.dedup import Dedup


class MyBaiduNewsParserTest(feapder.BaseParser):
    def __init__(self,*args,**kwargs):
        # filter_type：去重类型，支持BloomFilter、MemoryFilter、ExpireFilter三种
        self.dedup = Dedup() # 默认是永久去重

    """
    注意 这里继承的是BaseParser，而不是Spider
    """
    # # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="localhost:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    # )
    def download_midware(self, request):
        request.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request


    def start_requests(self):
        yield feapder.Request("https://top.baidu.com/board?tab=realtime")

    def parse(self, request, response):
        div_list = response.xpath('..//div[contains(@class,"category-wrap_iQLoo") and contains(@class,"horizontal_1eKyQ")]')
        for per_div in div_list:
            item = MySpiderIntegratedBaiduNewsTestItem()
            # 标题
            item["title"] = per_div.xpath('.//div[@class="c-single-text-ellipsis"]/text()').extract_first().strip()
            # 热度值
            item["hot_search_index"] = per_div.xpath('.//div[@class="hot-index_1Bl1a"]/text()').extract_first().strip()
            if self.dedup.add(item):
                # 插入时间
                item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item


if __name__ == "__main__":
    MyBaiduNewsParserTest(redis_key="xxx:xxx").start()
