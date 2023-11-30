# -*- coding: utf-8 -*-
"""
Created on 2023-09-06 20:13:05
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import UpdateItem


class YoutubeLinkGetChannelIdDataItem(UpdateItem):
    """
    通过给予的YouTube Link，获取其对应的YouTube Channel Id
    """

    __table_name__ = "youtube_link_get_channel_id_data"
    __unique_key__ = ['youtube_channel_link']
    __update_key__ = ['youtube_channel_id','youtube_channel_link','youtube_link']

    def __init__(self, *args, **kwargs):
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.youtube_channel_id = None
        self.youtube_channel_link = None  # 获取到的YouTube Channel Link
        self.youtube_link = None  # 任务中给的YouTube Link


class YoutubeVideoLinkInfoBatchDataItem(UpdateItem):
    """
    获取其YouTube LinK页面信息，包括YouTube Link、Title、Channel Id、Views
    """

    __table_name__ = "youtube_video_link_info_batch_data"
    __unique_key__ = ['youtube_link','batch']
    __update_key__ = ['batch', 'youtube_channel_id','youtube_link','youtube_title','youtube_views','youtube_channel_name']

    def __init__(self, *args, **kwargs):
        self.batch = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.youtube_channel_id = None
        self.youtube_link = None
        self.youtube_title = None
        self.youtube_views = None
        self.youtube_channel_name = None


class YoutubeMusicPlaylistBatchDataItem(UpdateItem):
    """
    通过给予的YouTube Music Playlist获取其下对应的所有歌曲id
    """

    __table_name__ = "youtube_music_playlist_batch_data"
    __unique_key__ = ['youtube_music_playlist_id','youtube_music_video_id']
    __update_key__ = ['youtube_music_playlist_link','youtube_music_playlist_id','youtube_music_video_id','youtube_music_video_link','batch']


    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_music_playlist_link = None
        self.youtube_music_playlist_id = None
        self.youtube_music_video_id = None
        self.youtube_music_video_link = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')

class YoutubeVideoLinkInfoBatchTaskItem(UpdateItem):
    """
    将获取到的YouTube Video Id添加至任务表youtube_video_link_info_batch_task
    """

    __table_name__ = "youtube_video_link_info_batch_task"
    __unique_key__ = ['youtube_video_link']
    __update_key__ = ['youtube_video_link']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_video_link = None  # Youtube Video Link
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')