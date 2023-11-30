# -*- coding: utf-8 -*-
"""
Created on 2023-08-21 16:49:34
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
import re


class YoutubeShortsLikesInfoSpider(feapder.BatchSpider):
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
        update_state_sql = "UPDATE youtube_shorts_video_likes_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
        # update_state_sql = "UPDATE youtube_shorts_video_likes_batch_task SET {} = 0".format(self._task_state)
        self._mysqldb.update(update_state_sql)


    def download_midware(self,request):
        request.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_youtube_artist_channel_id = task.youtube_artist_channel_id
        task_youtube_artist_name = task.youtube_artist_name
        task_youtube_shorts_id = task.youtube_shorts_id
        if task_youtube_shorts_id == '-':
            pass
        else:
            yield feapder.Request("https://www.youtube.com/shorts/{}".format(task_youtube_shorts_id),
            task_youtube_artist_channel_id=task_youtube_artist_channel_id,
            task_id=task_id,
            task_youtube_artist_name=task_youtube_artist_name,
            task_youtube_shorts_id=task_youtube_shorts_id
            )

    def parse(self, request, response):
        youtube_shorts_video_likes_batch_data_item = YoutubeShortsVideoLikesBatchDataItem()
        likes = re.findall(r'"likeCountWithLikeText":\{(.*?)\}',response.text)[0].split('"label":"')[1].split('likes')[0].strip().replace(',','')
        youtube_shorts_video_likes_batch_data_item['youtube_artist_channel_id']=request.task_youtube_artist_channel_id
        youtube_shorts_video_likes_batch_data_item['youtube_artist_name']=request.task_youtube_artist_name
        youtube_shorts_video_likes_batch_data_item['youtube_shorts_id']=request.task_youtube_shorts_id
        youtube_shorts_video_likes_batch_data_item['youtube_shorts_video_likes']=likes
        youtube_shorts_video_likes_batch_data_item['batch'] = self.batch_date
        yield youtube_shorts_video_likes_batch_data_item
        yield self.update_task_state(request.task_id, 1)
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)  



if __name__ == "__main__":
    spider = YoutubeShortsLikesInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="YoutubeShortsLikesInfoSpider爬虫")

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
    # python youtube_shorts_likes_info_spider.py --start_master  # 添加任务
    # python youtube_shorts_likes_info_spider.py --start_worker  # 启动爬虫
