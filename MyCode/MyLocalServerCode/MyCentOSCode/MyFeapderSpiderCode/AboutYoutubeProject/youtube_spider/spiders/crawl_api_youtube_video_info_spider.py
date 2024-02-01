# -*- coding: utf-8 -*-
"""
Created on 2023-10-17 19:19:58
---------
@summary:
---------
@author: QiuQiuRen
@description:
    根据提供的YouTube video link，获取其相关信息
"""

import feapder
from feapder import ArgumentParser


class CrawlApiYoutubeVideoInfoSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        return request

    def start_requests(self, task):
        # youtube_key = 'AIzaSyAyLDhd-d7vsvmlXQIPOy7bWoGQk-T4H9g'
        youtube_key = "AIzaSyDrSZ7-1VsFbA35MnKeEQ3_B3kkVEx18Ng"
        task_id = task.id
        task_youtube_video_link = task.youtube_video_link
        task_youtube_video_id = task.youtube_video_link.split('=')[-1]
        url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}".format(task_youtube_video_id,youtube_key)
        yield feapder.Request(url,task_id=task_id,task_youtube_video_link=task_youtube_video_link,task_youtube_video_id=task_youtube_video_id)

    def parse(self, request, response):
        item = dict()
        data = response.json['items'][0]
        item['youtube_id'] = data['id']
        item['youtube_title'] = data['snippet']['title']
        item['publish_date'] = data['snippet']['publishedAt'].replace('T', '').replace('Z', '')
        item['description'] = data['snippet']['description']
        item['youtube_channel'] = data['snippet']['channelTitle']
        print(item)


if __name__ == "__main__":
    spider = CrawlApiYoutubeVideoInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlApiYoutubeVideoInfoSpider爬虫")

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
    # python crawl_api_youtube_video_info_spider.py --start_master  # 添加任务
    # python crawl_api_youtube_video_info_spider.py --start_worker  # 启动爬虫
