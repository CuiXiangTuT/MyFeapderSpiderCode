# -*- coding: utf-8 -*-
"""
Created on 2023-01-18 15:38:28
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *



def crawl_baidu_news(args):
    """
    BatchSpider爬虫
    """
    spider = batch_spider_test.BatchSpiderTest(
        redis_key="feapder:my_batch_spider_task_test",  # 分布式爬虫调度信息存储位置
        task_table="my_batch_spider_task_test",  # mysql中的任务表
        task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="my_batch_spider_task_test_batch_record",  # mysql中的批次记录表
        batch_name="百度新闻采集",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )


    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="百度新闻采集爬虫")

    parser.add_argument(
        "--crawl_baidu_news",
        type=int,
        nargs=1,
        help="百度新闻采集爬虫",
        choices=[1, 2, 3],
        function=crawl_baidu_news,
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

