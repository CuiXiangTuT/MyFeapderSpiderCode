# -*- coding: utf-8 -*-
"""
Created on 2023-09-27 14:34:44
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *


def about_crawl_youtube_artist_playlist_info_spider(args):
    """
    1-通过YouTube前端页面获取到艺人Channel Id，经YouTube API获取其对应的播放列表YouTube Playlist Id
    :param args:
    :return:
    """
    spider = crawl_youtube_artist_playlist_info_spider.CrawlYoutubeArtistPlaylistInfoSpider(
        task_table="api_youtube_artist_channel_id_batch_task",  # mysql中的任务表
        batch_record_table="api_youtube_artist_channel_id_batch_task_record",  # mysql中的批次记录表
        batch_name="1-通过YouTube前端页面获取到艺人Channel Id，经YouTube API获取其对应的播放列表YouTube Playlist Id",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id",'youtube_artist_channel_id'],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:api_youtube_artist_channel_id_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()

def about_crawl_youtube_playlist_video_info_spider(args):
    """
    2-通过YouTube API获取Playlist下的信息，主要涉及获取Video Id
    """
    spider = crawl_youtube_playlist_video_info_spider.CrawlYoutubePlaylistVideoInfoSpider(
        task_table="api_youtube_artist_playlist_batch_task",  # mysql中的任务表
        batch_record_table="api_youtube_artist_playlist_batch_task_record",  # mysql中的批次记录表
        batch_name="2-通过YouTube API获取Playlist下的信息，主要涉及获取Video Id",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id",'youtube_playlist_id'],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:api_youtube_artist_playlist_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()

def about_crawl_youtube_video_info_spider(args):
    """
    3-通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息
    :param args:
    :return:
    """
    spider = crawl_youtube_video_info_spider.CrawlYoutubeVideoInfoSpider(
        task_table="api_youtube_video_batch_task",  # mysql中的任务表
        batch_record_table="api_youtube_video_batch_task_record",  # mysql中的批次记录表
        batch_name="3-通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", 'youtube_video_id'],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:api_youtube_video_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()

def about_crawl_api_youtube_video_info_spider(args):
    """
    4-通过Youtube Video Link，经Youtube API获取其信息
    :param args:
    :return:
    """
    spider = crawl_api_youtube_video_info_spider.CrawlApiYoutubeVideoInfoSpider(
        task_table="temporary_crawl_api_youtube_video_info_batch_task",  # mysql中的任务表
        batch_record_table="temporary_crawl_api_youtube_video_info_batch_task_record",  # mysql中的批次记录表
        batch_name="4-通过Youtube Video Link，经Youtube API获取其信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", 'youtube_video_link'],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:temporary_crawl_api_youtube_video_info_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()


# 临时任务时使用，临时任务表：temporary_api_youtube_video_batch_task
def temporary_about_crawl_youtube_video_info_spider(args):
    """
    5-临时任务：通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息
    :param args:
    :return:
    """
    spider = crawl_youtube_video_info_spider.CrawlYoutubeVideoInfoSpider(
        task_table="temporary_api_youtube_video_batch_task",  # mysql中的任务表
        batch_record_table="temporary_api_youtube_video_batch_task_record",  # mysql中的批次记录表
        batch_name="5-临时任务：通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", 'youtube_video_id'],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:temporary_api_youtube_video_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()


def about_crawl_youtube_link_info_spider(args):
    """
    6-通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views
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


if __name__ == "__main__":
    parser = ArgumentParser(description="YouTube相关爬虫")

    # 1-通过YouTube前端页面获取到艺人Channel Id，经YouTube API获取其对应的播放列表YouTube Playlist Id
    parser.add_argument(
        "--about_crawl_youtube_artist_playlist_info_spider",
        type=int,
        nargs=1,
        help="1-通过YouTube前端页面获取到艺人Channel Id，经YouTube API获取其对应的播放列表YouTube Playlist Id",
        choices=[1, 2, 3],
        function=about_crawl_youtube_artist_playlist_info_spider,
    )


    # 2-通过YouTube API获取Playlist下的信息，主要涉及获取Video Id
    parser.add_argument(
        "--about_crawl_youtube_playlist_video_info_spider",
        type=int,
        nargs=1,
        help="2-通过YouTube API获取Playlist下的信息，主要涉及获取Video Id",
        choices=[1, 2, 3],
        function=about_crawl_youtube_playlist_video_info_spider,
    )

    # 3-通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息
    parser.add_argument(
        "--about_crawl_youtube_video_info_spider",
        type=int,
        nargs=1,
        help="3-通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_video_info_spider,
    )

    # 4-通过Youtube Video Link，经Youtube API获取其信息
    parser.add_argument(
        "--about_crawl_api_youtube_video_info_spider",
        type=int,
        nargs=1,
        help="4-通过Youtube Video Link，经Youtube API获取其信息",
        choices=[1, 2, 3],
        function=about_crawl_api_youtube_video_info_spider,
    )

    # 5-临时任务：通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息
    parser.add_argument(
        "--temporary_about_crawl_youtube_video_info_spider",
        type=int,
        nargs=1,
        help="5-临时任务：通过YouTube API获取到YouTube Video Id，经前端Web页面采集，获取其播放量及点赞量信息",
        choices=[1, 2, 3],
        function=temporary_about_crawl_youtube_video_info_spider,
    )

    # 6-通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views
    parser.add_argument(
        "--about_crawl_youtube_link_info_spider",
        type=int,
        nargs=1,
        help="6-通过给予的YouTube Video Link 抓取相对应的页面Title、Channel Id、Channel Name、Views",
        choices=[1, 2, 3],
        function=about_crawl_youtube_link_info_spider,
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

