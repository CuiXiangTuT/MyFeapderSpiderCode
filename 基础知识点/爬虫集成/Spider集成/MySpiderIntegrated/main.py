# -*- coding: utf-8 -*-
"""
Created on 2023-01-19 11:27:05
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *
from feapder import Spider


def crawl_news():
    """
    Spider爬虫
    """
    spider = Spider(redis_key="feapder:test_spider_integrated_news")
    # 集成
    spider.add_parser(my_baidu_news_parser_test.MyBaiduNewsParserTest)
    spider.add_parser(my_wangyi_news_parser_test.MyWangyiNewsParserTest)
    spider.start()



if __name__ == "__main__":
    crawl_news()
#     parser = ArgumentParser(description="xxx爬虫")

#     parser.add_argument(
#         "--crawl_xxx", action="store_true", help="xxx爬虫", function=crawl_xxx
#     )
#     parser.add_argument(
#         "--crawl_xxx", action="store_true", help="xxx爬虫", function=crawl_xxx
#     )
#     parser.add_argument(
#         "--crawl_xxx",
#         type=int,
#         nargs=1,
#         help="xxx爬虫",
#         choices=[1, 2, 3],
#         function=crawl_xxx,
#     )

#     parser.start()

    # main.py作为爬虫启动的统一入口，提供命令行的方式启动多个爬虫，若只有一个爬虫，可不编写main.py
    # 将上面的xxx修改为自己实际的爬虫名
    # 查看运行命令 python main.py --help
    # AirSpider与Spider爬虫运行方式 python main.py --crawl_xxx
    # BatchSpider运行方式
    # 1. 下发任务：python main.py --crawl_xxx 1
    # 2. 采集：python main.py --crawl_xxx 2
    # 3. 重置任务：python main.py --crawl_xxx 3

