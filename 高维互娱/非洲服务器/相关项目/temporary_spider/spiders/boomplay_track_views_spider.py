# -*- coding: utf-8 -*-
"""
Created on 2023-04-14 17:53:33
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *
import re
import json
import copy

class BoomplayTrackViewsSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def add_task(self):
        update_state_sql = """
        UPDATE boomplay_track_info_batch_task
        SET views_state = 0
        WHERE views_state = -1
        """
        self._mysqldb.update(update_state_sql)

    def my_init_task(self):
        sql = "update {task_table} set {state} = 0 where {state} != -1".format(
            task_table=self._task_table,
            state=self._task_state,
        )
        return self._mysqldb.update(sql)
    
    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_track_id = task.track_id
        if self._task_state=='views_state':
            task_crawl_frequency = 'crawl_weekly'
        url = "https://www.boomplay.com/embed/{}/MUSIC?colType=5&colID=".format(task_track_id)
        yield feapder.Request(url=url,task_id=task_id,task_crawl_frequency=task_crawl_frequency,task_track_id=task_track_id)

    def parse(self, request, response):
        track_views_batch_data_item = BoomplayTrackViewsBatchDataItem()
        try:
            view = response.xpath('.//span[@class="listen"]/text()').extract_first().replace(",","")
            # 22-播放量
            if 'k' in view:
                track_views_batch_data_item["views"] = int(float(view[:-1]) * 1000)
            elif 'm' in view:
                track_views_batch_data_item["views"] = int(float(view[:-1]) * 1000000)
            else:
                track_views_batch_data_item["views"] = view
            track_views_batch_data_item['track_id'] = request.task_track_id
            track_views_batch_data_item['batch'] = self.batch_date
            track_views_batch_data_item['crawl_frequency'] = request.task_crawl_frequency
            yield track_views_batch_data_item
            yield self.update_task_batch(request.task_id,1)
        except:
            yield self.update_task_batch(request.task_id,-1)
    
    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response,e):
        yield request
        yield self.update_task_state(request.task_id, -1)



if __name__ == "__main__":
    spider = BoomplayTrackViewsSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BoomplayTrackViewsSpider爬虫")

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
    # python boomplay_track_views_spider.py --start_master  # 添加任务
    # python boomplay_track_views_spider.py --start_worker  # 启动爬虫
