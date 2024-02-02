# -*- coding: utf-8 -*-
"""
Created on 2023-12-12 14:35:16
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *


def about_crawl_youtube_artist_channel_page_info_spider(args):
    """
    1-Youtube Music Web页面歌手页面信息采集
    """
    spider = crawl_youtube_artist_channel_page_info_spider.CrawlYoutubeArtistChannelPageInfoSpider(
        task_table="youtube_music_channel_id_batch_task",  # mysql中的任务表
        batch_record_table="record_youtube_music_channel_id_batch_task",  # mysql中的批次记录表
        batch_name="1-Youtube Music Web页面歌手页面信息采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","gmg_artist_name","youtube_music_channel_id","youtube_music_channel_name"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_youtube_music_channel_id_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_page_albums_singles_info_spider(args):
    """
    2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接
    """
    spider = crawl_youtube_page_albums_singles_info_spider.CrawlYoutubePageAlbumsSinglesInfoSpider(
        task_table="youtube_music_albums_singles_task",  # mysql中的任务表
        batch_record_table="record_youtube_music_albums_singles_task",  # mysql中的批次记录表
        batch_name="2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_albums_singles_id","youtube_music_albums_singles_url"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_page_albums_singles_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()



if __name__ == "__main__":
    parser = ArgumentParser(description="Youtube Music Web爬虫")

    parser.add_argument(
        "--about_crawl_youtube_artist_channel_page_info_spider",
        type=int,
        nargs=1,
        help="1-Youtube Music Web页面歌手页面信息采集",
        choices=[1, 2, 3],
        function=about_crawl_youtube_artist_channel_page_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_page_albums_singles_info_spider",
        type=int,
        nargs=1,
        help="2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_albums_singles_info_spider,
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

