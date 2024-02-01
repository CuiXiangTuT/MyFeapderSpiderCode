# -*- coding: utf-8 -*-
"""
Created on 2023-10-09 10:56:40
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.boomplay_info_item import *


class CrawlBoomplayTrackViewsSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_track_id = task.track_id
        url = "https://www.boomplay.com/embed/{}/MUSIC?colType=5&colID=".format(
            task_track_id)
        yield feapder.Request(url=url,
                              task_id=task_id,
                              task_track_id=task_track_id)

    def parse(self, request, response):
        # 判断页面是否正常打开
        is_exists_banner = response.xpath('//header[contains(@class,"header") and contains(@class,"clearfix")]')
        if is_exists_banner:
            # 歌曲播放量相关
            boomplay_track_views_batch_data_item = BoomplayTrackViewsBatchDataItem()
            view = response.xpath(
                '//span[@class="listen"]/text()').extract_first().replace(
                ",", "")
            # 22-播放量
            if 'k' in view:
                boomplay_track_views_batch_data_item["views"] = int(
                    float(view[:-1]) * 1000)
            elif 'm' in view:
                boomplay_track_views_batch_data_item["views"] = int(
                    float(view[:-1]) * 1000000)
            else:
                boomplay_track_views_batch_data_item["views"] = view
            boomplay_track_views_batch_data_item['track_id'] = request.task_track_id
            boomplay_track_views_batch_data_item['batch'] = self.batch_date
            boomplay_track_views_batch_data_item[
                'crawl_frequency'] = "crawl_frequency"

            # 歌曲播放量采集情况表相关字段
            boomplay_track_views_crawl_situation_record_batch_data_item = BoomplayTrackViewsCrawlSituationRecordBatchDataItem()
            boomplay_track_views_crawl_situation_record_batch_data_item['track_id'] = request.task_track_id
            boomplay_track_views_crawl_situation_record_batch_data_item['track_views_remarks'] = "EV"
            boomplay_track_views_crawl_situation_record_batch_data_item['track_exception_info'] = ""
            boomplay_track_views_crawl_situation_record_batch_data_item['batch'] = self.batch_date

            yield boomplay_track_views_batch_data_item
            yield boomplay_track_views_crawl_situation_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)

        else:
            exception_info = response.xpath('//div[@class="noData"]/div[@class="text"]/text()').extract_first()
            boomplay_track_views_crawl_situation_record_batch_data_item = BoomplayTrackViewsCrawlSituationRecordBatchDataItem()
            boomplay_track_views_crawl_situation_record_batch_data_item['track_id'] = request.task_track_id
            boomplay_track_views_crawl_situation_record_batch_data_item['track_views_remarks'] = "NV"
            boomplay_track_views_crawl_situation_record_batch_data_item['track_exception_info'] = exception_info
            boomplay_track_views_crawl_situation_record_batch_data_item['batch'] = self.batch_date
            yield boomplay_track_views_crawl_situation_record_batch_data_item
            yield self.update_task_batch(request.task_id, 1)

    # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlBoomplayTrackViewsSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlBoomplayTrackViewsSpider爬虫")

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
    # python crawl_boomplay_track_views_spider.py --start_master  # 添加任务
    # python crawl_boomplay_track_views_spider.py --start_worker  # 启动爬虫
