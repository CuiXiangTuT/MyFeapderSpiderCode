# -*- coding: utf-8 -*-
"""
Created on 2023-11-08 10:56:57
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder.db.mysqldb import MysqlDB



class UpdateBoomplayTrackInfoIsrcSpider(feapder.AirSpider):
    def __init__(self):
        self.db = MysqlDB()


    def download_midware(self, request):
        request.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        return request

    def start_requests(self):
        url = "https://www.baidu.com/"
        yield feapder.Request(url=url)

    def parse(self, request, response):
        if response.status_code == 200:
            update_sql = """
            UPDATE boomplay_track_info_batch_data a
            INNER JOIN boomplay_isrc_track b
            ON a.crawl_track_id = b.track_id
            SET a.`ISRC`=b.`ISRC`,a.`isrc_track_name`=b.`track_name`,a.`isrc_artist_name`=b.`artist_name`,a.`isrc_genre`=b.`Genre`,a.`CP`=b.`CP`,a.`Date Created`=b.`Date Created`
            """
            self.db.update(update_sql)
        else:
            self.start_requests()


if __name__ == "__main__":
    UpdateBoomplayTrackInfoIsrcSpider().start()
