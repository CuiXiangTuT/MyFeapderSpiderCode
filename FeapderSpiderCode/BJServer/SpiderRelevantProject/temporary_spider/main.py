# -*- coding: utf-8 -*-
"""
Created on 2023-05-09 15:10:41
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *


def crawl_boomplay_chart_data_daily_spider(args):
    """
    1-Boomplay榜单页数据采集爬虫
    """
    spider = boomplay_chart_data_daily_spider.BoomplayChartDataDailySpider(
        task_table="chart_boomplay_batch_task",  # mysql中的任务表
        batch_record_table="chart_boomplay_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay榜单页数据采集爬虫",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=[
            "id", "region_en_abbreviation", "chart_region",
            "crawl_chart_country", "chart_site", "chart_type",
            "update_frequency", "chart_language", "chart_segment",
            "front-end web"
        ],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:bj_chart_boomplay_batch_task",  # redis中存放request等信息的根key
        task_state="bj_state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()


def crawl_boomplay_artist_info_spider(args):
    """
    2-Boomplay歌手详情页信息采集
    """
    spider = boomplay_artist_info_spider.BoomplayArtistInfoSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_artist_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌手详情页信息采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=[
            "id", "gmg_artist_id", "gmg_artist_name", "boomplay_artist_id",
            "boomplay_artist_name"
        ],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_artist_info_batch_task",  # redis中存放request等信息的根key
        task_state="bj_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_artist_info_task_spider(args):
    """
    3-Boomplay歌手详情页歌曲、专辑任务采集
    """
    spider = boomplay_artist_info_task_spider.BoomplayArtistInfoTaskSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_artist_album_track_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌手详情页歌曲、专辑任务采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "boomplay_artist_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_artist_album_track_task",  # redis中存放request等信息的根key
        task_state="bj_artist_album_track_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_album_info_task_spider(args):
    """
    4-Boomplay专辑详情页信息采集
    """
    spider = boomplay_album_info_spider.BoomplayAlbumInfoSpider(
        task_table="boomplay_album_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_album_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay专辑详情页信息采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "album_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_album_info_batch_task",  # redis中存放request等信息的根key
        task_state="bj_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_track_info_task_spider(args):
    """
    5-Boomplay歌曲详情页信息采集
    """
    spider = boomplay_track_info_spider.BoomplayTrackInfoSpider(
        task_table="boomplay_track_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_track_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌曲详情页信息采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "track_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_track_info_batch_task",  # redis中存放request等信息的根key
        task_state="bj_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_track_views_task_spider(args):
    """
    6-Boomplay歌曲播放量信息采集
    """
    spider = boomplay_track_views_spider.BoomplayTrackViewsSpider(
        task_table="boomplay_track_info_batch_task",  # mysql中的任务表
        batch_record_table="boomplay_track_views_spider_record",  # mysql中的批次记录表
        batch_name="Boomplay歌曲播放量信息采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "track_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_track_views_batch_task",  # redis中存放request等信息的根key
        task_state="bj_views_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="Boomplay相关爬虫")

    # 1-Boomplay榜单页数据采集爬虫：crawl_boomplay_chart_data_daily_spider
    parser.add_argument(
        "--crawl_boomplay_chart_data_daily_spider",
        type=int,
        nargs=1,
        help="Boomplay榜单页数据采集爬虫",
        choices=[1, 2, 3],
        function=crawl_boomplay_chart_data_daily_spider,
    )

    # 2-Boomplay歌手详情页信息采集
    parser.add_argument(
        "--crawl_boomplay_artist_info_spider",
        type=int,
        nargs=1,
        help="Boomplay歌手详情页信息采集",
        choices=[1, 2, 3],
        function=crawl_boomplay_artist_info_spider,
    )

    # 3-Boomplay歌手详情页歌曲、专辑任务采集
    parser.add_argument(
        "--crawl_boomplay_artist_info_task_spider",
        type=int,
        nargs=1,
        help="Boomplay歌手详情页歌曲、专辑任务采集",
        choices=[1, 2, 3],
        function=crawl_boomplay_artist_info_task_spider,
    )

    # 4-Boomplay专辑详情页信息采集
    parser.add_argument(
        "--crawl_boomplay_album_info_task_spider",
        type=int,
        nargs=1,
        help="Boomplay专辑详情页信息采集",
        choices=[1, 2, 3],
        function=crawl_boomplay_album_info_task_spider,
    )

    # 5-Boomplay歌曲详情页信息采集
    parser.add_argument(
        "--crawl_boomplay_track_info_task_spider",
        type=int,
        nargs=1,
        help="Boomplay歌手详情页歌曲、专辑任务采集",
        choices=[1, 2, 3],
        function=crawl_boomplay_track_info_task_spider,
    )

    # 6-Boomplay歌曲播放量信息采集
    parser.add_argument(
        "--crawl_boomplay_track_views_task_spider",
        type=int,
        nargs=1,
        help="Boomplay歌曲播放量信息采集",
        choices=[1, 2, 3],
        function=crawl_boomplay_track_views_task_spider,
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
