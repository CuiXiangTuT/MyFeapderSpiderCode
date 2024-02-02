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
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","batch"]
    __update_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_artist_name","youtube_music_artist_subscriber_count",
    "youtube_music_artist_description","youtube_music_artist_background_image_url","views","youtube_music_all_songs_url","youtube_music_all_albums_singles_url",
    "youtube_music_all_videos_url","batch","youtube_music_all_songs_id","youtube_music_all_albums_singles_id",
    "youtube_music_all_videos_id","youtube_music_artist_channel_id","gmg_artist_name","youtube_music_channel_name"]

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
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_all_songs_id","youtube_music_all_albums_singles_id","youtube_music_all_videos_id",
    "youtube_music_all_songs_url","youtube_music_all_albums_singles_url","youtube_music_all_videos_url"]
    __update_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_all_songs_id","youtube_music_all_albums_singles_id","youtube_music_all_videos_id"]

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
    __update_key__ = ["gmg_artist_id","youtube_music_artist_channel_id","youtube_music_artist_channel_name","featured_title",
    "featured_id","featured_url","batch"]
    __unique_key__ = ["youtube_music_artist_channel_id","featured_id","batch","gmg_artist_id"]

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

class YoutubeMusicArtistPlateBatchTaskItem(UpdateItem):
    """
    4.说明
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_page_featured_batch_data

        用于存储歌手板块信息
    """

    __table_name__ = "youtube_music_artist_plate_task"
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_playlist_id","youtube_music_plate_remark"]
    __update_key__ = ['gmg_artist_id','youtube_music_channel_id','youtube_music_playlist_id','youtube_music_playlist_url','youtube_music_plate_remark']

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
    __update_key__ = ["gmg_artist_id","gmg_artist_name","youtube_music_channel_id","youtube_music_channel_name",
    "fans_also_like_artist_name","fans_also_like_artist_channel_id","fans_also_like_artist_channel_url",
    "origin_fans_also_like_artist_subscriber_count","fans_also_like_artist_subscriber_count","batch"]
    __unique_key__ = ["youtube_music_channel_id","fans_also_like_artist_channel_id","batch","gmg_artist_id"]

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
    __update_key__ = ['gmg_artist_id','youtube_music_channel_id','youtube_music_channel_name',
    'youtube_music_artist_name','youtube_music_infomation_is_exist_remark','youtube_music_songs_plate_is_exist_remark',
    'youtube_music_album_plate_is_exist_remark','youtube_music_singles_plate_is_exist_remark','youtube_music_videos_plate_is_exist_remark',
    'youtube_music_featured_on_plate_is_exist_remark','youtube_music_fans_might_also_like_plate_is_exist_remark','youtube_music_latest_episodes_plate_is_exist_remark',
    'youtube_music_podcasts_plate_is_exist_remark'
    ]
    __unique_key__ = ["youtube_music_channel_id","batch"]

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
    __update_key__ = ["gmg_artist_id","youtube_music_channel_id","gmg_artist_name","youtube_music_channel_name"]
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id"]

    def __init__(self, *args, **kwargs):
        self.gmg_artist_id = None
        self.gmg_artist_name = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')
        self.youtube_music_channel_id = None
        self.youtube_music_channel_name = None


class YoutubeMusicArtistAlbumTaskItem(UpdateItem):
    """
    8.说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_album_task
        用于存储歌手的专辑id
    """

    __table_name__ = "youtube_music_artist_album_task"
    __update_key__ = ["album_id","gmg_artist_id","youtube_music_channel_id"]
    __unique_key__ = ["album_id","gmg_artist_id","youtube_music_channel_id"]

    def __init__(self, *args, **kwargs):
        self.album_id = None
        self.gmg_artist_id = None
        # self.id = kwargs.get('id')
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')
        self.youtube_music_channel_id = None


class YoutubeMusicArtistAlbumBatchDataItem(UpdateItem):
    """
    9.说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_album_batch_data
        用于存储批次歌手的专辑id
    """

    __table_name__ = "youtube_music_artist_album_batch_data"
    __update_key__ = ["album_id","gmg_artist_id","youtube_music_channel_id","batch","gmg_artist_name","youtube_music_channel_name"]
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","album_id","batch"]

    def __init__(self, *args, **kwargs):
        self.album_id = None
        self.batch = None
        self.gmg_artist_id = None
        self.gmg_artist_name = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.youtube_music_channel_id = None
        self.youtube_music_channel_name = None


class YoutubeMusicArtistPageSongsBatchDataItem(UpdateItem):
    """
    10-说明：
        任务表：youtube_music_channel_id_batch_task
        目标表：youtube_music_artist_album_batch_data
        用于存储歌手页面下，歌曲因为数量过少，无法跳转情况下且源码不提供全部歌曲ID链接情况下，
        获取当前页面下的所有歌曲
    """

    __table_name__ = "youtube_music_artist_page_songs_batch_data"
    __update_key__ = ["batch","gmg_artist_id","youtube_music_channel_id","youtube_video_id",
    "youtube_video_img","youtube_video_name","youtube_video_artist_channel_id",
    "youtube_video_artist_channel_name","youtube_video_album_id","youtube_video_album_name"]
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","batch","original_views","views"]

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
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_video_id","youtube_music_source_remark","youtube_music_source_playlist_url"]
    __update_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_video_id","youtube_music_source_remark","youtube_music_source_playlist_url","youtube_music_video_url"]

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


class YoutubeMusicAlbumsSinglesTaskItem(UpdateItem):
    """
    12-说明：
        用于存储歌手专辑-单曲页面的URL作任务
    """

    __table_name__ = "youtube_music_albums_singles_task"
    __update_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_albums_singles_id","youtube_music_albums_singles_url"]
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_albums_singles_id","youtube_music_albums_singles_url"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = kwargs.get('gmg_artist_id')
        self.youtube_music_channel_id = kwargs.get('youtube_music_channel_id')
        self.youtube_music_albums_singles_id = kwargs.get('youtube_music_albums_singles_id')
        self.youtube_music_albums_singles_url = kwargs.get('youtube_music_albums_singles_url')
        # self.state = kwargs.get('state')
        # self.gtime = kwargs.get('gtime')



class YoutubeMusicAlbumsSinglesDataItem(UpdateItem):
    """
    13-说明：
        用于存储【专辑-单曲】页面下的所有【专辑、单曲】的URL及跳转后的URL信息
    """

    __table_name__ = "youtube_music_albums_singles_data"
    __unique_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_albums_singles_id"]
    __update_key__ = ["gmg_artist_id","youtube_music_channel_id","youtube_music_albums_singles_id",
    "youtube_music_albums_singles_url","youtube_music_albums_singles_url_pre_redirect","youtube_music_albums_singles_url_after_redirect",
    "batch","title"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.youtube_music_channel_id = None
        self.youtube_music_albums_singles_id = None
        self.youtube_music_albums_singles_url = None
        self.youtube_music_albums_singles_url_pre_redirect = None
        self.youtube_music_albums_singles_url_after_redirect = None
        self.batch = None
        self.title = None
        # self.gtime = kwargs.get('gtime')
