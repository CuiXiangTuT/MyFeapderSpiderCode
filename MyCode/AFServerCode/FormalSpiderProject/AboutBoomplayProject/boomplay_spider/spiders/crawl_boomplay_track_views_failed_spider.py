# -*- coding: utf-8 -*-
"""
Created on 2023-10-24 11:02:46
---------
@summary:
---------
@author: QiuQiuRen
@description：
    采集Boomplay批次播放量失败的歌曲
    1.若采集成功：
        1.1-将歌曲播放量入库至boomplay_track_views_batch_data
        1.2-将boomplay_track_info_batch_task的views_state更新设置为1
    2.若采集失败：
        2.1-将失败信息及原因录入至库表boomplay_track_views_failed_batch_data
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *


class CrawlBoomplayTrackViewsFailedSpider(feapder.BatchSpider):
    def download_midware(self, request):
        request.headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_track_id = task.track_id
        task_batch = task.batch
        url = "https://www.boomplay.com/embed/{}/MUSIC?colType=5&colID=".format(
            task_track_id)
        yield feapder.Request(url=url,
                              task_id=task_id,
                              task_batch=task_batch,
                              task_track_id=task_track_id)

    def parse(self, request, response):
        try:
            track_views_batch_data_item = BoomplayTrackViewsBatchDataItem()
            view = response.xpath(
                '//span[@class="listen"]/text()').extract_first().replace(
                ",", "")
            # 22-播放量
            if 'k' in view:
                track_views_batch_data_item["views"] = int(
                    float(view[:-1]) * 1000)
            elif 'm' in view:
                track_views_batch_data_item["views"] = int(
                    float(view[:-1]) * 1000000)
            else:
                track_views_batch_data_item["views"] = view
            track_views_batch_data_item['track_id'] = request.task_track_id
            track_views_batch_data_item['batch'] = request.task_batch
            track_views_batch_data_item[
                'crawl_frequency'] = "crawl_frequency"
            update_sql = "UPDATE boomplay_track_info_batch_task SET views_state = 1 WHERE track_id = {}".format(
                request.task_track_id)
            yield track_views_batch_data_item
            yield self.update_task_batch(request.task_id, 1)
            return self._mysqldb.update(update_sql)
        except:
            failed_info = response.xpath('//div[@class="noData"]/div[@class="text"]/text()').extract_first()
            boomplay_track_views_failed_batch_data_item = BoomplayTrackViewsFailedBatchDataItem()
            boomplay_track_views_failed_batch_data_item['track_id'] = request.task_track_id
            boomplay_track_views_failed_batch_data_item['failed_info'] = failed_info
            boomplay_track_views_failed_batch_data_item['batch'] = request.task_batch
            yield boomplay_track_views_failed_batch_data_item
            yield self.update_task_batch(request.task_id, -1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        failed_info = response.xpath('//div[@class="noData"]/div[@class="text"]/text()').extract_first()
        boomplay_track_views_failed_batch_data_item = BoomplayTrackViewsFailedBatchDataItem()
        boomplay_track_views_failed_batch_data_item['track_id'] = request.task_track_id
        boomplay_track_views_failed_batch_data_item['failed_info'] = failed_info
        boomplay_track_views_failed_batch_data_item['batch'] = request.task_batch
        yield boomplay_track_views_failed_batch_data_item
        yield request
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlBoomplayTrackViewsFailedSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayTrackViewsFailedSpider爬虫")

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
    # python crawl_boomplay_track_views_failed_spider.py --start_master  # 添加任务
    # python crawl_boomplay_track_views_failed_spider.py --start_worker  # 启动爬虫
