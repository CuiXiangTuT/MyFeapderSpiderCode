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
        redis_key="temporary_feapder:crawl_youtube_artist_channel_page_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_artist_channel_page_info_new_spider(args):
    """
    1-A-Youtube Music Web页面歌手页面信息采集
    """
    spider = crawl_youtube_artist_channel_page_info_new_spider.CrawlYoutubeArtistChannelPageInfoNewSpider(
        task_table="youtube_music_channel_id_batch_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_artist_channel_page_info_new_spider",  # mysql中的批次记录表
        batch_name="1-Youtube Music Web页面歌手页面信息采集（最新）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","gmg_artist_name","youtube_music_channel_id","youtube_music_channel_name"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_artist_channel_page_info_new_spider",  # redis中存放request等信息的根key
        task_state="new_state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

# def about_crawl_youtube_page_albums_singles_info_spider(args):
#     """
#     2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接（未二次跳转前）
#     """
#     spider = crawl_youtube_page_albums_singles_info_spider.CrawlYoutubePageAlbumsSinglesInfoSpider(
#         task_table="youtube_music_playlist_task",  # mysql中的任务表
#         batch_record_table="record_youtube_music_playlist_task",  # mysql中的批次记录表
#         batch_name="2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接（未二次跳转前）",  # 批次名字
#         batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
#         task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
#         redis_key="temporary_feapder:about_crawl_youtube_page_albums_singles_info_spider",  # redis中存放request等信息的根key
#         task_state="state",  # mysql中任务状态字段
#     )
#
#     if args == 1:
#         spider.start_monitor_task()
#     elif args == 2:
#         spider.start()
#     elif args == 3:
#         spider.init_task()

def about_crawl_youtube_page_albums_singles_info_new_spider(args):
    """
    2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接（未二次跳转前）
    """
    spider = crawl_youtube_page_albums_singles_info_new_spider.CrawlYoutubePageAlbumsSinglesInfoNewSpider(
        task_table="youtube_music_playlist_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_page_albums_singls_info_new_spider",  # mysql中的批次记录表
        batch_name="2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接（未二次跳转前）",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_page_albums_singls_info_new_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_youtube_playlist_url_redirect_spider(args):
    """
    3-对获取的【专辑、单曲】链接进行二次重定向
    """
    spider = crawl_youtube_playlist_url_redirect_spider.CrawlYoutubePlaylistUrlRedirectSpider(
        task_table="youtube_music_plate_url_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_playlist_url_redirect_spider",  # mysql中的批次记录表
        batch_name="3-对获取的【专辑、单曲】链接进行二次重定向",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark",'youtube_music_playlist_url_pre_redirect','title'],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_playlist_url_redirect_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_page_songs_info_spider(args):
    """
    4-采集Youtube【歌曲】下的所有歌曲信息
    """
    spider = crawl_youtube_page_songs_info_spider.CrawlPageSongsInfoSpider(
        task_table="youtube_music_artist_plate_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_page_songs_info_spider",  # mysql中的批次记录表
        batch_name="4-采集Youtube【歌曲】下的所有歌曲信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_page_songs_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='Songs'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_youtube_page_songs_info_new_spider(args):
    """
    4-A-采集Youtube【歌曲】下的所有歌曲信息
    """
    spider = crawl_youtube_page_songs_info_new_spider.CrawlYoutubePageSongsInfoNewSpider(
        task_table="youtube_music_artist_plate_task",  # mysql中的任务表
        batch_record_table="record_about_crawl_youtube_page_songs_info_new_spider",  # mysql中的批次记录表
        batch_name="4-A-采集Youtube【歌曲】下的所有歌曲信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_page_songs_info_new_spider",  # redis中存放request等信息的根key
        task_state="state_new",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='Songs'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()



def about_crawl_youtube_page_videos_spider(args):
    """
    5-采集Youtube【视频】下的所有歌曲信息
    """
    spider = crawl_youtube_page_videos_spider.CrawlPageVideosSpider(
        task_table="youtube_music_artist_plate_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_page_videos_spider",  # mysql中的批次记录表
        batch_name="5-采集Youtube【视频】下的所有歌曲信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_page_videos_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='Videos'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_youtube_page_videos_info_new_spider(args):
    """
    5-A-采集Youtube【视频】下的所有歌曲信息
    """
    spider = crawl_youtube_page_videos_info_new_spider.CrawlYoutubePageVideosInfoNewSpider(
        task_table="youtube_music_artist_plate_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_page_videos_info_new_spider",  # mysql中的批次记录表
        batch_name="5-A-采集Youtube【视频】下的所有歌曲信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_page_videos_info_new_spider",  # redis中存放request等信息的根key
        task_state="state_new",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='Videos'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_page_playlist_info_spider(args):
    """
    6-采集Youtube【专辑-单曲】下的所有歌曲信息
    """
    spider = crawl_youtube_page_playlist_info_spider.CrawlYoutubePagePlaylistInfoSpider(
        task_table="youtube_music_artist_plate_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_page_playlist_info_spider",  # mysql中的批次记录表
        batch_name="6-采集Youtube【专辑-单曲】下的所有歌曲信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:crawl_youtube_page_playlist_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='Albums/Singles'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_youtube_page_featured_on_info_spider(args):
    """
    7-采集歌手Feature On 中的信息
    """
    spider = crawl_youtube_page_featured_on_info_spider.CrawlYoutubePageFeaturedOnInfoSpider(
        task_table="youtube_music_artist_plate_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_page_featured_on_info_spider",  # mysql中的批次记录表
        batch_name="9-采集歌手Feature On 中的信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_playlist_url","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_page_featured_on_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='Featured on'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()



def about_crawl_youtube_video_views_info_spider(args):
    """
    8-采集Youtube Music 歌曲播放量信息
    """
    spider = crawl_youtube_video_views_info_spider.CrawlYoutubeVideoViewsInfoSpider(
        task_table="youtube_music_video_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_video_views_info_spider",  # mysql中的批次记录表
        batch_name="7-采集Youtube Music 歌曲播放量信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_video_id","youtube_music_video_url","youtube_music_source_remark","youtube_music_source_playlist_url"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_video_views_info_spider",  # redis中存放request等信息的根key
        task_state="view_state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


def about_crawl_youtube_video_artist_info_spider(args):
    """
    9-采集Youtube Music 歌曲的歌手信息
    """
    spider = crawl_youtube_video_artist_info_spider.CrawlYoutubeVideoArtistInfoSpider(
        task_table="youtube_music_video_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_video_artist_info_spider",  # mysql中的批次记录表
        batch_name="8-采集Youtube Music 歌曲的歌手信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_video_id","youtube_music_video_url","youtube_music_source_remark","youtube_music_source_playlist_url"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_video_artist_info_spider",  # redis中存放request等信息的根key
        task_state="artist_state",  # mysql中任务状态字段
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()



def about_crawl_youtube_api_playlist_info_spider(args):
    """
    X-采集API提供的Playlist下的所有video id 信息
    """
    spider = crawl_youtube_api_playlist_info_spider.CrawlYoutubeApiPlaylistInfoSpider(
        task_table="api_youtube_playlist_info_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_api_playlist_info_spider",  # mysql中的批次记录表
        batch_name="X-采集API提供的Playlist下的所有video id 信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_plate_remark"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_api_playlist_info_spider",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
        task_condition="youtube_music_plate_remark='test_album'"
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()

def about_crawl_youtube_api_video_info_spider(args):
    """
    Y-采集API提供的video id 信息
    """
    spider = crawl_youtube_api_video_info_spider.CrawlYoutubeApiVideoInfoSpider(
        task_table="api_youtube_video_info_task",  # mysql中的任务表
        batch_record_table="record_crawl_youtube_api_video_info_spider",  # mysql中的批次记录表
        batch_name="Y-采集API提供的video id 信息",  # 批次名字
        batch_interval=1,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "youtube_video_ids","youtube_video_ids_md5"],  # 需要获取任务表里的字段名，可添加多个
        redis_key="temporary_feapder:about_crawl_youtube_api_video_info_spider",  # redis中存放request等信息的根key
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

    # parser.add_argument(
    #     "--about_crawl_youtube_artist_channel_page_info_spider",
    #     type=int,
    #     nargs=1,
    #     help="1-Youtube Music Web页面歌手页面信息采集",
    #     choices=[1, 2, 3],
    #     function=about_crawl_youtube_artist_channel_page_info_spider,
    # )

    # about_crawl_youtube_artist_channel_page_info_new_spider
    parser.add_argument(
        "--about_crawl_youtube_artist_channel_page_info_new_spider",
        type=int,
        nargs=1,
        help="1-A-Youtube Music Web页面歌手页面信息采集（最新）",
        choices=[1, 2, 3],
        function=about_crawl_youtube_artist_channel_page_info_new_spider,
    )

    # parser.add_argument(
    #     "--about_crawl_youtube_page_albums_singles_info_spider",
    #     type=int,
    #     nargs=1,
    #     help="2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接（未二次跳转前）",
    #     choices=[1, 2, 3],
    #     function=about_crawl_youtube_page_albums_singles_info_spider,
    # )

    # about_crawl_youtube_page_albums_singls_info_new_spider
    parser.add_argument(
        "--about_crawl_youtube_page_albums_singles_info_new_spider",
        type=int,
        nargs=1,
        help="2-Youtube Music Web页面【专辑、单曲】下获取所有的【专辑、单曲】链接（未二次跳转前）",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_albums_singles_info_new_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_playlist_url_redirect_spider",
        type=int,
        nargs=1,
        help="3-对获取的【专辑、单曲】链接进行二次重定向",
        choices=[1, 2, 3],
        function=about_crawl_youtube_playlist_url_redirect_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_page_songs_info_spider",
        type=int,
        nargs=1,
        help="4-采集Youtube【歌曲】下的所有歌曲信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_songs_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_page_songs_info_new_spider",
        type=int,
        nargs=1,
        help="4-A-采集Youtube【歌曲】下的所有歌曲信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_songs_info_new_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_page_videos_spider",
        type=int,
        nargs=1,
        help="5-采集Youtube【视频】下的所有歌曲信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_videos_spider,
    )
    # about_crawl_youtube_page_videos_info_new_spider
    parser.add_argument(
        "--about_crawl_youtube_page_videos_info_new_spider",
        type=int,
        nargs=1,
        help="5-A-采集Youtube【视频】下的所有歌曲信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_videos_info_new_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_page_playlist_info_spider",
        type=int,
        nargs=1,
        help="6-采集Youtube【专辑-单曲】下的所有歌曲信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_playlist_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_page_featured_on_info_spider",
        type=int,
        nargs=1,
        help="7-采集歌手Feature On 中的信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_page_featured_on_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_video_views_info_spider",
        type=int,
        nargs=1,
        help="8-采集Youtube Music 歌曲播放量信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_video_views_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_video_artist_info_spider",
        type=int,
        nargs=1,
        help="9-采集Youtube Music 歌曲的歌手信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_video_artist_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_api_playlist_info_spider",
        type=int,
        nargs=1,
        help="X-采集API提供的Playlist下的所有video id 信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_api_playlist_info_spider,
    )

    parser.add_argument(
        "--about_crawl_youtube_api_video_info_spider",
        type=int,
        nargs=1,
        help="Y-采集API提供的video id 信息",
        choices=[1, 2, 3],
        function=about_crawl_youtube_api_video_info_spider,
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

