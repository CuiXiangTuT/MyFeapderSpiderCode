# -*- coding: utf-8 -*-
"""
Created on 2023-10-07 18:23:06
---------
@summary:
---------
@author: QiuQiuRen
@description:
    IP：192.168.10.135
    数据库名：my_music_data
    采集任务表：api_youtube_artist_channel_id_batch_task
    入库数据表：api_youtube_artist_channel_id_batch_data
    入库任务表：api_youtube_artist_playlist_batch_task
    采集目的：
        旨在通过YouTube前端页面显示提供的艺人Channel Id，经YouTube API获取艺人下的所有播放列表id及部分附属信息
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *


class CrawlYoutubeArtistPlaylistInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def add_task(self):
        update_state_sql = "UPDATE {} SET {} = 0".format(self._task_table, self._task_state)
        self._mysqldb.update(update_state_sql)

    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self, task):
        youtube_key = 'AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'
        task_id = task.id
        task_youtube_artist_channel_id = task.youtube_artist_channel_id
        yield feapder.Request(
            url='https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&maxResults=50&key={}'.format(
                task_youtube_artist_channel_id, youtube_key),
            task_id=task_id,
            task_youtube_artist_channel_id=task_youtube_artist_channel_id,
            youtube_key=youtube_key
        )

    def parse(self, request, response):

        items_list = response.json['items']
        task_id = request.task_id
        for per_item in items_list:
            api_youtube_artist_channel_id_batch_data_item = ApiYoutubeArtistChannelIdBatchDataItem()
            api_youtube_artist_playlist_batch_task_item = ApiYoutubeArtistPlaylistBatchTaskItem()
            api_youtube_artist_channel_id_batch_data_item[
                'crawl_condition_youtube_artist_channel_id'] = request.task_youtube_artist_channel_id
            api_youtube_artist_playlist_batch_task_item[
                'crawl_condition_youtube_artist_channel_id'] = request.task_youtube_artist_channel_id
            api_youtube_artist_channel_id_batch_data_item['crawl_result_youtube_artist_channel_id'] = \
            per_item['snippet'][
                'channelId']
            api_youtube_artist_channel_id_batch_data_item['youtube_playlist_id'] = per_item['id']
            api_youtube_artist_playlist_batch_task_item['youtube_playlist_id'] = per_item['id']
            api_youtube_artist_channel_id_batch_data_item['title'] = per_item['snippet']['title']
            api_youtube_artist_channel_id_batch_data_item['publish_date'] = per_item['snippet']['publishedAt'].replace(
                'T',
                ' ').replace(
                'Z', ' ')
            api_youtube_artist_channel_id_batch_data_item['batch'] = self.batch_date
            yield api_youtube_artist_channel_id_batch_data_item
            yield api_youtube_artist_playlist_batch_task_item
        if response.json.get('nextPageToken'):
            next_page_token = response.json['nextPageToken']
            task_youtube_artist_channel_id = request.task_youtube_artist_channel_id
            youtube_key = request.youtube_key
            url = 'https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&pageToken={}&channelId={}&maxResults=50&key={}'.format(
                next_page_token, task_youtube_artist_channel_id, youtube_key)
            headers = {
                'Accept': 'application/json'
            }
            yield feapder.Request(url=url, headers=headers, callback=self.parse,
                                  task_youtube_artist_channel_id=task_youtube_artist_channel_id,
                                  youtube_key=youtube_key, task_id=task_id)
        yield self.update_task_state(request.task_id, 1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlYoutubeArtistPlaylistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeArtistPlaylistInfoSpider爬虫")

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
    # python crawl_youtube_artist_playlist_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_artist_playlist_info_spider.py --start_worker  # 启动爬虫
