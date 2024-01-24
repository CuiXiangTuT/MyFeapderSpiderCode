# -*- coding: utf-8 -*-
"""
Created on 2023-12-18 11:44:53
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import UpdateItem


class YoutubeMusicChannelIdBatchDataItem(UpdateItem):
    """
    1.说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_channel_id_batch_data

        用于存储歌手channel_id采集到的页面信息，
        主要字段包含以下，模块包括：页面【歌曲】、页面【专辑】、页面【单曲】、页面【视频】
    """

    __table_name__ = "youtube_music_channel_id_batch_data"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "batch"]
    __update_key__ = ["gmg_artist_id", "origin_views", "youtube_music_channel_id", "youtube_music_artist_name",
                      "youtube_music_artist_subscriber_count",
                      "youtube_music_artist_description", "youtube_music_artist_background_image_url", "views",
                      "youtube_music_all_songs_url", "youtube_music_all_albums_singles_url",
                      "youtube_music_all_videos_url", "batch", "youtube_music_all_songs_id",
                      "youtube_music_all_albums_singles_id",
                      "youtube_music_all_videos_id", "youtube_music_artist_channel_id", "gmg_artist_name",
                      "youtube_music_channel_name"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.gmg_artist_name = None
        self.youtube_music_channel_id = None
        self.youtube_music_channel_name = None
        self.youtube_music_artist_name = None
        self.youtube_music_artist_channel_id = None
        self.youtube_music_artist_subscriber_count = None
        self.youtube_music_artist_description = None
        self.youtube_music_artist_background_image_url = None
        self.origin_views = None  # 歌手被查看次数
        self.views = None  # 歌手被查看次数
        self.youtube_music_all_songs_url = None
        self.youtube_music_all_albums_singles_url = None
        self.youtube_music_all_videos_url = None
        self.youtube_music_all_songs_id = None
        self.youtube_music_all_albums_singles_id = None
        self.youtube_music_all_videos_id = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicArtistPagePlateInfoBatchDataItem(UpdateItem):
    """
    2.说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_page_plate_info_batch_data

        用于存储歌手channel_id采集到的页面信息，
        主要字段包含以下，模块包括：页面【歌曲】、页面【专辑】、页面【单曲】、页面【视频】链接信息
    """

    __table_name__ = "youtube_music_artist_page_plate_info_batch_data"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_all_songs_id",
                      "youtube_music_all_albums_singles_id", "youtube_music_all_videos_id",
                      "youtube_music_all_songs_url", "youtube_music_all_albums_singles_url",
                      "youtube_music_all_videos_url"]
    __update_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_all_songs_id",
                      "youtube_music_all_albums_singles_id", "youtube_music_all_videos_id"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_all_songs_id = None
        self.youtube_music_all_albums_singles_id = None
        self.youtube_music_all_videos_id = None
        self.youtube_music_all_songs_url = None
        self.youtube_music_all_albums_singles_url = None
        self.youtube_music_all_videos_url = None
        # self.songs_state = kwargs.get('songs_state')
        # self.albums_singles_state = kwargs.get('albums_singles_state')
        # self.videos_state = kwargs.get('videos_state')
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicArtistPageFeaturedBatchDataItem(UpdateItem):
    """
    3.说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_page_featured_batch_data

        用于存储歌手channel_id采集到的页面信息，
        主要模块包括歌手【精选】
    """

    __table_name__ = "youtube_music_artist_page_featured_batch_data"
    __update_key__ = ["gmg_artist_id", "youtube_music_artist_channel_id", "youtube_music_artist_channel_name",
                      "featured_title",
                      "featured_id", "featured_url", "batch"]
    __unique_key__ = ["youtube_music_artist_channel_id", "featured_id", "batch", "gmg_artist_id"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_artist_channel_id = None
        self.youtube_music_artist_channel_name = None
        self.featured_title = None
        self.featured_id = None
        self.featured_url = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicArtistPlateTaskItem(UpdateItem):
    """
    4.说明
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_page_featured_batch_data

        用于存储歌手板块信息
    """

    __table_name__ = "youtube_music_artist_plate_task"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_plate_remark"]
    __update_key__ = ['gmg_artist_id', 'youtube_music_channel_id', 'youtube_music_playlist_id',
                      'youtube_music_playlist_url', 'youtube_music_plate_remark']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_playlist_id = None
        self.youtube_music_playlist_url = None
        self.youtube_music_plate_remark = None  # 表明来自哪个板块
        # self.gtime = kwargs.get('gtime')
        # self.state = kwargs.get('state')
        # self.parser_name = kwargs.get('parser_name')


class YoutubeMusicArtistFansAlsoLikeBatchDataItem(UpdateItem):
    """
    5.说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_fans_also_like_batch_data

        用于存储歌手channel_id采集到的页面信息，
        主要模块包括歌手【粉丝也可能喜欢】
    """

    __table_name__ = "youtube_music_artist_fans_also_like_batch_data"
    __update_key__ = ["gmg_artist_id", "gmg_artist_name", "youtube_music_channel_id", "youtube_music_channel_name",
                      "fans_also_like_artist_name", "fans_also_like_artist_channel_id",
                      "fans_also_like_artist_channel_url",
                      "origin_fans_also_like_artist_subscriber_count", "fans_also_like_artist_subscriber_count",
                      "batch"]
    __unique_key__ = ["youtube_music_channel_id", "fans_also_like_artist_channel_id", "batch", "gmg_artist_id"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.gmg_artist_name = None
        self.youtube_music_channel_id = None
        self.youtube_music_channel_name = None
        self.fans_also_like_artist_name = None
        self.fans_also_like_artist_channel_id = None
        self.fans_also_like_artist_channel_url = None
        self.origin_fans_also_like_artist_subscriber_count = None
        self.fans_also_like_artist_subscriber_count = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicChannelIdCrawlSituationBatchDataItem(UpdateItem):
    """
    6.说明
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_channel_id_crawl_situation_batch_data
    """

    __table_name__ = "youtube_music_channel_id_crawl_situation_batch_data"
    __update_key__ = ['gmg_artist_id', 'youtube_music_channel_id', 'youtube_music_channel_name',
                      'youtube_music_artist_name', 'youtube_music_infomation_is_exist_remark',
                      'youtube_music_songs_plate_is_exist_remark',
                      'youtube_music_album_plate_is_exist_remark', 'youtube_music_singles_plate_is_exist_remark',
                      'youtube_music_videos_plate_is_exist_remark',
                      'youtube_music_featured_on_plate_is_exist_remark',
                      'youtube_music_fans_might_also_like_plate_is_exist_remark',
                      'youtube_music_latest_episodes_plate_is_exist_remark',
                      'youtube_music_podcasts_plate_is_exist_remark'
                      ]
    __unique_key__ = ["youtube_music_channel_id", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_channel_name = None
        self.youtube_music_artist_name = None
        # self.youtube_music_remark_rule = kwargs.get('youtube_music_remark_rule')
        self.youtube_music_infomation_is_exist_remark = None  # 歌手信息板块是否存在
        self.youtube_music_songs_plate_is_exist_remark = None  # 歌曲板块是否存在
        self.youtube_music_album_plate_is_exist_remark = None  # 专辑板块是否存在
        self.youtube_music_singles_plate_is_exist_remark = None  # 单曲板块是否存在
        self.youtube_music_videos_plate_is_exist_remark = None  # 视频板块是否存在
        self.youtube_music_featured_on_plate_is_exist_remark = None  # 精选板块是否存在
        self.youtube_music_fans_might_also_like_plate_is_exist_remark = None  # 粉丝可能也喜欢板块是否存在
        self.youtube_music_latest_episodes_plate_is_exist_remark = None  # 最新分集是否存在
        self.youtube_music_podcasts_plate_is_exist_remark = None  # 播客是否存在
        self.batch = kwargs.get('batch')
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicChannelIdBatchTaskItem(UpdateItem):
    """
    7.说明：
        任务表：youtube_music_channel_id_batch_task

        用于存储歌手channel_id采集情况记录
    """

    __table_name__ = "youtube_music_channel_id_batch_task"
    __update_key__ = ["gmg_artist_id", "youtube_music_channel_id", "gmg_artist_name", "youtube_music_channel_name"]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id"]

    def __init__(self, *args, **kwargs):
        self.gmg_artist_id = None
        self.gmg_artist_name = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')
        self.youtube_music_channel_id = None
        self.youtube_music_channel_name = None


# class YoutubeMusicArtistAlbumTaskItem(UpdateItem):
#     """
#     8.说明：
#         任务表：youtube_music_channel_id_batch_task
#         目标表：youtube_music_artist_album_task
#         用于存储歌手的专辑id
#     """
#
#     __table_name__ = "youtube_music_artist_album_task"
#     __update_key__ = ["album_id","gmg_artist_id","youtube_music_channel_id"]
#     __unique_key__ = ["album_id","gmg_artist_id","youtube_music_channel_id"]
#
#     def __init__(self, *args, **kwargs):
#         self.album_id = None
#         self.gmg_artist_id = None
#         # self.id = kwargs.get('id')
#         # self.parser_name = kwargs.get('parser_name')
#         # self.state = kwargs.get('state')
#         self.youtube_music_channel_id = None


# class YoutubeMusicArtistAlbumBatchDataItem(UpdateItem):
#     """
#     9.说明：
#         任务表：youtube_music_channel_id_batch_task
#         目标表：youtube_music_artist_album_batch_data
#         用于存储批次歌手的专辑id
#     """
#
#     __table_name__ = "youtube_music_artist_album_batch_data"
#     __update_key__ = ["album_id","gmg_artist_id","youtube_music_channel_id","batch","gmg_artist_name","youtube_music_channel_name"]
#     __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","album_id","batch"]
#
#     def __init__(self, *args, **kwargs):
#         self.album_id = None
#         self.batch = None
#         self.gmg_artist_id = None
#         self.gmg_artist_name = None
#         # self.gtime = kwargs.get('gtime')
#         # self.id = kwargs.get('id')
#         self.youtube_music_channel_id = None
#         self.youtube_music_channel_name = None


class YoutubeMusicArtistPageSongsBatchDataItem(UpdateItem):
    """
    10-说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_album_batch_data
        用于存储歌手页面下，歌曲因为数量过少，无法跳转情况下且源码不提供全部歌曲ID链接情况下，
        获取当前页面下的所有歌曲
    """

    __table_name__ = "youtube_music_artist_page_songs_batch_data"
    __update_key__ = ["batch", "gmg_artist_id", "youtube_music_channel_id", "youtube_video_id",
                      "youtube_video_img", "youtube_video_name", "youtube_video_artist_channel_id",
                      "youtube_video_artist_channel_name", "youtube_video_album_id", "youtube_video_album_name"]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "batch", "original_views", "views"]

    def __init__(self, *args, **kwargs):
        self.batch = None
        self.gmg_artist_id = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.youtube_music_channel_id = None
        self.youtube_video_id = None
        self.youtube_video_img = None
        self.youtube_video_name = None
        # self.youtube_video_album = None
        self.youtube_video_artist_channel_id = None
        self.youtube_video_artist_channel_name = None
        self.youtube_video_album_id = None
        self.youtube_video_album_name = None
        self.original_views = None
        self.views = None


class YoutubeMusicVideoTaskItem(UpdateItem):
    """
    11-说明：
        用于存储产生的youtube_video_id,并标注来源
    """

    __table_name__ = "youtube_music_video_task"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
                      "youtube_music_source_remark", "youtube_music_source_playlist_url"]
    __update_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
                      "youtube_music_source_remark", "youtube_music_source_playlist_url", "youtube_music_video_url"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_video_id = None
        self.youtube_music_video_url = None
        self.youtube_music_source_remark = None  # 表明来自哪个板块
        self.youtube_music_source_playlist_url = None
        # self.state = kwargs.get('state')
        # self.parser_name = kwargs.get('parser_name')
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicPlaylistTaskItem(UpdateItem):
    """
    12-说明：
        用于存储歌手专辑-单曲页面的URL作任务
    """

    __table_name__ = "youtube_music_playlist_task"
    __update_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_playlist_url", "youtube_music_plate_remark"]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_playlist_url", "youtube_music_plate_remark"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_plate_remark = None
        self.youtube_music_channel_id = None
        self.youtube_music_playlist_id = None
        self.youtube_music_playlist_url = None
        # self.state = kwargs.get('state')
        # self.gtime = kwargs.get('gtime')


# YoutubeMusicAlbumsSinglesDataItem
class YoutubeMusicPlaylistDataItem(UpdateItem):
    """
    13-说明：
        用于存储URL及跳转后的URL信息
    """

    __table_name__ = "youtube_music_playlist_data"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_plate_remark", "youtube_music_playlist_url_pre_redirect"]
    __update_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_plate_remark",
                      "youtube_music_playlist_url", "youtube_music_playlist_url_pre_redirect",
                      "batch", "title"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_playlist_id = None
        self.youtube_music_playlist_url = None
        self.youtube_music_playlist_url_pre_redirect = None
        self.batch = None
        self.title = None
        self.youtube_music_plate_remark = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicArtistPlateDataItem(UpdateItem):
    """
    14-用来存储playlist产生的数据，包含Albums/Singles、Songs、Videos
    """

    __table_name__ = "youtube_music_artist_plate_data"
    __update_key__ = ['gmg_artist_id', 'youtube_music_channel_id', 'youtube_music_playlist_id',
                      'youtube_music_playlist_url', 'youtube_music_plate_remark', 'serial_number',
                      'title', 'playlist_type', 'artist_name', 'publish_date',
                      'artist_channel_id', 'img_url', 'origin_songs_count', 'songs_count',
                      'description', 'origin_total_duration', 'total_duration',
                      'url_canonical', 'youtube_music_video_id', 'youtube_music_video_url',
                      'origin_youtube_music_video_url', 'youtube_music_video_url_split_playlist_id',
                      'youtube_music_video_url_split_playlist_url', 'youtube_music_video_name',
                      'youtube_music_video_artist_name', 'youtube_music_video_artist_channel_id',
                      'origin_youtube_music_video_play_count', 'youtube_music_video_play_count',
                      'youtube_music_playlist_set_video_id', 'youtube_music_video_playlist_name',
                      'youtube_music_video_playlist_id', 'origin_youtube_music_playlist_url',
                      'youtube_music_playlist_url_pre_redirect', 'origin_duration',
                      'duration', 'is_playable', 'batch', "other_info", "youtube_music_video_img_url"
                      ]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id", "playlist_type",
                      "youtube_music_video_name", "youtube_music_video_id", "youtube_music_plate_remark"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None  # aka中的gmg_artist_id
        self.youtube_music_channel_id = None  # Youtube艺人channel id
        self.youtube_music_playlist_id = None  # Youtube Music Playlist Id
        self.youtube_music_playlist_url = None  # Youtube Music Playlist URL
        self.youtube_music_plate_remark = None  # 该链接来自哪个版块
        self.serial_number = None  # 页面上的歌曲序号，如果不存在，则记为0
        self.title = None  # Youtube Music Playlist Title
        self.playlist_type = None  # Youtube Music Playlist 类型
        self.artist_name = None  # Youtube Music Playlist所属艺人
        self.publish_date = None  # Youtube Music Playlist发行日期或更新日期
        self.artist_channel_id = None  # Youtube Music Playlist所属艺人的Channel Id
        self.img_url = None  # 封面URL
        self.origin_songs_count = None  # Playlist下歌曲数量源字段
        self.songs_count = None  # Playlist下歌曲数量（处理后）
        self.description = None  # Playlist简介
        self.origin_total_duration = None  # Playlist总时长源字段
        self.total_duration = None  # Playlist总时长（处理后，单位：秒）
        self.url_canonical = None
        self.youtube_music_video_id = None  # 歌曲id
        self.youtube_music_video_url = None  # 歌曲URL
        self.origin_youtube_music_video_url = None  # 歌曲URL源字段
        self.youtube_music_video_url_split_playlist_id = None  # 歌曲携带的Playlist id（处理后）
        self.youtube_music_video_url_split_playlist_url = None
        self.youtube_music_video_name = None  # 歌曲名
        self.youtube_music_video_artist_name = None  # 歌曲艺人名
        self.youtube_music_video_artist_channel_id = None  # 歌曲艺人的Channel Id
        self.origin_youtube_music_video_play_count = None  # 歌曲播放量源字段
        self.youtube_music_video_play_count = None  # 歌曲播放量（处理后）
        self.youtube_music_playlist_set_video_id = None
        self.youtube_music_video_playlist_name = None  # 歌曲对应的Playlist名（专辑名或单曲名）
        self.youtube_music_video_playlist_id = None  # 歌曲对应的Playlist id
        self.origin_youtube_music_playlist_url = None  # 歌曲对应的playlist URL源字段
        self.youtube_music_playlist_url_pre_redirect = None  # 歌曲对应的Playlist URL（跳转前）
        self.origin_duration = None  # 歌曲播放时长源字段
        self.duration = None  # 歌曲播放时长（处理后，单位：秒）
        self.is_playable = None  # 歌曲是否可播放
        self.batch = None
        self.youtube_music_video_img_url = None
        self.other_info = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicArtistPlateCrawlSituationBatchRecordItem(UpdateItem):
    """
    15-用来记录playlist采集情况
    """

    __table_name__ = "youtube_music_artist_plate_crawl_situation_batch_record"
    __update_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_url",
                      "youtube_music_playlist_id", "youtube_music_playlist_infomation_remark", "batch"]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_playlist_infomation_remark", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_playlist_id = None
        self.youtube_music_playlist_url = None
        # self.youtube_music_playlist_infomation_rule = kwargs.get('youtube_music_playlist_infomation_rule')
        self.youtube_music_playlist_infomation_remark = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


# YoutubeMusicPlateUrlTaskItem
# YoutubeMusicPlateUrlDataItem

class YoutubeMusicPlateUrlTaskItem(UpdateItem):
    """
    16-用来存储各个Playlist跳转前的URL
    """

    __table_name__ = "youtube_music_plate_url_task"
    __unique_key__ = ["gmg_artist_id", 'youtube_music_plate_remark', "youtube_music_channel_id",
                      "youtube_music_playlist_id", "youtube_music_playlist_url_pre_redirect"]
    __update_key__ = ['gmg_artist_id', 'youtube_music_channel_id', 'youtube_music_playlist_id',
                      'youtube_music_playlist_url', 'youtube_music_plate_remark',
                      'youtube_music_playlist_url_pre_redirect', 'title']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_playlist_id = None
        self.youtube_music_playlist_url = None
        self.youtube_music_playlist_url_pre_redirect = None
        self.title = None
        self.youtube_music_plate_remark = None
        # self.state = kwargs.get('state')


class YoutubeMusicPlateUrlDataItem(UpdateItem):
    """
    17-用来存储各个Playlist跳转后的URL
    """

    __table_name__ = "youtube_music_plate_url_data"
    __update_key__ = ['gmg_artist_id', 'youtube_music_plate_remark', 'youtube_music_channel_id',
                      'youtube_music_playlist_id',
                      'youtube_music_playlist_url', 'title', 'youtube_music_playlist_url_pre_redirect',
                      'youtube_music_playlist_url_after_redirect', 'batch']
    __unique_key__ = ["gmg_artist_id", 'youtube_music_plate_remark', "youtube_music_channel_id",
                      "youtube_music_playlist_id", "youtube_music_playlist_url_pre_redirect"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_playlist_id = None
        self.youtube_music_playlist_url = None
        self.title = None
        self.youtube_music_playlist_url_pre_redirect = None  # 各Playlist跳转前的URL
        self.youtube_music_playlist_url_after_redirect = None  # 各Playlist跳转后的URL
        self.batch = None
        self.youtube_music_plate_remark = None


class ApiYoutubePlaylistInfoDataItem(UpdateItem):
    """
    18-用来存储youtube api下的playlist info信息
    """

    __table_name__ = "api_youtube_playlist_info_data"
    __unique_key__ = ["gmg_artist_id", "youtube_channel_id", "crawl_condition_youtube_playlist_id", "youtube_video_id",
                      "youtube_video_position", "batch"]
    __update_key__ = [
        "gmg_artist_id", "youtube_channel_id", "youtube_playlist_kind", "crawl_condition_youtube_playlist_id",
        "youtube_playlist_etag", "youtube_unique_id", "origin_youtube_published_at", "youtube_published_at",
        "youtube_playlist_channel_id", "youtube_video_id", "youtube_video_name",
        "description", "image_url", "youtube_playlist_id",
        "youtube_video_position", "youtube_resource_id_kind", "youtube_resource_id_video_id",
        "youtube_video_owner_channel_title", "youtube_video_owner_channel_id", "origin_youtube_video_publish_date",
        "youtube_video_publish_date", "youtube_video_privacy_status", "youtube_video_remark",
        "batch"
    ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_channel_id = None
        self.crawl_condition_youtube_playlist_id = None
        self.youtube_playlist_kind = None
        self.youtube_playlist_etag = None
        self.youtube_unique_id = None
        self.origin_youtube_published_at = None  # 内容被添加到播放列表的日期和时间
        self.youtube_published_at = None  # 内容被添加到播放列表的日期和时间
        self.youtube_playlist_channel_id = None  # YouTube 用于唯一标识将内容添加到播放列表的用户的 ID
        self.youtube_video_id = None
        self.youtube_video_name = None
        self.description = None
        self.image_url = None
        self.youtube_playlist_id = None
        self.youtube_video_position = None  # 内容在播放列表中的顺序
        self.youtube_resource_id_kind = None  # 所引用资源的种类或类型
        self.youtube_resource_id_video_id = None  # 如果 snippet.resourceId.kind 属性的值为 youtube#video，则此属性会显示且其值将包含 YouTube 用来对播放列表中的视频进行唯一标识的 ID
        self.youtube_video_owner_channel_title = None  # 上传视频的频道的频道标题
        self.youtube_video_owner_channel_id = None  # 上传此视频的频道的频道 ID
        self.origin_youtube_video_publish_date = None  # 视频发布到 YouTube 的日期和时间
        self.youtube_video_publish_date = None
        self.youtube_video_privacy_status = None  # 播放列表项的隐私设置
        self.youtube_video_remark = None  # 标注来源
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class ApiYoutubeVideoInfoDataItem(UpdateItem):
    """
    19-用来存储youtube api下的video info信息
    """

    __table_name__ = "api_youtube_video_info_data"
    __update_key__ = [
        # "gmg_artist_id","youtube_channel_id","youtube_source_playlist_id","youtube_video_source_remark",
        "youtube_video_id", "youtube_video_kind",
        "youtube_video_etag", "youtube_video_published_at", "youtube_video_channel_id",
        "youtube_video_name", "description", "image_url", "origin_youtube_video_published_at",
        "youtube_video_owner_channel_title", "youtube_video_relate_tags", "youtube_video_category_id",
        "youtube_video_localized_title", "youtube_video_localized_description", "origin_duration", "duration",
        "youtube_video_dimension", "youtube_video_definition", "youtube_video_caption",
        "youtube_video_licensed_content", "youtube_video_region_restriction_allowed",
        "youtube_video_region_restriction_blocked",
        "youtube_video_content_rating", "youtube_video_projection", "youtube_video_upload_status",
        "youtube_video_privacy_status", "youtube_video_license", "youtube_video_embeddable",
        "youtube_video_public_stats_viewable", "youtube_video_made_for_kids", "youtube_video_view_count",
        "youtube_video_like_count", "youtube_video_comment_count", "youtube_video_topic_categories", "batch"
    ]
    __unique_key__ = ["youtube_video_id", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        # self.gmg_artist_id = None
        # self.youtube_channel_id = None
        # self.youtube_source_playlist_id = None
        self.youtube_video_id = None
        # self.youtube_video_source_remark = None
        self.youtube_video_kind = None  # 标识 API 资源类型。其值为 youtube#video
        self.youtube_video_etag = None  # 此资源的 Etag
        self.origin_youtube_video_published_at = None  # 视频发布的日期和时间，请注意，此时间可能与视频上传的时间不同
        self.youtube_video_published_at = None  # 视频发布的日期和时间，请注意，此时间可能与视频上传的时间不同
        self.youtube_video_channel_id = None  # YouTube 用来唯一标识上传视频的目标频道的 ID
        self.youtube_video_name = None  # 视频的标题
        self.description = None  # 视频的说明
        self.image_url = None  # 图片的链接
        self.youtube_video_owner_channel_title = None  # 视频所属频道的频道标题
        self.youtube_video_relate_tags = None  # 与视频相关联的一系列关键字
        self.youtube_video_category_id = None  # 与视频相关联的 YouTube 视频类别
        self.youtube_video_localized_title = None  # 本地化的视频标题
        self.youtube_video_localized_description = None  # 本地化的视频说明
        self.origin_duration = None  # 视频的长度
        self.duration = None  # 视频的长度
        self.youtube_video_dimension = None  # 指明视频支持 3D 还是 2D
        self.youtube_video_definition = None  # 指明视频是能够以高清 (HD) 模式播放，还是仅能以标清模式播放。此属性的有效值包括：hd、sd
        self.youtube_video_caption = None  # 指明视频是否提供字幕,此属性的有效值包括:true、false
        self.youtube_video_licensed_content = None  # 指明视频是否代表许可内容，即内容已上传到与 YouTube 内容合作伙伴关联的频道，并由该合作伙伴提出版权主张
        self.youtube_video_region_restriction_allowed = None  # 地区代码列表，用于标识哪些国家/地区的用户可以观看视频。如果此属性存在，但其值中未列出某个国家/地区，则表示该视频无法在该国家/地区显示。如果此属性存在且包含空列表，则视频在所有国家/地区禁播
        self.youtube_video_region_restriction_blocked = None  # 地区代码列表，用于标识视频遭到禁播的国家/地区。如果该属性存在，但其值中未列出某个国家/地区，则表示该视频在该国家/地区是可观看的。如果此属性存在且包含空列表，则视频在所有国家/地区均可观看。
        self.youtube_video_content_rating = None  # 指定视频根据各种分级制度获得的分级
        self.youtube_video_projection = None  # 指定视频的投影格式，此属性的有效值包括：360、rectangular
        self.youtube_video_upload_status = None  # 已上传的视频的状态，此属性的有效值包括：deleted、failed、processed、rejected、uploaded
        self.youtube_video_privacy_status = None  # 视频的隐私状态。此属性的有效值包括：private、public、unlisted
        self.youtube_video_license = None  # 视频的许可，此属性的有效值包括：creativeCommon、youtube
        self.youtube_video_embeddable = None  # 此值用于指明视频是否可以嵌入到其他网站中
        self.youtube_video_public_stats_viewable = None  # 此值用于指明视频观看页面上的扩展视频统计信息是否公开显示
        self.youtube_video_made_for_kids = None  # 此值指示视频是否被指定为面向儿童的内容，并且包含视频当前的“面向儿童的内容”状态
        self.youtube_video_view_count = None
        self.youtube_video_like_count = None
        self.youtube_video_comment_count = None
        self.youtube_video_topic_categories = None  # 提供视频内容简要说明的维基百科网址列表
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicVideoViewsCrawlSituationBatchRecordItem(UpdateItem):
    """
    20-用来存储youtube music video歌曲播放量采集信息情况记录
    """

    __table_name__ = "youtube_music_video_views_crawl_situation_batch_record"
    __update_key__ = [
        "gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
        "youtube_music_source_remark", "youtube_music_source_playlist_url",
        "youtube_music_video_views_infomation_remark",
        "exception_info", "batch", "origin_is_playable", "is_playable"
    ]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
                      "youtube_music_source_remark", "youtube_music_source_playlist_url", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_video_id = None
        self.youtube_music_source_remark = None
        self.youtube_music_source_playlist_url = None
        # self.youtube_music_video_views_infomation_rule = kwargs.get('youtube_music_video_views_infomation_rule')
        self.youtube_music_video_views_infomation_remark = None
        self.exception_info = None
        self.batch = None
        self.origin_is_playable = None
        self.is_playable = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicVideoViewsDataItem(UpdateItem):
    """
    21-用来存储youtube music video歌曲播放量信息
    """

    __table_name__ = "youtube_music_video_views_data"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id", "batch",
                      "youtube_music_source_playlist_url", "youtube_music_source_remark"]
    __update_key__ = [
        "gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
        "youtube_music_video_url", "youtube_music_source_remark", "youtube_music_source_playlist_url",
        "youtube_music_video_name", "duration", "is_playable", "origin_is_playable",
        "image_url", "youtube_music_view_count", "youtube_music_author",
        "youtube_music_video_is_private", "youtube_music_video_url_canonical", "youtube_music_video_title",
        "description", "youtube_music_video_tags", "youtube_music_external_channel_name",
        "youtube_music_external_channel_id", "youtube_music_external_channel_url", "youtube_music_profile_url",
        "youtube_music_external_video_id", "youtube_music_external_duration", "youtube_music_external_duration_iso",
        "origin_youtube_music_video_publish_date", "youtube_music_video_publish_date", "youtube_music_video_category",
        "origin_youtube_music_video_upload_date", "youtube_music_video_upload_date",
        "youtube_music_video_available_countries",
        "batch"
    ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_video_id = None
        self.youtube_music_video_url = None
        self.youtube_music_source_remark = None
        self.youtube_music_source_playlist_url = None
        self.origin_is_playable = None
        self.is_playable = None
        self.youtube_music_video_name = None
        self.duration = None
        self.image_url = None
        self.youtube_music_view_count = None
        self.youtube_music_author = None
        self.youtube_music_video_is_private = None
        self.youtube_music_video_url_canonical = None
        self.youtube_music_video_title = None
        self.description = None
        self.youtube_music_video_tags = None
        self.youtube_music_external_channel_name = None
        self.youtube_music_external_channel_id = None
        self.youtube_music_external_channel_url = None
        self.youtube_music_profile_url = None
        self.youtube_music_external_video_id = None
        self.youtube_music_external_duration = None
        self.youtube_music_external_duration_iso = None
        self.origin_youtube_music_video_publish_date = None
        self.youtube_music_video_publish_date = None
        self.youtube_music_video_category = None
        self.origin_youtube_music_video_upload_date = None
        self.youtube_music_video_upload_date = None
        self.youtube_music_video_available_countries = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicVideoArtistDataItem(UpdateItem):
    """
        22-用来存储youtube music所涉及的艺人信息，主要为Channel id
    """
    __update_key__ = [
        "gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
        "youtube_music_video_url", "youtube_music_source_remark", "youtube_music_source_playlist_url",
        "youtube_music_video_title", "youtube_music_video_artist_name", "youtube_music_video_artist_channel_id",
        "origin_youtube_music_video_views", "youtube_music_video_views", "origin_youtube_music_video_likes",
        "youtube_music_video_likes", "image_url", "origin_duration",
        "duration", "batch"
    ]

    __table_name__ = "youtube_music_video_artist_data"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
                      "youtube_music_source_remark", "youtube_music_source_playlist_url", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_video_id = None
        self.youtube_music_video_url = None
        self.youtube_music_source_remark = None
        self.youtube_music_source_playlist_url = None
        self.youtube_music_video_title = None
        self.youtube_music_video_artist_name = None
        self.youtube_music_video_artist_channel_id = None
        self.origin_youtube_music_video_views = None
        self.youtube_music_video_views = None
        self.origin_youtube_music_video_likes = None
        self.youtube_music_video_likes = None
        self.image_url = None
        self.origin_duration = None
        self.duration = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicVideoArtistCrawlSituationBatchRecordItem(UpdateItem):
    """
    23-用来存储youtube music所涉及的艺人信息采集情况
    """

    __table_name__ = "youtube_music_video_artist_crawl_situation_batch_record"
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
                      "youtube_music_source_remark", "youtube_music_source_playlist_url", "batch"]
    __update_key__ = [
        "gmg_artist_id", "youtube_music_channel_id", "youtube_music_video_id",
        "youtube_music_video_url", "youtube_music_source_remark", "youtube_music_source_playlist_url",
        "youtube_music_video_artists_infomation_remark", "batch"
    ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_video_id = None
        self.youtube_music_video_url = None
        self.youtube_music_source_remark = None
        self.youtube_music_source_playlist_url = None
        # self.youtube_music_video_artist_infomation_rule = kwargs.get('youtube_music_video_artist_infomation_rule')
        self.youtube_music_video_artists_infomation_remark = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicRelatedPlaylistsInfoBatchDataItem(UpdateItem):
    """
    23-用来存储Youtube Music Related Playlists信息
    """

    __table_name__ = "youtube_music_related_playlists_info_batch_data"
    __update_key__ = [
        "gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
        "youtube_music_playlist_url", "youtube_music_plate_remark", "img_url",
        "title", "youtube_music_related_playlist_id", "youtube_music_related_playlist_url",
        "playlist_type", "youtube_music_related_playlist_artist_name",
        "youtube_music_related_playlist_artist_channel_id",
        "youtube_music_related_playlist_artist_channel_url", "origin_views", "views",
        "batch"
    ]
    __unique_key__ = ["gmg_artist_id", "youtube_music_channel_id", "youtube_music_playlist_id",
                      "youtube_music_plate_remark", "youtube_music_related_playlist_id", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = kwargs.get('')
        self.youtube_music_channel_id = kwargs.get('')
        self.youtube_music_playlist_id = kwargs.get('')
        self.youtube_music_playlist_url = kwargs.get('')
        self.youtube_music_plate_remark = kwargs.get('')
        self.img_url = kwargs.get('')
        self.title = kwargs.get('')
        self.youtube_music_related_playlist_id = kwargs.get('')
        self.youtube_music_related_playlist_url = kwargs.get('')
        self.playlist_type = kwargs.get('')
        self.youtube_music_related_playlist_artist_name = kwargs.get('')
        self.youtube_music_related_playlist_artist_channel_id = kwargs.get('')
        self.youtube_music_related_playlist_artist_channel_url = kwargs.get('')
        self.origin_views = kwargs.get('')
        self.views = kwargs.get('')
        self.batch = kwargs.get('')
        # self.gtime = kwargs.get('gtime')
