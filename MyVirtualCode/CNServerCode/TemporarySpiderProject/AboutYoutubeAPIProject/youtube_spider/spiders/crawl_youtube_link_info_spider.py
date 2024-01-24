# -*- coding: utf-8 -*-
"""
Created on 2023-09-27 14:35:23
---------
@summary:
---------
@author: QiuQiuRen
@description：
    采集任务表：
    入库数据表：
    采集说明：
        根据提供的YouTubeLink，采集YouTubeLink下的页面信息，
        主要涉及YouTubeTitle、YouTubeChannel、YouTubeChannelId、Views、Likes
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
import re
import json


class CrawlYoutubeLinkInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def my_init_task(self):
        sql = "update {task_table} set {state} = 0 where {state} != -1".format(
            task_table=self._task_table,
            state=self._task_state,
        )
        return self._mysqldb.update(sql)

    def download_midware(self, request):
        request.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_youtube_video_link = task.youtube_video_link
        task_id = task.id
        yield feapder.Request(task_youtube_video_link,
                              task_youtube_video_link=task_youtube_video_link,
                              task_id=task_id,
                              )

    def parse(self, request, response):
        youtube_video_batch_data_item = YoutubeVideoLinkInfoBatchDataItem()
        if response.status_code == 200:
            data = \
            re.findall(r'var ytInitialPlayerResponse = (.*?)var meta = document\.createElement', response.extract(),
                       re.S)[0][:-1]
            video_status =  json.loads(data)['playabilityStatus']['status']
            if video_status=="OK":
                json_data = json.loads(data)['videoDetails']
                # link
                youtube_video_batch_data_item['youtube_video_link'] = request.task_youtube_video_link
                #  标题
                youtube_video_batch_data_item["youtube_title"] = json_data["title"].strip().lower()
                # video_id
                youtube_video_batch_data_item["youtube_video_id"] = json_data["videoId"]
                # 时长？
                youtube_video_batch_data_item["duration"] = json_data["lengthSeconds"]
                # channelId
                youtube_video_batch_data_item["youtube_channel_id"] = json_data["channelId"]
                # 播放量
                youtube_video_batch_data_item["youtube_views"] = json_data['viewCount']
                # 作者
                youtube_video_batch_data_item['youtube_channel_name'] = json_data['author'].strip().lower()
                # 简述
                youtube_video_batch_data_item["description"] = json_data['shortDescription'].replace("\n", " ")
                youtube_video_batch_data_item['batch'] = self.batch_date
                print(youtube_video_batch_data_item)
                yield youtube_video_batch_data_item

                youtube_video_link_info_crawl_situation_record_batch_data = YoutubeVideoLinkInfoCrawlSituationRecordBatchDataItem()
                youtube_video_link_info_crawl_situation_record_batch_data[
                    'youtube_video_link'] = request.task_youtube_video_link
                youtube_video_link_info_crawl_situation_record_batch_data[
                    "youtube_video_link_infomation_remarks"] = "EI"
                youtube_video_link_info_crawl_situation_record_batch_data[
                    'youtube_video_link_infomation_status'] = video_status
                youtube_video_link_info_crawl_situation_record_batch_data['youtube_video_link_infomation_reasons'] = ""
                youtube_video_link_info_crawl_situation_record_batch_data['batch'] = self.batch_date
                print(youtube_video_link_info_crawl_situation_record_batch_data)
                yield youtube_video_link_info_crawl_situation_record_batch_data
                yield self.update_task_batch(request.task_id, 1)
            else:
                youtube_video_link_info_crawl_situation_record_batch_data = YoutubeVideoLinkInfoCrawlSituationRecordBatchDataItem()
                youtube_video_link_info_crawl_situation_record_batch_data['youtube_video_link'] = request.task_youtube_video_link
                youtube_video_link_info_crawl_situation_record_batch_data["youtube_video_link_infomation_remarks"] = "NI"
                youtube_video_link_info_crawl_situation_record_batch_data['youtube_video_link_infomation_status'] = video_status
                youtube_video_link_info_crawl_situation_record_batch_data['youtube_video_link_infomation_reasons'] = json.loads(data)['playabilityStatus']['messages']
                youtube_video_link_info_crawl_situation_record_batch_data['batch'] = self.batch_date
                yield youtube_video_link_info_crawl_situation_record_batch_data
                print(youtube_video_link_info_crawl_situation_record_batch_data)
                yield self.update_task_batch(request.task_id, 1)

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


