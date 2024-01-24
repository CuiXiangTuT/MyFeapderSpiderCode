# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 18:16:43
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.temp_bajao_artist_data_001_item import  *


class CrawlBajaoArtistInfoSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self,task):
        url = "https://bajao.pk/api/artist/details?siteid="
        task_id = task.id
        task_aid = task.bajao_artist_id
        data = {
            'aId': task_aid,
            'sIndex': 0,
            'fIndex': 7
        }
        yield feapder.Request(url=url, data=data,task_id=task_id,task_aid=task_aid)

    def parse(self, request, response):
        item = TempBajaoArtistData001Item()
        data = response.json
        if data['msg']=='SUCCESS':
            title = data['respData']['title']
            item['bajao_artist_id'] = request.task_aid
            item['bajao_artist_name'] = title
            yield item
            yield self.update_task_state(request.task_id, 1)
        else:
            yield self.update_task_batch(request.task_id, -1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlBajaoArtistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBajaoArtistInfoSpider爬虫")

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
    # python crawl_bajao_artist_info_spider.py --start_master  # 添加任务
    # python crawl_bajao_artist_info_spider.py --start_worker  # 启动爬虫
