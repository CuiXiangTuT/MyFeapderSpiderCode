# -*- coding: utf-8 -*-
"""
Created on 2023-08-18 16:54:19
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from feapder.utils.webdriver import WebDriver
import re
import time
from items.youtube_info_item import *


class YoutubeVideoViewsInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def my_init_task(self):
        sql = "update {task_table} set {state} = 0 where {state} != -1".format(
            task_table=self._task_table,
            state=self._task_state,
        )
        return self._mysqldb.update(sql)


    def add_task(self):
        update_state_sql = "UPDATE youtube_video_batch_task SET {} = 0 WHERE {} = -1".format(self._task_state,self._task_state)
        self._mysqldb.update(update_state_sql)

    def download_midware(self,request):
        request.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_youtube_video_id = task.youtube_video_id
        task_id = task.id
        yield feapder.Request("https://www.youtube.com/watch?v={}".format(task_youtube_video_id),
        task_youtube_video_id=task_youtube_video_id,
        task_id=task_id
        )

    def parse(self, request, response):
        youtube_video_batch_data_item = YoutubeVideoBatchDataItem()

        res = response.text

        if 'likeCount' in res or 'viewCount' in res:
            like_count = re.findall(r'\"likeCount\":\"(.*?)\"',res)[0]
            view_count = re.findall(r'\"viewCount\":\"(.*?)\"',res)[0]


            youtube_video_batch_data_item['youtube_video_id'] = request.task_youtube_video_id
            youtube_video_batch_data_item['views'] = view_count
            youtube_video_batch_data_item['like_count'] = like_count
            youtube_video_batch_data_item['batch'] = self.batch_date
            # response.close_browser(request)
            yield youtube_video_batch_data_item
            yield self.update_task_state(request.task_id, 1)
        else:
            yield self.update_task_state(request.task_id, -1)
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)  



if __name__ == "__main__":
    spider = YoutubeVideoViewsInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="YoutubeVideoViewsInfoSpider爬虫")

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
    # python youtube_video_views_info_spider.py --start_master  # 添加任务
    # python youtube_video_views_info_spider.py --start_worker  # 启动爬虫
