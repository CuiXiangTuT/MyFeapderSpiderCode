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


def crawl_boomplay_artist_info_spider(args):
    """
    1-Boomplay歌手详情页信息采集（北京采集）
    """
    spider = boomplay_artist_info_spider.BoomplayArtistInfoSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_artist_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌手详情页信息采集（北京采集）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=[
            "id", "gmg_artist_id", "gmg_artist_name", "boomplay_artist_id",
            "boomplay_artist_name"
        ],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_artist_info_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_artist_info_task_spider(args):
    """
    2-Boomplay歌手详情页歌曲、专辑任务采集（北京采集）
    """
    spider = boomplay_artist_info_task_spider.BoomplayArtistInfoTaskSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_artist_album_track_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌手详情页歌曲、专辑任务采集（北京采集）",  # 批次名字
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
    3-Boomplay专辑详情页（包含歌曲）信息采集（北京采集）
    """
    spider = boomplay_album_info_spider.BoomplayAlbumInfoSpider(
        task_table="boomplay_album_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_album_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay专辑详情页（包含歌曲）信息采集（北京采集）",  # 批次名字
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
    4-Boomplay歌曲详情页信息采集（北京采集）
    """
    spider = boomplay_track_info_spider.BoomplayTrackInfoSpider(
        task_table="boomplay_track_info_batch_task",  # mysql中的任务表
        batch_record_table=
        "boomplay_track_info_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌曲详情页信息采集（北京采集）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "track_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_track_info_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_track_views_task_spider(args):
    """
    5-Boomplay歌曲播放量信息采集（北京采集）
    """
    spider = boomplay_track_views_spider.BoomplayTrackViewsSpider(
        task_table="boomplay_track_info_batch_task",  # mysql中的任务表
        batch_record_table="boomplay_track_views_spider_record",  # mysql中的批次记录表
        batch_name="Boomplay歌曲播放量信息采集（北京采集）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "track_id","batch"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_track_views_batch_task",  # redis中存放request等信息的根key
        task_state="views_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()



def crawl_boomplay_artist_album_track_count_info_spider(args):
    """
    6-Boomplay歌手web页面歌曲及专辑数采集（北京采集）
    """
    spider = boomplay_artist_album_track_count_info_spider.BoomplayArtistAlbumTrackCountInfoSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table="boomplay_artist_album_track_count_record",  # mysql中的批次记录表
        batch_name="Boomplay歌手web页面歌曲及专辑数采集（北京采集）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "boomplay_artist_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_artist_album_track_count_record",  # redis中存放request等信息的根key
        task_state="bj_artist_album_track_count_state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def crawl_boomplay_track_views_task_failed_spider(args):
    """
    7-Boomplay歌曲播放量失败信息采集（北京采集）
    """
    spider = boomplay_track_views_spider.BoomplayTrackViewsSpider(
        task_table="boomplay_track_status_failed_batch_task",  # mysql中的任务表
        batch_record_table="boomplay_track_status_failed_batch_task_record",  # mysql中的批次记录表
        batch_name="Boomplay歌曲播放量失败信息采集（北京采集）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "track_id",'batch'],  # 需要获取任务表里的字段名，可添加多个
        redis_key=
        "feapder:bj_boomplay_track_status_failed_batch_task",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()

if __name__ == "__main__":
    parser = ArgumentParser(description="Boomplay相关爬虫")

    # 1-Boomplay歌手详情页信息采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_artist_info_spider",
        type=int,
        nargs=1,
        help="Boomplay歌手详情页信息采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_artist_info_spider,
    )

    # 2-Boomplay歌手详情页歌曲、专辑任务采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_artist_info_task_spider",
        type=int,
        nargs=1,
        help="Boomplay歌手详情页歌曲、专辑任务采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_artist_info_task_spider,
    )

    # 3-Boomplay专辑详情页（包含歌曲）信息采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_album_info_task_spider",
        type=int,
        nargs=1,
        help="Boomplay专辑详情页（包含歌曲）信息采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_album_info_task_spider,
    )

    # 4-Boomplay歌曲详情页信息采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_track_info_task_spider",
        type=int,
        nargs=1,
        help="Boomplay歌曲详情页信息采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_track_info_task_spider,
    )

    # 5-Boomplay歌曲播放量信息采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_track_views_task_spider",
        type=int,
        nargs=1,
        help="Boomplay歌曲播放量信息采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_track_views_task_spider,
    )

    # 6-Boomplay歌手web页面歌曲及专辑数采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_artist_album_track_count_info_spider",
        type=int,
        nargs=1,
        help="Boomplay歌手web页面歌曲及专辑数采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_artist_album_track_count_info_spider,
    )


    # 7-Boomplay歌曲播放量失败信息采集（北京采集）
    parser.add_argument(
        "--crawl_boomplay_track_views_task_failed_spider",
        type=int,
        nargs=1,
        help="Boomplay歌曲播放量失败信息采集（北京采集）",
        choices=[1, 2, 3],
        function=crawl_boomplay_track_views_task_failed_spider,
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
