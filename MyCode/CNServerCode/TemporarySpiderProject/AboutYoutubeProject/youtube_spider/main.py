# -*- coding: utf-8 -*-
"""
Created on 2023-12-01 14:48:46
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *


def about_crawl_search_youtube_info_spider(args):
    """
    1.根据提供的artist_name和track_name，查找相关的youtube信息
    """
    spider = crawl_search_youtube_info_spider.CrawlSearchYoutubeInfoSpider(
        task_table="temporary_search_youtube_info_batch_task",  # mysql中的任务表
        batch_record_table="record_temporary_search_youtube_info_batch_task",  # mysql中的批次记录表
        batch_name="1.根据提供的artist_name和track_name，查找相关的youtube信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "artist_id","track_id","artist_name","track_name"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_youtube_data:temporary_search_youtube_info_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="临时Youtube爬虫")

    # 1.根据提供的artist_name和track_name，查找相关的youtube信息
    parser.add_argument(
        "--about_crawl_search_youtube_info_spider",
        type=int,
        nargs=1,
        help="1.根据提供的artist_name和track_name，查找相关的youtube信息",
        choices=[1, 2, 3],
        function=about_crawl_search_youtube_info_spider,
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

