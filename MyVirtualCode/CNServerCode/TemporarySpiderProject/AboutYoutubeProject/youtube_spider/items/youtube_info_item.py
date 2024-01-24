from feapder import UpdateItem


class TemporarySearchYoutubeInfoBatchDataItem(UpdateItem):

    __table_name__ = "temporary_search_youtube_info_batch_data"
    __unique_key__ = ["artist_id","track_id"]
    __update_key__ = ["artist_name","batch","description","duration","publish_date","track_name","views","youtube_channel_id","youtube_channel_name","youtube_link","youtube_title","youtube_video_id"]

    def __init__(self, *args, **kwargs):
        self.artist_id = None
        self.artist_name = None
        self.batch = None
        self.description = None
        self.duration = None
        # self.gtime = kwargs.get('gtime')
        # self.id = kwargs.get('id')
        self.publish_date = None
        self.track_id = None
        self.track_name = None
        self.views = None
        self.youtube_channel_id = None
        self.youtube_channel_name = None
        self.youtube_link = None
        self.youtube_title = None
        self.youtube_video_id = None
