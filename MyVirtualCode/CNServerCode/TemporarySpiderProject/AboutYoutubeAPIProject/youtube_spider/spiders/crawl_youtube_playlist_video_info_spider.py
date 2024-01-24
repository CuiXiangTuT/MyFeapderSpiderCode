# -*- coding: utf-8 -*-
"""
Created on 2023-10-08 10:26:03
---------
@summary:
---------
@author: QiuQiuRen
@description:
    IP：192.168.10.135
    数据库名：my_music_data
    采集任务表：api_youtube_artist_playlist_batch_task
    入库数据表：api_youtube_artist_playlist_batch_data
    入库任务表：api_youtube_video_batch_task
    采集目的：旨在通过YouTube API获取到的Playlist Id，将该对应下的视频Video Id进行采集
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *

class CrawlYoutubePlaylistVideoInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def add_task(self):
        update_state_sql = "UPDATE {} SET {} = 0".format(self._task_table,self._task_state)
        self._mysqldb.update(update_state_sql)

    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_youtube_playlist_id = task.youtube_playlist_id
        youtube_key = 'AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'
        yield feapder.Request(
            "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={}&key={}".format(
                task_youtube_playlist_id, youtube_key),
            task_youtube_playlist_id=task_youtube_playlist_id,
            task_id=task_id,
            youtube_key=youtube_key
            )

    def parse(self, request, response):
        # 提取网站title
        item_list = response.json['items']
        task_id = request.task_id
        for per_item in item_list:
            api_youtube_artist_playlist_batch_data_item = ApiYoutubeArtistPlaylistBatchDataItem()
            # api_youtube_video_batch_task_item = ApiYoutubeVideoBatchTaskItem()
            api_youtube_artist_playlist_batch_data_item['youtube_playlist_id'] = request.task_youtube_playlist_id
            api_youtube_artist_playlist_batch_data_item['youtube_video_id'] = per_item['snippet']['resourceId']['videoId']
            api_youtube_artist_playlist_batch_data_item['batch'] = self.batch_date
            # api_youtube_video_batch_task_item['youtube_video_id'] = per_item['snippet']['resourceId']['videoId']
            # yield api_youtube_video_batch_task_item
            yield api_youtube_artist_playlist_batch_data_item

        if response.json.get('nextPageToken'):
            next_page_token = response.json['nextPageToken']
            task_youtube_playlist_id = request.task_youtube_playlist_id
            youtube_key = request.youtube_key
            url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&maxResults=50&playlistId={}&key={}'.format(
                next_page_token, task_youtube_playlist_id, youtube_key)
            headers = {
                'Accept': 'application/json'
            }
            yield feapder.Request(url=url, headers=headers, task_youtube_playlist_id=task_youtube_playlist_id,
                                  youtube_key=youtube_key, task_id=task_id)
        yield self.update_task_state(request.task_id, 1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)

if __name__ == "__main__":
    spider = CrawlYoutubePlaylistVideoInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubePlaylistVideoInfoSpider爬虫")

    parser.add_argument(
        "--start_master",
        action="store_true",
        help="添加任务",
        function=spider.start_monitor_task,
    )
    parser.add_argument(
        "--start_worker", action="store_true", help="启动爬虫", function=spider.start
    )

    parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python crawl_youtube_playlist_video_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_playlist_video_info_spider.py --start_worker  # 启动爬虫
