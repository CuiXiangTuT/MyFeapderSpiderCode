# -*- coding: utf-8 -*-
"""
Created on 2023-10-07 10:25:20
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
@description: 主要涉及Instagram相关程序的采集
"""

from feapder import ArgumentParser

from spiders import *


def about_crawl_instagram_artist_info_spider(args):
    """
    1-Instagram艺人粉丝数获取相关信息
    """
    spider = crawl_instagram_artist_info_spider.CrawInstagramArtistInfoSpider(
        task_table="instagram_artist_info_batch_task",  # mysql中的任务表
        batch_record_table="instagram_artist_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Instagram艺人粉丝数获取相关信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "instagram_artist_url","instagram_artist_name"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:instagram_artist_info_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="Instagram爬虫")

    parser.add_argument(
        "--about_crawl_instagram_artist_info_spider",
        type=int,
        nargs=1,
        help="Instagram艺人粉丝数获取相关信息",
        choices=[1, 2, 3],
        function=about_crawl_instagram_artist_info_spider,
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

