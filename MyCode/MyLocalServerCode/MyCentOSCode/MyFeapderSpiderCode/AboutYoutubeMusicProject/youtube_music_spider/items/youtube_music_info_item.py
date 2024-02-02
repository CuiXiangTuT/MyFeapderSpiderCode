# -*- coding: utf-8 -*-
"""
Created on 2023-10-08 15:27:16
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import UpdateItem


class YoutubeMusicChannelIdBatchDataItem(UpdateItem):
    """
    1-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：youtube_music_channel_id_batch_task
        涉及数据表：youtube_music_channel_id_batch_data
        涉及程序：
            crawl_youtube_music_artist_playlist_info_spider.py
    """

    __table_name__ = "youtube_music_channel_id_batch_data"
    __unique_key__ = ["youtube_music_channel_id", "batch"]
    __update_key__ = ["youtube_music_artist_name", "youtube_music_channel_name", "youtube_music_track_playlist_url", "youtube_music_album_single_playlist_url", "youtube_music_video_playlist_url"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_music_channel_id = None
        self.youtube_music_artist_name = None
        self.youtube_music_channel_name = None  # Youtube Music频道名（与youtube_music_artist_name不一致，此字段带Topic）
        self.youtube_music_track_playlist_url = None  # YouTube Music歌曲列表链接
        self.youtube_music_album_single_playlist_url = None  # YouTube Music专辑及单曲列表链接
        self.youtube_music_video_playlist_url = None  # YouTube Music视频列表链接
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicChannelIdPlaylistBatchTaskItem(UpdateItem):
    """
    2-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：youtube_music_channel_id_batch_task
        涉及数据表：youtube_music_channel_id_batch_data
        涉及程序：
            crawl_youtube_music_artist_playlist_info_spider.py

    """

    __table_name__ = "youtube_music_channel_id_playlist_batch_task"
    __update_key__ = ["youtube_music_channel_id","youtube_music_track_playlist_url","youtube_music_album_single_playlist_url","youtube_music_video_playlist_url"]
    __unique_key__ = ["youtube_music_channel_id"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_music_channel_id = None
        self.youtube_music_track_playlist_url = None  # YouTube Music歌曲列表链接
        self.youtube_music_album_single_playlist_url = None  # YouTube Music专辑及单曲列表链接
        self.youtube_music_video_playlist_url = None  # YouTube Music视频列表链接
        # self.album_single_playlist_state = kwargs.get('album_single_playlist_state')
        # self.parser_name = kwargs.get('parser_name')
        # self.gtime = kwargs.get('gtime')


class YoutubeMusicChannelIdPlaylistBatchDataItem(UpdateItem):
    """
    3-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：
        涉及数据表：
        涉及程序：
    """

    __table_name__ = "youtube_music_channel_id_playlist_batch_data"
    __unique_key__ = []
    __update_key__ = []

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_music_channel_id = kwargs.get('youtube_music_channel_id')
        self.youtube_music_album_single_playlist_url = kwargs.get('youtube_music_album_single_playlist_url')  # Youtube Music 专辑及单曲的综合播放列表链接
        self.youtube_music_album_single_url_pre_redirect = kwargs.get('youtube_music_album_single_url_pre_redirect')  # Youtube Music专辑及单曲的单个链接（重定向前）
        self.youtube_music_album_single_url = kwargs.get('youtube_music_album_single_url')  # Youtube Music专辑及单曲的单个链接（重定向后），该字段获取等号后的内容，即为youtube_artist_playlist_batch_task中的youtube_playlist_id字段
        self.batch = kwargs.get('batch')
        # self.gtime = kwargs.get('gtime')