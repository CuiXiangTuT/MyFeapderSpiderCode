# -*- coding: utf-8 -*-
"""
Created on 2023-09-06 19:30:30
---------
@summary:
---------
@author: QiuQiuRen
@description：
    通过给予的YouTube Link，获取其对应的YouTube Channel Id
"""
import feapder
from feapder import ArgumentParser
import time
from feapder.utils.webdriver import WebDriver
import re
import time
from items.youtube_info_item import *
from selenium.webdriver.common.by import By


class CrawlYoutubeLinkGetChannelIdSpider(feapder.BatchSpider):

    def start_requests(self, task):
        task_id = task.id
        task_youtube_link = task.youtube_link
        yield feapder.Request(url=task_youtube_link,render=True,task_id=task_id,task_youtube_link=task_youtube_link
        )

    def parse(self, request, response):
        browser: WebDriver = response.browser
        js = "window.scrollTo(0, document.body.scrollHeight)"
        browser.execute_script(js)
        time.sleep(4)
        youtube_link_get_channel_id_data_item = YoutubeLinkGetChannelIdDataItem()
        channel_id_m = browser.find_element(By.XPATH,'//link[@title="RSS"]')
        channel_id = channel_id_m.get_attribute("href").split('=')[1]
        youtube_link_get_channel_id_data_item['youtube_link'] = request.task_youtube_link
        youtube_link_get_channel_id_data_item['youtube_channel_link'] = "https://www.youtube.com/channel/"+channel_id
        youtube_link_get_channel_id_data_item['youtube_channel_id'] = channel_id
        yield youtube_link_get_channel_id_data_item
        yield self.update_task_state(request.task_id, 1)

    def failed_request(self, request, response, e):
        yield request
        yield self.update_task_state(request.task_id, -1)



if __name__ == "__main__":
    spider = CrawlYoutubeLinkGetChannelIdSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeLinkGetChannelIdSpider爬虫")

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
    # python crawl_youtube_link_get_channel_id_spider.py --start_master  # 添加任务
    # python crawl_youtube_link_get_channel_id_spider.py --start_worker  # 启动爬虫
