# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 10:53:40
---------
@summary: 爬虫入口
---------
@author: QiuQiuRen
"""

from feapder import ArgumentParser

from spiders import *

def about_crawl_boomplay_chart_data_daily_spider(args):
    """
    1-Boomplay每日榜单数据
    """
    spider = crawl_boomplay_chart_data_daily_spider.CrawlBoomplayChartDataDailySpider(
        task_table="chart_boomplay_batch_task",  # mysql中的任务表
        batch_record_table="record_crawl_boomplay_chart_data_daily_spider",  # mysql中的批次记录表
        batch_name="1-Boomplay每日榜单数据",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "region_en_abbreviation", "chart_region",
            "crawl_chart_country", "chart_site", "chart_type",
            "update_frequency", "chart_language", "chart_segment",
            "front-end web"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_chart_data_daily_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_boomplay_artist_info_spider(args):
    """
    2-Boomplay歌手信息采集
    """
    spider = crawl_boomplay_artist_info_spider.CrawlBoomplayArtistInfoSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table="record_boomplay_artist_info_batch_task",  # mysql中的批次记录表
        batch_name="2-Boomplay歌手信息采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id", "gmg_artist_name", "boomplay_artist_id", "boomplay_artist_name"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_artist_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_boomplay_artist_songs_albums_playlists_counts_spider(args):
    """
    3-Boomplay歌手歌曲、专辑、播放列表 条目数 采集
    """
    spider = crawl_boomplay_artist_songs_albums_playlists_counts_spider.CrawlBoomplayArtistSongsAlbumsPlaylistsCountsSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table="record_boomplay_artists_sap_counts_batch",  # mysql中的批次记录表
        batch_name="3-Boomplay歌手歌曲、专辑、播放列表 条目数 采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "boomplay_artist_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_artist_songs_albums_playlists_counts_spider",  # redis中存放request等信息的根key
        task_state="bj_crawl_songs_albums_playlists_count_state",  # mysql中任务状态字段
        task_condition="bj_crawl_songs_albums_playlists_count_state=0"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()


def about_crawl_boomplay_artist_songs_albums_playlists_task_spider(args):
    """
    4-Boomplay歌手歌曲id、专辑id、播放列表id 及 相关映射 采集
    """
    spider = crawl_boomplay_artist_songs_albums_playlists_task_spider.CrawlBoomplayArtistAlbumTrackInfoTaskSpider(
        task_table="boomplay_artist_info_batch_task",  # mysql中的任务表
        batch_record_table="record_boomplay_artist_songs_albums_playlists_task_batch",  # mysql中的批次记录表
        batch_name="4-Boomplay歌手歌曲id、专辑id、播放列表id 及 相关映射 采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "boomplay_artist_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_artist_songs_albums_playlists_task_spider",  # redis中存放request等信息的根key
        task_state="bj_crawl_artist_album_track_playlist_task_state",  # mysql中任务状态字段
        task_condition="bj_crawl_artist_album_track_playlist_task_state=0"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()

def about_crawl_boomplay_album_info_spider(args):
    """
    5-Boomplay专辑信息及专辑歌曲映射、专辑下歌曲任务采集
    """
    spider = crawl_boomplay_album_info_spider.CrawlBoomplayAlbumInfoSpider(
        task_table="boomplay_album_info_batch_task",  # mysql中的任务表
        batch_record_table="record_boomplay_album_info_batch_task_batch",  # mysql中的批次记录表
        batch_name="5-Boomplay专辑信息及专辑歌曲映射、专辑下歌曲任务采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "album_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_album_info_spider",  # redis中存放request等信息的根key
        task_state="bj_state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()


def about_crawl_boomplay_track_info_spider(args):
    """
    6-Boomplay歌曲信息采集
    """
    spider = crawl_boomplay_track_info_spider.CrawlBoomplayTrackInfoSpider(
        task_table="boomplay_track_info_batch_task",  # mysql中的任务表
        batch_record_table="record_boomplay_track_info_batch_task",  # mysql中的批次记录表
        batch_name="6-Boomplay歌曲信息采集  ",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id",'track_id'],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_track_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )
    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.my_init_task()

def about_crawl_boomplay_track_views_spider(args):
    """
    7-Boomplay批次播放量采集
    """
    spider = crawl_boomplay_track_views_spider.CrawlBoomplayTrackViewsSpider(
        task_table="boomplay_track_info_batch_task",  # mysql中的任务表
        batch_record_table="record_boomplay_track_info_batch_task",  # mysql中的批次记录表
        batch_name="8-Boomplay批次播放量采集",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id","track_id"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="feapder:crawl_boomplay_track_views_spider",  # redis中存放request等信息的根key
        task_state="views_state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()



if __name__ == "__main__":
    parser = ArgumentParser(description="Boomplay相关爬虫")

    # 1-Boomplay每日榜单数据
    parser.add_argument(
        "--about_crawl_boomplay_chart_data_daily_spider",
        type=int,
        nargs=1,
        help="1-Boomplay每日榜单数据",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_chart_data_daily_spider,
    )

    # 2-Boomplay歌手信息采集
    parser.add_argument(
        "--about_crawl_boomplay_artist_info_spider",
        type=int,
        nargs=1,
        help="2-Boomplay歌手信息采集",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_artist_info_spider,
    )

    # 3-Boomplay歌手歌曲、专辑、播放列表 条目数 采集
    parser.add_argument(
        "--about_crawl_boomplay_artist_songs_albums_playlists_counts_spider",
        type=int,
        nargs=1,
        help="3-Boomplay歌手歌曲、专辑、播放列表 条目数 采集",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_artist_songs_albums_playlists_counts_spider,
    )

    # 4-Boomplay歌手歌曲id、专辑id、播放列表id 及 相关映射 采集
    parser.add_argument(
        "--about_crawl_boomplay_artist_songs_albums_playlists_task_spider",
        type=int,
        nargs=1,
        help="4-Boomplay歌手歌曲id、专辑id、播放列表id 及 相关映射 采集",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_artist_songs_albums_playlists_task_spider,
    )

    # 5-Boomplay专辑信息及专辑歌曲映射、专辑下歌曲任务采集
    parser.add_argument(
        "--about_crawl_boomplay_album_info_spider",
        type=int,
        nargs=1,
        help="5-Boomplay专辑信息及专辑歌曲映射、专辑下歌曲任务采集",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_album_info_spider,
    )

    # 6-Boomplay歌曲信息采集
    parser.add_argument(
        "--about_crawl_boomplay_track_info_spider",
        type=int,
        nargs=1,
        help="6-Boomplay歌曲信息采集",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_track_info_spider,
    )

    # 7-Boomplay批次播放量采集
    parser.add_argument(
        "--about_crawl_boomplay_track_views_spider",
        type=int,
        nargs=1,
        help="7-Boomplay批次播放量采集",
        choices=[1, 2, 3],
        function=about_crawl_boomplay_track_views_spider,
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

