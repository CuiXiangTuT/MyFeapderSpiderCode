# -*- coding: utf-8 -*-
"""
Created on 2023-09-07 01:31:21
---------
@summary:
---------
@author: AirWolf
@Description：
    获取其YouTube LinK页面信息，包括YouTube Link、Title、Channel Id、Views
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
import re
import json


class CrawlYoutubeLinkInfoSpider(feapder.BatchSpider):

    def init_task(self):
        pass

    # def add_task(self):
    #     update_state_sql = "update {task_table} SET {task_state}=0 WHERE {task_state}=-1".format(task_table=self._task_table,task_state=self._task_state)
    #     self._mysqldb.update(update_state_sql)

    def start_requests(self, task):
        task_id = task.id
        task_youtube_video_link =task.youtube_video_link
        if 'shorts' in task_youtube_video_link:
            video_id = task_youtube_video_link.split('shorts')[1][1:]
            new_youtube_video_link = "https://www.youtube.com/watch?v="+video_id
            yield feapder.Request(url=new_youtube_video_link,task_id=task_id,task_youtube_video_link=task_youtube_video_link)
        else:
            yield feapder.Request(url=task_youtube_video_link,task_id=task_id,task_youtube_video_link=task_youtube_video_link)

    def parse(self, request, response):
        youtube_video_link_info_batch_item = YoutubeVideoLinkInfoBatchDataItem()

        res = response.text

        if 'likeCount' in res or 'viewCount' in res:
            view_count = re.findall(r'\"viewCount\":\"(.*?)\"', res)[0]
            title = re.findall(r'\"title\":\"(.*?)\"', res)[0]
            json_str = re.findall(r'\"videoOwnerRenderer\":(.*?)\]\},\"subscriptionButton\"', res)[0].split('"runs":')[
                           1][1:]

            json_data = json.loads(json_str)
            channel_name = json_data["text"]
            channel_id = json_data["navigationEndpoint"]["browseEndpoint"]["browseId"]
            youtube_video_link_info_batch_item['youtube_link'] = request.task_youtube_video_link
            youtube_video_link_info_batch_item['youtube_title'] = title
            youtube_video_link_info_batch_item['youtube_channel_id'] = channel_id
            youtube_video_link_info_batch_item['youtube_channel_name'] = channel_name
            youtube_video_link_info_batch_item['youtube_views'] = view_count
            youtube_video_link_info_batch_item['batch'] = self.batch_date
            yield youtube_video_link_info_batch_item
            yield self.update_task_state(request.task_id, 1)
        else:
            yield self.update_task_state(request.task_id, -1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlYoutubeLinkInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeLinkInfoSpider爬虫")

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
    # python crawl_youtube_link_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_link_info_spider.py --start_worker  # 启动爬虫
