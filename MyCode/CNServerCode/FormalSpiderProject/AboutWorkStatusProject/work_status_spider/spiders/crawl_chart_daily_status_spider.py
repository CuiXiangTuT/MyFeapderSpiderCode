# -*- coding: utf-8 -*-
"""
Created on 2023-11-03 10:48:06
---------
@summary:
---------
@author: QiuQiuRen
@description：
    旨在更新当前work_status.chart_daily_status表数据
"""

import feapder
from feapder.db.mysqldb import MysqlDB
from setting import *

class CrawlChartDailyStatusSpider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        return request

    def start_requests(self):
        url = "https://www.baidu.com/"
        yield feapder.Request(url=url)

    def parse(self, request, response):
        """
        batch 						：跟随当日榜单数据的日期
        week 						：默认空
        tasks 						：默认空
        chart_daily 				：当日采集Spotify榜单数量
                                      SELECT COUNT(1) FROM music_data.chart_data_daily WHERE batch="日期"
        spotify_listeners 			：当日采集spotify_artist_info_batch_data条目数
                                      SELECT batch,COUNT(1) FROM spotify_artist_info_batch_data WHERE batch="日期"
        spotify_album 				：默认 -
        spotify_track 				：默认 -
        spotify_track_views 		：默认 -
        gmg_track_youtube_views 	：默认 -
        gmg_label_youtube_views 	：默认 -
        :param request:
        :param response:
        :return:
        """
        insert_sql = """
        INSERT INTO work_status.chart_daily_status(
        batch,`week`,tasks,chart_daily,spotify_listeners,spotify_album,spotify_track,spotify_track_views,gmg_track_youtube_views,gmg_label_youtube_views
        )
        SELECT
        a.a_batch AS batch
        ,NULL AS `week`
        ,"听众、日榜" AS tasks
        ,a.c1 AS chart_daily
        ,b.c2 AS spotify_listeners
        ,'-' AS spotify_album
        ,'-' AS spotify_track
        ,'-' AS spotify_track_views
        ,'-' AS gmg_track_youtube_views
        ,'-' AS gmg_label_youtube_views
        FROM (
        (SELECT batch AS a_batch,COUNT(1) AS c1 FROM music_data.chart_data_daily WHERE batch>CURRENT_DATE ) a 
        INNER JOIN (
        SELECT batch AS b_batch,COUNT(1) AS c2 FROM music_data.spotify_artist_info_batch_data WHERE batch>CURRENT_DATE 
        ) b 
        ON a.a_batch = b.b_batch
        );
        """
        db = MysqlDB()
        db.add(insert_sql)
        print("香港添加数据成功")

        # 北京数据库
        bj_db = MysqlDB(
            ip=BJ_SERVER_MYSQL_IP, port=BJ_SERVER_MYSQL_PORT, db=BJ_SERVER_MYSQL_DB,
            user_name=BJ_SERVER_MYSQL_USER_NAME, user_pass=BJ_SERVER_MYSQL_USER_PASS
        )
        bj_db.add(insert_sql)
        print("北京添加数据成功")


if __name__ == "__main__":
    CrawlChartDailyStatusSpider().start()
