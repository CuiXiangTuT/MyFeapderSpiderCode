# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 15:07:22
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import UpdateItem


class ChartDataDailyBoomplayItem(UpdateItem):
    """
    1-Item说明：
        Item：榜单页面相关数据字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：chart_boomplay_batch_task
        涉及数据表：chart_boomplay_batch_data
        涉及程序：
            crawl_boomplay_chart_data_daily_spider.py
    """
    __table_name__ = "chart_data_daily_boomplay_af"
    __update_key__ = ['rank', 'song_id', 'crawl_chart_country', 'batch', 'song_name', 'chart_artist_id',
                      'chart_artist_name', 'album_id', 'album_name', 'duration', 'chart_region', 'chart_site',
                      'chart_type', 'update_frequency', 'chart_language', 'chart_segment', 'chart_release_date',
                      'ranking_state_change', 'chart_name']
    __unique_key__ = ['rank', 'song_id', 'crawl_chart_country', 'batch']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.rank = None  # 榜单歌曲排名
        self.song_id = None  # 榜单歌曲id
        self.song_name = None  # 榜单歌曲名
        self.chart_artist_id = None  # 榜单歌手id
        self.chart_artist_name = None  # 榜单歌手名
        self.album_id = None  # 榜单专辑id
        self.album_name = None  # 榜单专辑名
        self.duration = None  # 歌曲时长
        self.chart_region = None  # 抓取国家地区
        self.crawl_chart_country = None  # 抓取国家
        self.batch = None  # 抓取批次
        self.chart_site = None  # 抓取网站
        self.chart_type = None  # 榜单类型（歌手榜/歌曲榜）
        self.update_frequency = None  # 榜单更新频率
        self.chart_language = None  # 榜单语种
        self.chart_segment = None  # 榜单内容数量
        self.chart_release_date = None  # 榜单本身的更新日期
        self.ranking_state_change = None  # 榜单歌曲排名变化
        self.chart_name = None  # 榜单名
        # self.note = None  # 标明数据是北京/非洲


class BoomplayArtistInfoBatchTaskItem(UpdateItem):
    """
    2-Item说明：
        Item：歌手任务相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：chart_boomplay_batch_task
        涉及数据表：chart_boomplay_batch_data
        涉及程序：
            crawl_boomplay_chart_data_daily_spider.py
    """

    __table_name__ = "boomplay_artist_info_batch_task"
    __unique_key__ = ["boomplay_artist_id"]
    __update_key__ = ["gmg_artist_id", 'gmg_artist_name', 'boomplay_artist_name']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.gmg_artist_name = None  # gmg_artist_aka中的字段
        self.boomplay_artist_id = None  # 榜单抓取过来的歌手id
        self.boomplay_artist_name = None  # 榜单抓取过来的歌手名
        # self.source = None
        # self.state = kwargs.get('state')  # 抓取歌手信息时使用的状态字段state
        # self.usable = kwargs.get('usable')  # boomplay_artist_id是否可用（gmg_artist_aka表中不存在的数据被认为不可用）
        # self.parser_name = kwargs.get('parser_name')
        # self.insert_date = kwargs.get('insert_date')  # 更新时间
        # self.bj_artist_album_track_state = kwargs.get('bj_artist_album_track_state')  # 北京抓取歌手的歌曲、专辑任务时使用的状态字段
        # self.af_artist_album_track_state = kwargs.get('af_artist_album_track_state')  # 非洲抓取歌手的歌曲、专辑任务时使用的状态字段


class BoomplayAlbumInfoBatchTaskItem(UpdateItem):
    """
    3-Item说明：
        Item：专辑任务相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：chart_boomplay_batch_task
        涉及数据表：chart_boomplay_batch_data
        涉及程序：
            crawl_boomplay_chart_data_daily_spider.py
    """

    __table_name__ = "boomplay_album_info_batch_task"
    __update_key__ = ['album_id']
    __unique_key__ = ['album_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.album_id = None  # 专辑id
        # self.source = None
        # self.bj_state = kwargs.get('bj_state')  # 北京抓取状态字段
        # self.af_state = kwargs.get('af_state')  # 非洲抓取状态字段
        # self.gtime = kwargs.get('gtime')  # 更新时间
        # self.parser_name = kwargs.get('parser_name')


class BoomplayTrackInfoBatchTaskItem(UpdateItem):
    """
    4-Item说明：
        Item：歌曲任务相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：chart_boomplay_batch_task
        涉及数据表：chart_boomplay_batch_data
        涉及程序：
            crawl_boomplay_chart_data_daily_spider.py
    """

    __table_name__ = "boomplay_track_info_batch_task"
    __unique_key__ = ['track_id']
    __update_key__ = ['track_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.track_id = None  # 歌曲id
        # self.source = None
        # self.gtime = kwargs.get('gtime')  # 更新时间
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')
        # self.views_state = kwargs.get('views_state')


class BoomplayArtistTrackBatchDataItem(UpdateItem):
    """
    5-Item说明：
        Item：歌手-歌曲 映射相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：chart_boomplay_batch_task
        涉及数据表：boomplay_artist_track_batch_data
        涉及程序：
            crawl_boomplay_chart_data_daily_spider.py
    """

    __table_name__ = "boomplay_artist_track_batch_data"
    __update_key__ = ['boomplay_artist_id', 'track_id',"batch"]
    __unique_key__ = ['boomplay_artist_id', 'track_id',"batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.boomplay_artist_id = None
        self.track_id = None
        # self.source = None
        # self.gtime = kwargs.get('gtime')
        self.batch = None


class BoomplayArtistInfoBatchDataItem(UpdateItem):
    """
    7-Item说明：
        Item：歌手个人信息相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_artist_info_batch_task
        涉及数据表：boomplay_artist_info_batch_data
        涉及程序：
            crawl_boomplay_artist_info_spider.py
    """

    __table_name__ = "boomplay_artist_info_batch_data"
    __unique_key__ = ['boomplay_artist_id']
    __update_key__ = ['gmg_artist_id', 'gmg_artist_name', 'crawl_condition_boomplay_artist_id',
                      'crawl_result_boomplay_artist_id', 'boomplay_artist_id', 'crawl_condition_boomplay_artist_name',
                      'crawl_result_boomplay_artist_name', 'boomplay_artist_name', 'boomplay_artist_certification',
                      'boomplay_artist_image', 'boomplay_artist_info', 'country_region', 'batch']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None  # 来源于gmg_artist_aka提供
        self.gmg_artist_name = None  # 来源于gmg_artist_aka提供
        self.crawl_condition_boomplay_artist_id = None  # 采集条件提供的boomplay_artist_id
        self.crawl_result_boomplay_artist_id = None  # 实际采集结果的boomplay_artist_id
        self.boomplay_artist_id = None  # 与crawl_condition_boomplay_artist_id保持一致
        self.crawl_condition_boomplay_artist_name = None  # 来源于gmg_artist_aka提供的歌手名
        self.crawl_result_boomplay_artist_name = None  # 实际采集结果的boomplay_artist_name
        self.boomplay_artist_name = None  # 与crawl_result_boomplay_artist_name保持一致
        self.boomplay_artist_certification = None  # 歌手是否认证
        self.boomplay_artist_image = None  # 歌手封面
        self.boomplay_artist_info = None  # 歌手信息简介
        self.country_region = None  # 来源
        self.batch = None  # 抓取批次日期
        self.ranking_current = None
        self.ranking_alltime = None
        self.artist_favorite_count = None
        self.artist_share_count =  None
        self.artist_comment_count =  None
        # self.gtime = kwargs.get('gtime')  # 更新时间


class BoomplayArtistInfoCrawlSituationRecordBatchDataItem(UpdateItem):
    """
    8-Item说明：
        Item：歌手个人信失败原因记录 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_artist_info_batch_task
        涉及数据表：boomplay_artist_info_failed_status_reason_record_batch_data
        涉及程序：
            crawl_boomplay_artist_info_spider.py
    """
    __table_name__ = "boomplay_artist_info_crawl_situation_record_batch_data"
    __update_key__ = ["boomplay_artist_exception_info", "boomplay_artist_id", "boomplay_artist_infomation_remarks",
                      "batch"]
    __unique_key__ = ["boomplay_artist_id", "batch"]

    def __init__(self, *args, **kwargs):
        self.batch = None
        self.boomplay_artist_exception_info = None
        self.boomplay_artist_id = None
        self.boomplay_artist_infomation_remarks = None  # EI表示存在歌手信息，NI表示不存在歌手信息
        # self.boomplay_artist_infomation_rules = kwargs.get('boomplay_artist_infomation_rules')
        # self.id = kwargs.get('id')


class BoomplayArtistSongsAlbumsPlaylistsCountsRecordBatchDataItem(UpdateItem):
    """
    9-Item说明：
        Item：歌手 歌曲-专辑-播放列表记录 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_artist_info_batch_task
        涉及数据表：boomplay_artist_songs_albums_playlists_counts_record_batch_data
        涉及程序：
            crawl_boomplay_artist_songs_albums_playlists_counts_spider.py
    """

    __table_name__ = "boomplay_artist_songs_albums_playlists_counts_record_batch_data"
    __update_key__ = ['boomplay_artist_id', 'batch', 'albums_count', 'albums_count_none_info', 'songs_count',
                      'songs_count_none_info', 'playlists_count', 'playlists_count_none_info']
    __unique_key__ = ['boomplay_artist_id', 'batch']

    def __init__(self, *args, **kwargs):
        self.albums_count = None
        self.albums_count_none_info = None
        self.batch = None
        self.boomplay_artist_id = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.playlists_count = None
        self.playlists_count_none_info = None
        self.songs_count = None
        self.songs_count_none_info = None


class BoomplayArtistPlaylistBatchDataItem(UpdateItem):
    """
    10-Item说明：
        Item：歌手 播放列表映射 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_artist_info_batch_task
        涉及数据表：boomplay_artist_playlist_batch_data
        涉及程序：
            crawl_boomplay_artist_songs_albums_playlists_task_spider.py
    """

    __table_name__ = "boomplay_artist_playlist_batch_data"
    __update_key__ = ['boomplay_artist_id', 'boomplay_playlist_id', 'batch']
    __unique_key__ = ['boomplay_artist_id', 'boomplay_playlist_id', 'batch']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.boomplay_artist_id = None
        self.boomplay_playlist_id = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class BoomplayPlaylistInfoBatchTaskItem(UpdateItem):
    """
    11-Item说明：
        Item：播放列表任务 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_artist_info_batch_task
        涉及任务表：boomplay_playlist_info_batch_task
        涉及程序：
            crawl_boomplay_artist_songs_albums_playlists_task_spider.py
    """

    __table_name__ = "boomplay_playlist_info_batch_task"
    __update_key__ = ['boomplay_playlist_id']
    __unique_key__ = ['boomplay_playlist_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.boomplay_playlist_id = None
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')


class BoomplayArtistAlbumBatchDataItem(UpdateItem):
    """
    12-Item说明：
        Item：歌手-专辑任务 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_artist_info_batch_task
        涉及任务表：boomplay_playlist_info_batch_task
        涉及程序：
            crawl_boomplay_artist_songs_albums_playlists_task_spider.py
    """

    __table_name__ = "boomplay_artist_album_batch_data"
    __unique_key__ = ['boomplay_artist_id', 'album_id', "batch"]
    __update_key__ = ['boomplay_artist_id', 'album_id', "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.boomplay_artist_id = None  # boomplay歌手id
        self.album_id = None  # 歌手专辑id
        # self.gtime = kwargs.get('gtime')  # 录入时间
        self.batch = None


class BoomplayAlbumInfoCrawlSituationRecordBatchDataItem(UpdateItem):
    """
    13-Item说明：
        Item：专辑任务采集情况 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_album_info_batch_task
        涉及数据表：boomplay_album_info_crawl_situation_record_batch_data
        涉及程序：
            crawl_boomplay_album_info_spider.py
    """

    __table_name__ = "boomplay_album_info_crawl_situation_record_batch_data"
    __update_key__ = ['album_information_remarks', 'album_exception_info', 'album_id', 'batch']
    __unique_key__ = ['album_id', 'batch']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.album_id = None
        # self.information_rule = kwargs.get('information_rule')  # 记录专辑采集异常信息分类规则
        self.album_information_remarks = None  # NC表示无版权，NT表示无歌曲数据，ET表示存在歌曲数据
        self.album_exception_info = None  # 异常信息记录
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class BoomplayAlbumInfoBatchDataItem(UpdateItem):
    """
    14-Item说明：
        Item：专辑详情 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_album_info_batch_task
        涉及数据表：boomplay_album_info_batch_data
        涉及程序：
            crawl_boomplay_album_info_spider.py
    """

    __table_name__ = "boomplay_album_info_batch_data"
    __unique_key__ = ['crawl_condition_album_id']
    __update_key__ = ['album_name', 'crawl_result_album_id', 'album_type', 'album_id', 'album_image',
                      'album_track_count', 'album_info', 'album_favorite_count', 'album_share_count',
                      'album_comment_count', 'batch']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.crawl_condition_album_id = None  # 采集条件的专辑id
        self.album_id = None  # 专辑id
        self.album_name = None  # 专辑名
        self.crawl_result_album_id = None  # 采集结果的专辑id
        self.album_type = None  # 专辑类型
        self.album_image = None  # 专辑封面
        self.album_track_count = None  # 专辑下的歌曲数量
        self.album_info = None  # 专辑信息
        self.album_favorite_count = None  # 喜欢数
        self.album_share_count = None  # 分享数
        self.album_comment_count = None  # 评论数
        self.batch = None  # 批次
        # self.gtime = kwargs.get('gtime')  # 更新时间


class BoomplayAlbumTrackBatchDataItem(UpdateItem):
    """
    15-Item说明：
        Item：专辑歌曲映射 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_album_info_batch_task
        涉及数据表：boomplay_album_track_batch_data
        涉及程序：
            crawl_boomplay_album_info_spider.py
    """

    __table_name__ = "boomplay_album_track_batch_data"
    __update_key__ = ["album_id", "track_id","batch"]
    __unique_key__ = ["album_id", "track_id","batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.album_id = None
        self.track_id = None
        # self.gtime = kwargs.get('gtime')
        self.batch = None


class BoomplayTrackInfoCrawlSituationRecordBatchDataItem(UpdateItem):
    """
    16-Item说明：
        Item：专辑歌曲采集情况信息 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_track_info_batch_task
        涉及数据表：boomplay_track_info_crawl_situation_record_batch_data
        涉及程序：
            crawl_boomplay_track_info_spider.py
    """

    __table_name__ = "boomplay_track_info_crawl_situation_record_batch_data"
    __update_key__ = ["track_infomation_remarks", "track_exception_info", "track_id", "batch"]
    __unique_key__ = ["track_id", "batch"]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.track_id = None
        # self.track_infomation_rules = kwargs.get('track_infomation_rules')  # EI表示存在歌曲信息，NI表示不存在歌曲信息
        self.track_infomation_remarks = None
        self.track_exception_info = None
        self.batch = None
        # self.gtime = kwargs.get('gtime')


class BoomplayTrackInfoBatchDataItem(UpdateItem):
    """
    17-Item说明：
        Item：歌曲信息采集情况信息 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_track_info_batch_task
        涉及数据表：boomplay_track_info_batch_data
        涉及程序：
            crawl_boomplay_track_info_spider.py
    """

    __table_name__ = "boomplay_track_info_batch_data"
    __unique_key__ = ["crawl_condition__track_id"]
    __update_key__ = ["track_id", "crawl_result_track_id", "track_name", "crawl_condition_track_id",
                      "track_type", "track_image", "album_id", "duration",
                      "capture_artist_id", "capture_artist_name", "capture_artist_image", "capture_album_id",
                      ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.crawl_condition_track_id = None  # 采集条件的歌曲id
        self.crawl_result_track_id = None  # 采集结果的歌曲id
        self.track_id = None  # 与crawl_condition_track_id一致
        self.track_name = None  # 歌曲名
        self.track_type = None  # 歌曲类型
        self.track_image = None  # 歌曲封面
        self.album_id = None  # 专辑id
        self.duration = None  # 歌曲时长
        # self.boomplay_artist_id = None # 歌曲歌手id
        # self.boomplay_artist_name = None # 歌曲歌手名
        self.capture_artist_id = None  # capture_artist_id歌手id
        self.capture_artist_name = None  # capture_artist_name歌手名
        self.capture_artist_image = None  # 歌手封面
        self.capture_album_id = None  # 专辑id
        self.capture_album_name = None  # 专辑名
        self.capture_album_image = None  # 专辑封面
        self.track_favorite_count = None  # 喜欢数
        self.track_share_count = None  # 分享数
        self.track_comment_count = None  # 评论数
        self.genre = None  # 曲风
        self.publish_date = None  # 网页原字段发行年份
        self.fix_publish_date = None
        self.lyrics_url = None  # 歌词链接
        self.lyrics = None  # 歌词
        self.batch = None
        # self.ISRC = kwargs.get('ISRC')
        # self.isrc_track_name = kwargs.get('isrc_track_name')
        # self.isrc_artist_name = kwargs.get('isrc_artist_name')
        # self.isrc_genre = kwargs.get('isrc_genre')
        # self.CP = kwargs.get('CP')
        # self.Date Created = kwargs.get('Date Created')
        # self.gtime = kwargs.get('gtime')  # 更新时间


class BoomplayTrackNameCleanedDataItem(UpdateItem):
    """
    18-Item说明：
        Item：歌曲信息采集情况信息 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_track_info_batch_task
        涉及数据表：boomplay_track_name_cleaned_data
        涉及程序：
            crawl_boomplay_track_info_spider.py
    """

    __table_name__ = "boomplay_track_name_cleaned_data"
    __update_key__ = ["feat_artist_name", 'track_name_cleaned', 'track_id', 'track_name', 'version']
    __unique_key__ = ['track_id']

    def __init__(self, *args, **kwargs):
        self.feat_artist_name = None
        # self.id = kwargs.get('id')
        # self.state = kwargs.get('state')
        self.track_id = None
        self.track_name = None
        self.track_name_cleaned = None  # 歌曲名清理后
        self.version = None


class BoomplayTrackViewsBatchDataItem(UpdateItem):
    """
    19-Item说明：
        Item：歌曲播放量采集情况信息 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_track_info_batch_task
        涉及数据表：boomplay_track_views_batch_data
        涉及程序：
            crawl_boomplay_track_views_spider.py
    """

    __table_name__ = "boomplay_track_views_batch_data"
    __unique_key__ = ['track_id', 'batch']
    __update_key__ = ['track_id', 'batch', 'crawl_frequency', 'views']

    def __init__(self, *args, **kwargs):
        self.batch = None
        self.crawl_frequency = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.track_id = None
        self.views = None


class BoomplayTrackViewsCrawlSituationRecordBatchDataItem(UpdateItem):
    """
    20-Item说明：
        Item：歌曲信息采集情况信息 相关字段
        IP：192.168.10.135
        数据库名：my_music_data
        涉及任务表：boomplay_track_info_batch_task
        涉及数据表：boomplay_track_views_crawl_situation_record_batch_data
        涉及程序：
            crawl_boomplay_track_views_spider.py
    """

    __table_name__ = "boomplay_track_views_crawl_situation_record_batch_data"
    __update_key__ = ['track_id', 'track_exception_info', 'batch', 'track_views_remarks']
    __unique_key__ = ['track_id', 'batch']

    def __init__(self, *args, **kwargs):
        self.batch = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.track_exception_info = None
        self.track_id = None
        self.track_views_remarks = None  # EV表示存在歌曲播放量，NV表示不存在歌曲播放量
        # self.track_views_rules = kwargs.get('track_views_rules')
