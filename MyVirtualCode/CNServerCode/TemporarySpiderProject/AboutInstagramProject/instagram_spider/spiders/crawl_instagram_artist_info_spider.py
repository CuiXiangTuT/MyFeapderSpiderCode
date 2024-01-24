# -*- coding: utf-8 -*-
"""
Created on 2023-10-07 10:41:19
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.instagram_info_item import InstagramArtistInfoBatchDataItem


class CrawInstagramArtistInfoSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_instagram_artist_url = task.instagram_artist_url
        task_instagram_artist_name = task.instagram_artist_name
        task_url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=' + \
                   task.instagram_artist_url.split('/')[-1]
        yield feapder.Request(url=task_url, task_id=task_id, task_instagram_artist_url=task_instagram_artist_url,
                              task_instagram_artist_name=task_instagram_artist_name)

    def parse(self, request, response):
        data_json = response.json
        artist_info = data_json['data']['user']
        instagram_artist_info_batch_data_item = InstagramArtistInfoBatchDataItem()
        instagram_artist_info_batch_data_item['crawl_condition_instagram_artist_url'] = request.task_instagram_artist_url
        instagram_artist_info_batch_data_item['batch'] = self.batch_date
        instagram_artist_info_batch_data_item['crawl_condition_instagram_artist_name'] = request.task_instagram_artist_name
        instagram_artist_info_batch_data_item['crawl_result_instagram_artist_name'] = artist_info['username']
        instagram_artist_info_batch_data_item['crawl_result_instagram_artist_full_name'] = artist_info['full_name']
        instagram_artist_info_batch_data_item['instagram_artist_followers_count'] = artist_info['edge_followed_by']['count']
        instagram_artist_info_batch_data_item['instagram_artist_image'] = artist_info['external_url']
        yield instagram_artist_info_batch_data_item
        yield self.update_task_state(request.task_id, 1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_state(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawInstagramArtistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawInstagramArtistInfoSpider爬虫")

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
    # python crawl_instagram_artist_info_spider.py --start_master  # 添加任务
    # python crawl_instagram_artist_info_spider.py --start_worker  # 启动爬虫
