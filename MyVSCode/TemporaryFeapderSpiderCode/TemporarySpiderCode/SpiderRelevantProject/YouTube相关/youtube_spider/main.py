# -*- coding: utf-8 -*-
"""
Created on 2023-09-06 19:28:59
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *



def about_crawl_youtube_link_get_channel_id_spider(args):
    """
    1-Youtube通过给予的YouTubeLink抓取其对应的YouTube Channel Id
    """
    spider = crawl_youtube_link_get_channel_id_spider.CrawlYoutubeLinkGetChannelIdSpider(
        task_table="youtube_link_get_channel_id_task",  # mysql中的任务表
        batch_record_table="youtube_link_get_channel_id_task_record",  # mysql中的批次记录表
        batch_name="Youtube通过给予的YouTubeLink抓取其对应的YouTube Channel Id",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "youtube_link"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:youtube_link_get_channel_id_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_link_info_spider(args):
    """
    2-通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views
    """
    spider = crawl_youtube_link_info_spider.CrawlYoutubeLinkInfoSpider(
        task_table="youtube_video_link_info_batch_task",  # mysql中的任务表
        batch_record_table="youtube_video_link_info_batch_task_record",  # mysql中的批次记录表
        batch_name="通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "youtube_video_link"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:youtube_video_link_info_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_music_playlist_detail_info_spider(args):
    """
    3-通过YouTube Music Playlist Link获取其下所有的歌曲id即YouTube Video Id
    """
    spider = crawl_youtube_music_playlist_detail_info_spider.CrawlYoutubeMusicPlaylistDetailInfoSpider(
        task_table="youtube_music_playlist_batch_task",  # mysql中的任务表
        batch_record_table="youtube_music_playlist_batch_task_record",  # mysql中的批次记录表
        batch_name="通过YouTube Music Playlist Link获取其下所有的歌曲id即YouTube Video Id",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "youtube_music_playlist_link"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:youtube_music_playlist_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="xxx爬虫")

    """
    1-Youtube通过给予的YouTubeLink抓取其对应的YouTube Channel Id
    """
    parser.add_argument(
        "--about_crawl_youtube_link_get_channel_id_spider",
        type=int,
        nargs=1,
        help="Youtube通过给予的YouTubeLink抓取其对应的YouTube Channel Id",
        choices=[1, 2, 3],
        function=about_crawl_youtube_link_get_channel_id_spider,
    )

    """
        2-通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views
    """
    parser.add_argument(
        "--about_crawl_youtube_link_info_spider",
        type=int,
        nargs=1,
        help="通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views",
        choices=[1, 2, 3],
        function=about_crawl_youtube_link_info_spider,
    )

    """
        3-通过YouTube Music Playlist Link获取其下所有的歌曲id即YouTube Video Id
    """
    parser.add_argument(
        "--about_crawl_youtube_music_playlist_detail_info_spider",
        type=int,
        nargs=1,
        help="通过YouTube Music Playlist Link获取其下所有的歌曲id即YouTube Video Id",
        choices=[1, 2, 3],
        function=about_crawl_youtube_music_playlist_detail_info_spider,
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

