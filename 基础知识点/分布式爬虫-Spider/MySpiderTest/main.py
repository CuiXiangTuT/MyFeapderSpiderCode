# -*- coding: utf-8 -*-
"""
Created on 2023-01-17 16:29:18
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import my_baidu_news_test,my_wangyi_news_test


def crawl_baidu_news():
    """
    Spider爬虫,百度新闻
    """
    spider = my_baidu_news_test.MyBaiduNewsTest(redis_key="feapder:spider_baidu_news_test")
    spider.start()

def crawl_wangyi_news():
    """
    Spider爬虫,网易新闻
    """
    spider = my_wangyi_news_test.MyWangyiNewsTest(redis_key="feapder:spider_wangyi_news_test")
    spider.start()



if __name__ == "__main__":
    parser = ArgumentParser(description="xxx爬虫")

    parser.add_argument(
        "--crawl_baidu_news",action="store_true", help="spider-百度新闻爬虫", function=crawl_baidu_news
    )
    parser.add_argument(
        "--crawl_wangyi_news",action="store_true",  help="spider-网易新闻爬虫", function=crawl_wangyi_news
    )

    parser.start()

    # main.py作为爬虫启动的统一入口，提供命令行的方式启动多个爬虫，若只有一个爬虫，可不编写main.py
    # 将上面的xxx修改为自己实际的爬虫名
    # 查看运行命令 python main.py --help
    # AirSpider与Spider爬虫运行方式 python main.py --crawl_xxx
    # BatchSpider运行方式
    # 1. 下发任务：python main.py --crawl_xxx 1
    # 2. 采集：python main.py --crawl_xxx 2
    # 3. 重置任务：python main.py --crawl_xxx 3

