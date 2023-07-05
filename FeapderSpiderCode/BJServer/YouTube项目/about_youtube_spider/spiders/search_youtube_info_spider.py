# -*- coding: utf-8 -*-
"""
Created on 2023-05-19 19:57:21
---------
@summary:
---------
@author: AirWolf
"""

import feapder
from feapder import ArgumentParser
from items.search_youtube_info_data_item import *


class SearchYoutubeInfoSpider(feapder.BatchSpider):

    def add_task(self):
        sql_truncate_table = """
        TRUNCATE TABLE search_youtube_info_data
        """
        self._mysqldb.execute(sql_truncate_table)

        sql_update_state = """
        UPDATE search_youtube_info_task
        SET state = 0
        WHERE state = -1
        """
        self._mysqldb.update(sql_update_state)

    def download_midware(self, request):
        request.headers = {'Accept': 'application/json'}
        return request

    def start_requests(self, task):
        task_id = task.id
        task_artist_id = task.artist_id
        task_artist_name = task.artist_name
        task_track_id = task.track_id
        task_track_name = task.track_name
        yield feapder.Request(
            "https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={}&key=AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g"
            .format(task_track_name + ' ' + task_artist_name),
            task_artist_id=task_artist_id,
            task_artist_name=task_artist_name,
            task_track_id=task_track_id,
            task_track_name=task_track_name,
            task_id=task_id)

    def parse(self, request, response):
        youtube_info = SearchYoutubeInfoDataItem()
        info = response.json['items'][0]
        # etag
        youtube_info['etag'] = info['etag']
        # kind
        youtube_info['kind'] = info['id']['kind']
        # video_id
        youtube_info['youtube_video_id'] = info['id']['videoId']
        # youtube_link
        youtube_info[
            'youtube_link'] = 'https://www.youtube.com/watch?v=' + info['id'][
                'videoId']
        # 发布时间
        youtube_info['publish_time'] = info['snippet']['publishTime']
        # channelTitle
        youtube_info['youtube_channel_title'] = info['snippet']['channelTitle']
        # channelId
        youtube_info['youtube_channel_id'] = info['snippet']['channelId']
        # youtube_title
        youtube_info['youtube_title'] = info['snippet']['title']
        yield feapder.Request(
            'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key=AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'
            .format(youtube_info['youtube_video_id']),
            task_artist_id=request.task_artist_id,
            task_artist_name=request.task_artist_name,
            task_track_id=request.task_track_id,
            task_track_name=request.task_track_name,
            youtube_info=youtube_info,
            callback=self.parse_views)
        yield self.update_task_state(request.task_id, 1)

    def parse_views(self, request, response):
        views = response.json['items'][0]['statistics']['viewCount']
        youtube_info = request.youtube_info
        youtube_info['views'] = views
        print(youtube_info)
        yield youtube_info


if __name__ == "__main__":
    spider = SearchYoutubeInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="SearchYoutubeInfoSpider爬虫")

    parser.add_argument(
        "--start_master",
        action="store_true",
        help="添加任务",
        function=spider.start_monitor_task,
    )
    parser.add_argument("--start_worker",
                        action="store_true",
                        help="启动爬虫",
                        function=spider.start)

    parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python search_youtube_info_spider.py --start_master  # 添加任务
    # python search_youtube_info_spider.py --start_worker  # 启动爬虫
