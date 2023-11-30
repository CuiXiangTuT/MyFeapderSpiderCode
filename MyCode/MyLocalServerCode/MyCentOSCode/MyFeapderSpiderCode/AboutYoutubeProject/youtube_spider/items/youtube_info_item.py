# -*- coding: utf-8 -*-
"""
Created on 2023-08-18 11:04:26
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import UpdateItem

class ApiYoutubeArtistChannelIdBatchDataItem(UpdateItem):
    """
    1-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：api_youtube_artist_channel_id_batch_task
        涉及数据表：api_youtube_artist_channel_id_batch_data
        涉及程序：crawl_youtube_artist_playlist_info_spider.py
        说明：
            通过YouTube前端页面获取到的YouTube Channel Id，经YouTube API主要获取其对应的播放列表Id（Playlist Id）信息
    """

    __table_name__ = "api_youtube_artist_channel_id_batch_data"
    __update_key__ = ['crawl_condition_youtube_artist_channel_id','youtube_playlist_id','batch','publish_date','title','crawl_result_youtube_artist_channel_id']
    __unique_key__ = ['crawl_condition_youtube_artist_channel_id','youtube_playlist_id']

    def __init__(self, *args, **kwargs):
        self.batch = None
        self.crawl_condition_youtube_artist_channel_id = None  # 抓取条件的Youtube艺人频道id
        self.crawl_result_youtube_artist_channel_id = None  # 实际结果的Youtube艺人频道id
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.publish_date = None  # Youtube播放列表创建时间
        self.title = None  # Youtube播放列表名称
        self.youtube_playlist_id = None  # Youtube艺人播放列表

class ApiYoutubeArtistPlaylistBatchTaskItem(UpdateItem):
    """
    2-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：api_youtube_artist_playlist_batch_task
        涉及数据表：api_youtube_artist_playlist_batch_data
        涉及程序：
            crawl_youtube_artist_playlist_info_spider.py
    """
    __table_name__ = "api_youtube_artist_playlist_batch_task"
    __unique_key__ = ["crawl_condition_youtube_artist_channel_id","youtube_playlist_id"]
    __update_key__ = ["crawl_condition_youtube_artist_channel_id","youtube_playlist_id"]

    def __init__(self, *args, **kwargs):
        self.crawl_condition_youtube_artist_channel_id = None  # 抓取条件的Youtube艺人频道id
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')
        self.youtube_playlist_id = None  # Youtube艺人播放列表


class ApiYoutubeArtistPlaylistBatchDataItem(UpdateItem):
    """
    3-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：api_youtube_artist_playlist_batch_task
        涉及数据表：api_youtube_artist_playlist_batch_data
        涉及程序：
            crawl_youtube_playlist_video_info_spider.py
    """

    __table_name__ = "api_youtube_artist_playlist_batch_data"
    __update_key__ = ["youtube_playlist_id","youtube_video_id"]
    __unique_key__ = ["youtube_playlist_id","youtube_video_id","batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_playlist_id = None  # YouTube播放列表id
        self.youtube_video_id = None  # YouTube视频id
        # self.gtime = kwargs.get('gtime')
        self.batch = None

class ApiYoutubeVideoBatchTaskItem(UpdateItem):
    """
    4-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：api_youtube_video_batch_task
        涉及数据表：api_youtube_video_batch_data
        涉及程序：
            crawl_youtube_playlist_video_info_spider.py
    """

    __table_name__ = "api_youtube_video_batch_task"
    __unique_key__ = ["youtube_video_id"]
    __update_key__ = ["youtube_video_id"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_video_id = None
        # self.parser_name = kwargs.get('parser_name')
        # self.gtime = kwargs.get('gtime')
        # self.state = kwargs.get('state')

class ApiYoutubeVideoBatchDataItem(UpdateItem):
    """
    5-Item说明：
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：api_youtube_video_batch_task
        涉及数据表：api_youtube_video_batch_data
        涉及程序：
            crawl_youtube_video_info_spider.py
    """

    __table_name__ = "api_youtube_video_batch_data"
    __update_key__ = ["youtube_video_id", "views", "like_count", "batch"]
    __unique_key__ = ["youtube_video_id", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.youtube_video_id = None  # Youtube视频id
        self.views = None  # 视频播放列
        self.like_count = None  # 视频点赞数
        self.batch = None
        # self.gtime = kwargs.get('gtime')