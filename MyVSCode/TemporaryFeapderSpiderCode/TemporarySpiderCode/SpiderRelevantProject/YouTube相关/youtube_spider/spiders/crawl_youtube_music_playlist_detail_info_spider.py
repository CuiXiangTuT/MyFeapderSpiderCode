# -*- coding: utf-8 -*-
"""
Created on 2023-09-07 14:11:53
---------
@summary:
---------
@author: QiuQiuRen
@description：
    通过给予的YouTube Music Playlist获取其下对应的所有歌曲id
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *


class CrawlYoutubeMusicPlaylistDetailInfoSpider(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="localhost:6379",
    #     REDISDB_USER_PASS="",
    #     REDISDB_DB=0,
    #     MYSQL_IP="localhost",
    #     MYSQL_PORT=3306,
    #     MYSQL_DB="",
    #     MYSQL_USER_NAME="",
    #     MYSQL_USER_PASS="",
    # )
    def init_task(self):
        pass

    def add_task(self):
        update_state_sql = "update {task_table} SET {task_state}=0 WHERE {task_state}=-1".format(task_table=self._task_table,task_state=self._task_state)
        self._mysqldb.update(update_state_sql)

    def download_midware(self,request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_youtube_music_playlist_link = task.youtube_music_playlist_link
        task_youtube_music_playlist_id = task_youtube_music_playlist_link.split('=')[1]
        youtube_key = 'AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'
        yield feapder.Request("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={}&key={}".format(task_youtube_music_playlist_id,youtube_key),
            task_youtube_music_playlist_id=task_youtube_music_playlist_id,
            task_youtube_music_playlist_link=task_youtube_music_playlist_link,
            task_id=task_id,
            youtube_key=youtube_key
        )

    def parse(self, request, response):
        # 提取网站title
        item_list = response.json['items']
        task_id = request.task_id
        for per_item in item_list:
            # YouTube Music Playlist Data数据表
            youtube_music_playlist_batch_data_item = YoutubeMusicPlaylistBatchDataItem()
            # Youtube Video Task任务表
            youtube_video_link_info_batch_task_item = YoutubeVideoLinkInfoBatchTaskItem()
            youtube_music_playlist_batch_data_item['youtube_music_playlist_id'] = request.task_youtube_music_playlist_id
            youtube_music_playlist_batch_data_item['youtube_music_video_id'] = per_item['snippet']['resourceId']['videoId']
            youtube_music_playlist_batch_data_item['youtube_music_playlist_link'] = request.task_youtube_music_playlist_link
            youtube_music_playlist_batch_data_item['youtube_music_video_link'] = "https://www.youtube.com/watch?v="+per_item['snippet']['resourceId']['videoId']
            youtube_music_playlist_batch_data_item['batch'] = self.batch_date
            youtube_video_link_info_batch_task_item['youtube_video_link'] = "https://www.youtube.com/watch?v="+per_item['snippet']['resourceId']['videoId']
            yield youtube_music_playlist_batch_data_item
            yield youtube_video_link_info_batch_task_item
            # yield self.add_new_task('youtube_video_batch_task',youtube_video_batch_task_item.to_dict)
        if response.json.get('nextPageToken'):
            next_page_token = response.json['nextPageToken']
            task_youtube_playlist_id = request.task_youtube_music_playlist_id
            youtube_key = request.youtube_key
            url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&maxResults=50&playlistId={}&key={}'.format(next_page_token,task_youtube_music_playlist_id,youtube_key)
            headers = {
            'Accept': 'application/json'
            }
            yield feapder.Request(url=url,headers=headers,
                task_youtube_music_playlist_id=task_youtube_music_playlist_id,
                task_youtube_music_playlist_link=task_youtube_music_playlist_link,
                task_id=task_id,
                youtube_key=youtube_key)
        yield self.update_task_state(request.task_id, 1)


if __name__ == "__main__":
    spider = CrawlYoutubeMusicPlaylistDetailInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeMusicPlaylistDetailInfoSpider爬虫")

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
    # python crawl_youtube_music_playlist_detail_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_music_playlist_detail_info_spider.py --start_worker  # 启动爬虫
