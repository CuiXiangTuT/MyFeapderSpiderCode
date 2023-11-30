# -*- coding: utf-8 -*-
"""
Created on 2023-08-18 15:41:56
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
from feapder.utils import tools
from feapder.utils.log import log


class YoutubeGetVideoInfoSpider(feapder.BatchSpider):


    def init_task(self):
        pass

    def add_task(self):
        # update_state_sql = "UPDATE youtube_artist_playlist_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
        update_state_sql = "UPDATE youtube_artist_playlist_batch_task SET {} = 0".format(self._task_state)
        self._mysqldb.update(update_state_sql)

    def download_midware(self,request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_youtube_playlist_id = task.youtube_playlist_id
        youtube_key = 'AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'
        yield feapder.Request("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={}&key={}".format(task_youtube_playlist_id,youtube_key),
            task_youtube_playlist_id=task_youtube_playlist_id,
            task_id=task_id,
            youtube_key=youtube_key
        )

    def parse(self, request, response):
        # 提取网站title
        item_list = response.json['items']
        task_id = request.task_id
        for per_item in item_list:
            youtube_artist_playlist_batch_data_item = YoutubeArtistPlaylistBatchDataItem()
            youtube_video_batch_task_item = YoutubeVideoBatchTaskItem()
            youtube_artist_playlist_batch_data_item['youtube_playlist_id'] = request.task_youtube_playlist_id
            youtube_artist_playlist_batch_data_item['youtube_video_id'] = per_item['snippet']['resourceId']['videoId']
            youtube_artist_playlist_batch_data_item['batch'] = self.batch_date
            youtube_video_batch_task_item['youtube_video_id'] = per_item['snippet']['resourceId']['videoId']
            yield youtube_video_batch_task_item
            yield youtube_artist_playlist_batch_data_item
            # yield self.add_new_task('youtube_video_batch_task',youtube_video_batch_task_item.to_dict)
        if response.json.get('nextPageToken'):
            next_page_token = response.json['nextPageToken']
            task_youtube_playlist_id = request.task_youtube_playlist_id
            youtube_key = request.youtube_key
            url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&maxResults=50&playlistId={}&key={}'.format(next_page_token,task_youtube_playlist_id,youtube_key)
            headers = {
            'Accept': 'application/json'
            }
            yield feapder.Request(url=url,headers=headers,task_youtube_playlist_id=task_youtube_playlist_id,youtube_key=youtube_key,task_id=task_id)
        yield self.update_task_state(request.task_id, 1)
    
    # def add_new_task(self, table,data):
    #     sql = tools.make_insert_sql(
    #         table, data,insert_ignore=True
    #     )
    #     if self._mysqldb.update(sql):
    #         log.debug("添加任务成功: %s" % sql)
    #     else:
    #         log.error("添加任务失败") 
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)  


if __name__ == "__main__":
    spider = YoutubeGetVideoInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="YoutubeGetVideoInfoSpider爬虫")

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
    # python youtube_get_video_info_spider.py --start_master  # 添加任务
    # python youtube_get_video_info_spider.py --start_worker  # 启动爬虫
