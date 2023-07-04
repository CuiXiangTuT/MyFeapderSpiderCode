# -*- coding: utf-8 -*-
"""
Created on 2023-05-22 10:33:14
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.search_youtube_info_data_item import SearchYoutubeInfoDataItem


class GetYoutubeInfoViewsSpider(feapder.BatchSpider):
    def add_task(self):
        update_state_sql = """
        UPDATE search_youtube_info_task
        SET state = 0
        """
        self._mysqldb.update(update_state_sql)

    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_artist_id = task.artist_id
        task_artist_name = task.artist_name
        task_track_id = task.track_id
        task_track_name = task.track_name
        yield feapder.Request("https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={}&key=AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g".format(task_track_name,task_artist_name),
            task_id=task_id,
            task_artist_id=task_artist_id,
            task_artist_name=task_artist_name,
            task_track_id=task_track_id,
            task_track_name=task_track_name
        )

    def parse(self, request, response):
        youtube_info = SearchYoutubeInfoDataItem()
        res = response.json['items'][0]
        youtube_info['artist_id'] = request.task_artist_id
        youtube_info['artist_name'] = request.task_artist_name
        youtube_info['track_id'] = request.task_track_id
        youtube_info['track_name'] = request.task_track_name
        # etag
        youtube_info['etag'] = res['etag']
        # kind
        youtube_info['kind'] = res['id']['kind']
        # video_id
        youtube_info['youtube_video_id'] = res['id']['videoId']
        # youtube_link
        youtube_info['youtube_link'] = 'https://www.youtube.com/watch?v='+res['id']['videoId']
        # 发布时间
        youtube_info['publish_time'] = res['snippet']['publishTime']
        # channelTitle
        youtube_info['youtube_channel_title'] = res['snippet']['channelTitle']
        # channelId
        youtube_info['youtube_channel_id'] = res['snippet']['channelId']
        # youtube_title
        youtube_info['youtube_title'] = res['snippet']['title']
        view_url = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key=AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'.format(youtube_info['youtube_video_id'])
        headers = {
            'Accept': 'application/json'
        }
        yield feapder.Request(url=view_url,headers=headers,youtube_info=youtube_info,callback=self.parse_views)
        
    
    def parse_views(self,request,response):
        youtube_info = request.youtube_info
        youtube_info['views'] = response.json['items'][0]['statistics']['viewCount']
        youtube_info['batch'] = self.batch_date
        yield youtube_info
        yield self.update_task_batch(request.task_id, 1) 



if __name__ == "__main__":
    spider = GetYoutubeInfoViewsSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="GetYoutubeInfoViewsSpider爬虫")

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
    # python get_youtube_info_views_spider.py --start_master  # 添加任务
    # python get_youtube_info_views_spider.py --start_worker  # 启动爬虫
