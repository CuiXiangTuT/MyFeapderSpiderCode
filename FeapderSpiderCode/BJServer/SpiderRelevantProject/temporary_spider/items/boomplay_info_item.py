# -*- coding: utf-8 -*-
"""
Created on 2023-05-18 17:19:59
---------
@summary:
---------
@author: QiuQiuRen
"""

from feapder import Item,UpdateItem


class ChartDataDailyBoomplayItem(UpdateItem):
    """
    说明：Boomplay榜单数据表【chart_data_daily_boomplay】
    作用：用于存放每日抓取的榜单歌曲表信息
    """

    __table_name__ = "chart_data_daily_boomplay"
    __unique_key__ = ['rank','song_id','crawl_chart_country','batch','note']
    __update_key__ = [
        'album_id',
        'album_name',
        'chart_artist_id',
        'chart_artist_name',
        'chart_language',
        'chart_name',
        'chart_region',
        'chart_release_date',
        'chart_segment',
        'chart_site',
        'chart_type',
        'duration',
        'ranking_state_change',
        'song_name',
        'update_frequency',
        'note'
    ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.rank = None  # 榜单歌曲排名
        self.song_id = None  # 榜单歌曲id
        self.song_name = None  # 榜单歌曲名
        self.chart_artist_id = None  # 榜单歌手id
        self.chart_artist_name = None  # 榜单歌手名
        self.album_id = None  # 榜单专辑id
        self.album_name = None # 榜单专辑名
        self.duration = None # 歌曲时长
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
        self.note = None


class BoomplayArtistInfoBatchTaskItem(UpdateItem):
    """
    说明：Boomplay歌手任务表：boomplay_artist_info_batch_task
    作用：用于存放新的歌手id
    """

    __table_name__ = "boomplay_artist_info_batch_task"
    __update_key__ = ['boomplay_artist_name','gmg_artist_id','gmg_artist_name']
    __unique_key__ = ['boomplay_artist_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None
        self.gmg_artist_name = None  # gmg_artist_aka中的字段
        self.boomplay_artist_id = None  # 榜单抓取过来的歌手id
        self.boomplay_artist_name = None  # 榜单抓取过来的歌手名
        # self.state = kwargs.get('state')  # 抓取歌手信息时使用的状态字段state
        # self.usable = kwargs.get('usable')  # boomplay_artist_id是否可用（gmg_artist_aka表中不存在的数据被认为不可用）
        # self.parser_name = kwargs.get('parser_name')
        # self.insert_date = kwargs.get('insert_date')  # 更新时间
        # self.artist_album_track_state = kwargs.get('artist_album_track_state')  # 抓取歌手的歌曲、专辑任务时使用的状态字段


class BoomplayArtistInfoBatchDataItem(UpdateItem):
    """
    说明：Boomplay歌手信息表【boomplay_artist_info_batch_data】
    作用：用于存储歌手信息数据
    """

    __table_name__ = "boomplay_artist_info_batch_data"
    __unique_key__ = ['crawl_boomplay_artist_id']
    __update_key__ = [
        'gmg_artist_id',
        'gmg_artist_name',
        'boomplay_artist_name',
        'crawl_boomplay_artist_id',
        'boomplay_artist_id',
        'crawl_artist_name',
        'boomplay_artist_certification',
        'batch',
        'boomplay_artist_image',
        'boomplay_artist_info',
        'ranking_current',
        'ranking_alltime',
        'country_region',
        'artist_favorite_count',
        'artist_share_count',
        'artist_comment_count'
    ]


    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.gmg_artist_id = None # gmg歌手id
        self.gmg_artist_name = None  # gmg歌手名
        self.boomplay_artist_name = None  # 抓取到的boomplay歌手名
        self.crawl_boomplay_artist_id = None  # 抓取的boomplay_artist_id
        self.boomplay_artist_id = None  # 实际上boomplay歌手id
        self.crawl_artist_name = None  # boomplay歌手名
        self.boomplay_artist_certification = None  # 歌手认证
        self.batch = None  # 抓取批次日期
        self.boomplay_artist_image = None  # 歌手封面
        self.boomplay_artist_info = None  # 歌手信息
        self.ranking_current = None  # 当前排名
        self.ranking_alltime = None  # 持续排名
        self.country_region = None  # 来源
        self.artist_favorite_count = None  # 喜欢数
        self.artist_share_count = None  # 分享数
        self.artist_comment_count = None  # 评论数
        # self.gtime = kwargs.get('gtime')  # 更新时间

class BoomplayArtistAlbumBatchDataItem(UpdateItem):
    """
    说明：Boomplay歌手专辑映射表【boomplay_artist_album_batch_data】
    作用：用于存储歌手与专辑之间的关联关系
    """

    __table_name__ = "boomplay_artist_album_batch_data"
    __unique_key__ = ['boomplay_artist_id','album_id']
    __update_key__ = ['boomplay_artist_id','album_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.boomplay_artist_id = None  # boomplay歌手id
        self.album_id = None  # 歌手专辑id
        # self.gtime = kwargs.get('gtime')  # 录入时间


class BoomplayArtistTrackBatchDataItem(UpdateItem):
    """
    说明：Boomplay歌手歌曲映射表【boomplay_artist_track_batch_data】
    作用：用于存储歌手与歌曲之间的映射关系
    """

    __table_name__ = "boomplay_artist_track_batch_data"
    __unique_key__ = ['boomplay_artist_id','track_id']
    __update_key__ = ['boomplay_artist_id','track_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.boomplay_artist_id = None
        self.track_id = None
        # self.gtime = kwargs.get('gtime')

class BoomplayAlbumInfoBatchTaskItem(UpdateItem):
    """
    说明：Boomplay专辑任务表【boomplay_album_info_batch_task】
    作用：用于存储专辑任务数据
    """

    __table_name__ = "boomplay_album_info_batch_task"
    __unique_key__ = ['album_id']
    __update_key__ = ['album_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.album_id = None  # 专辑id
        # self.state = kwargs.get('state')
        # self.gtime = kwargs.get('gtime')  # 更新时间
        # self.parser_name = kwargs.get('parser_name')


class BoomplayAlbumInfoBatchDataItem(UpdateItem):
    """
    说明：Boomplay专辑信息表【boomplay_album_info_batch_data】
    作用：用于存储专辑信息数据
    """

    __table_name__ = "boomplay_album_info_batch_data"
    __unique_key__ = ['album_id']
    __update_key__ = [
        'crawl_album_id',
        'album_id',
        'album_name',
        'album_type',
        'album_image',
        'album_track_count',
        'album_info',
        'boomplay_artist_id',
        'album_favorite_count',
        'album_share_count',
        'album_comment_count',
        'batch'
    ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.crawl_album_id = None  # 抓取使用的专辑id
        self.album_id = None # 专辑id
        self.album_name = None # 专辑名
        self.album_type = None  # 专辑类型
        self.album_image = None  # 专辑封面
        self.album_track_count = None  # 专辑下的歌曲数量
        self.album_info = None  # 专辑信息
        self.boomplay_artist_id = None  # 歌手id
        self.album_favorite_count = None  # 喜欢数
        self.album_share_count = None  # 分享数
        self.album_comment_count = None  # 评论数
        self.batch = None  # 批次
        # self.gtime = kwargs.get('gtime')  # 更新时间

class BoomplayTrackInfoBatchTaskItem(UpdateItem):
    """
    说明：Boomplay歌曲任务表【boomplay_track_info_batch_task】
    作用：用于存储歌曲任务数据
    """

    __table_name__ = "boomplay_track_info_batch_task"
    __unique_key__ = ['track_id']
    __update_key__ = ['track_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.track_id = None  # 歌曲id
        # self.gtime = kwargs.get('gtime')  # 更新时间
        # self.parser_name = kwargs.get('parser_name')
        # self.state = kwargs.get('state')
        # self.views_state = kwargs.get('views_state')

class BoomplayTrackInfoBatchDataItem(UpdateItem):
    """
    说明：Boomplay歌曲信息表【boomplay_track_info_batch_data】
    作用：用于存储歌曲信息数据
    """

    __table_name__ = "boomplay_track_info_batch_data"
    __unique_key__ = ['track_id']
    __update_key__ = [
        'crawl_track_id',
        'track_id',
        'track_name',
        'track_type',
        'track_image',
        'album_id',
        'duration',
        'boomplay_artist_id',
        'boomplay_artist_name',
        'capture_artist_id',
        'capture_artist_name',
        'capture_artist_image',
        'capture_album_id',
        'capture_album_name',
        'capture_album_image',
        'track_favorite_count',
        'track_share_count',
        'track_comment_count',
        'genre',
        'publish_date',
        'lyrics_url',
        'lyrics',
        'batch'
    ]

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.crawl_track_id = None  # 抓取的歌曲id
        self.track_id = None  # 歌曲id
        self.track_name = None  # 歌曲名
        self.track_type = None  # 歌曲类型
        self.track_image = None  # 歌曲封面
        self.album_id = None  # 专辑id
        self.duration = None  # 歌曲时长
        self.boomplay_artist_id = None  # 歌曲歌手id
        self.boomplay_artist_name = None  # 歌曲歌手名
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
        self.publish_date = None  # 发行年份
        self.lyrics_url = None  # 歌词链接
        self.lyrics = None  # 歌词
        self.batch = None
        # self.gtime = kwargs.get('gtime')  # 更新时间
        # self.ISRC = kwargs.get('ISRC')
        # self.isrc_track_name = kwargs.get('isrc_track_name')
        # self.isrc_artist_name = kwargs.get('isrc_artist_name')
        # self.isrc_genre = kwargs.get('isrc_genre')
        # self.CP = kwargs.get('CP')
        # self.Date Created = kwargs.get('Date Created')

class BoomplayAlbumTrackBatchDataItem(UpdateItem):
    """
    说明：Boomplay专辑歌曲映射表【boomplay_album_track_batch_data】
    作用：用于存储专辑-歌曲映射关系
    """

    __table_name__ = "boomplay_album_track_batch_data"
    __unique_key__ = ['album_id','track_id']
    __update_key__ = ['album_id','track_id']

    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.album_id = None
        self.track_id = None
        # self.gtime = kwargs.get('gtime')

class BoomplayTrackViewsBatchDataItem(UpdateItem):
    """
    说明：Boomplay歌曲播放量数据表【boomplay_track_views_batch_data】
    作用：用于存储歌曲播放量
    """

    __table_name__ = "boomplay_track_views_batch_data"
    __unique_key__ = ['track_id','batch','crawl_frequency']
    __update_key__ = ['track_id','batch','crawl_frequency','views']


    def __init__(self, *args, **kwargs):
        # self.id = kwargs.get('id')
        self.track_id = None
        self.views = None
        self.batch = None
        self.crawl_frequency = None
        # self.gtime = kwargs.get('gtime')

# class BoomplayTrackViewsBatchDataAfItem(UpdateItem):
#     """
#     This class was generated by feapder
#     command: feapder create -i boomplay_track_views_batch_data_af 1
#     """

#     __table_name__ = "boomplay_track_views_batch_data_af"
#     __unique_key__ = ['track_id','batch','crawl_frequency']
#     __update_key__ = ['track_id','batch','crawl_frequency','views']

#     def __init__(self, *args, **kwargs):
#         # self.id = kwargs.get('id')
#         self.track_id = kwargs.get('track_id')
#         self.views = kwargs.get('views')
#         self.batch = kwargs.get('batch')
#         self.crawl_frequency = kwargs.get('crawl_frequency')
#         # self.gtime = kwargs.get('gtime')

# class BoomplayTrackViewsBatchDataBjItem(UpdateItem):
#     """
#     This class was generated by feapder
#     command: feapder create -i boomplay_track_views_batch_data_bj 1
#     """

#     __table_name__ = "boomplay_track_views_batch_data_bj"
#     __unique_key__ = ['track_id','batch','crawl_frequency']
#     __update_key__ = ['track_id','batch','crawl_frequency','views']

#     def __init__(self, *args, **kwargs):
#         # self.id = kwargs.get('id')
#         self.track_id = kwargs.get('track_id')
#         self.views = kwargs.get('views')
#         self.batch = kwargs.get('batch')
#         self.crawl_frequency = kwargs.get('crawl_frequency')
#         # self.gtime = kwargs.get('gtime')

