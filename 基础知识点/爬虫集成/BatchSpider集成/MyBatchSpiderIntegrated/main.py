# -*- coding: utf-8 -*-
"""
Created on 2023-01-19 12:01:37
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *
from feapder import BatchSpider


def crawl_news(args):
    """
    BatchSpider爬虫
    """
    spider = BatchSpider(
        task_table="my_batch_spider_integrated_task_test",  # mysql中的任务表
        batch_record_table="my_batch_spider_integrated_task_test_record",  # mysql中的批次记录表
        batch_name="爬虫集成-BatchSpider",  # 批次名字
        batch_interval=7,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "url","parser_name"],  # # 集成批次爬虫，需要将批次爬虫的名字取出来，任务分发时才知道分发到哪个模板上
        redis_key="feapder:my_batch_spider_integrated_task_test",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    # 集成
    spider.add_parser(my_batch_spider_baidu_news_parser_test.MyBatchSpiderBaiduNewsParserTest)
    spider.add_parser(my_batch_spider_wangyi_news_parser_test.MyBatchSpiderWangyiNewsParserTest)

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="爬虫集成批次测试")
    parser.add_argument(
        "--crawl_news",
        type=int,
        nargs=1,
        help="批次爬虫测试",
        choices=[1, 2, 3],
        function=crawl_news,
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

