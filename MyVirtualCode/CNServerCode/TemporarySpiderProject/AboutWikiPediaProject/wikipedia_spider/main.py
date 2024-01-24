# -*- coding: utf-8 -*-
"""
Created on 2023-12-12 17:38:40
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *

def about_crawl_wikipedia_artist_info_spider(args):
    """
    1-维基百科查询艺人信息
    """
    spider = crawl_wikipedia_artist_info_spider.CrawlWikipediaArtistInfoSpider(
        task_table="wikipedia_artist_batch_task",  # mysql中的任务表
        batch_record_table="record_wikipedia_artist_batch_task",  # mysql中的批次记录表
        batch_name="维基百科查询艺人信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","gmg_artist_name","artist_id","artist_name"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder_temporary_wikipedia_data:about_crawl_wikipedia_artist_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_wikipedia_spotify_artist_info_spider(args):
    """
    2-维基百科查询艺人信息
    """
    spider = crawl_wikipedia_artist_info_spider.CrawlWikipediaArtistInfoSpider(
        task_table="wikipedia_spotify_artist_batch_task",  # mysql中的任务表
        batch_record_table="record_wikipedia_spotify_artist_batch_task",  # mysql中的批次记录表
        batch_name="维基百科查询艺人信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","gmg_artist_name","artist_id","artist_name","spotify_wikipedia_url"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder_temporary_wikipedia_data:about_crawl_wikipedia_spotify_artist_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="维基百科爬虫")

    parser.add_argument(
        "--about_crawl_wikipedia_artist_info_spider",
        type=int,
        nargs=1,
        help="1-维基百科查询艺人信息",
        choices=[1, 2, 3],
        function=about_crawl_wikipedia_artist_info_spider,
    )

    parser.add_argument(
        "--about_crawl_wikipedia_spotify_artist_info_spider",
        type=int,
        nargs=1,
        help="2-维基百科查询艺人信息",
        choices=[1, 2, 3],
        function=about_crawl_wikipedia_spotify_artist_info_spider,
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

