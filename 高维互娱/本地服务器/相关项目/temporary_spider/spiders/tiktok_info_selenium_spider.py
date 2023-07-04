# -*- coding: utf-8 -*-
"""
Created on 2023-06-28 10:10:48
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from feapder.utils.webdriver import WebDriver
from items.tiktok_user_name_batch_data_item import TiktokUserNameBatchDataItem
import time

class TiktokInfoSeleniumSpider(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="127.0.0.1:6379",
    #     REDISDB_USER_PASS="",
    #     REDISDB_DB=0,
    #     MYSQL_IP="192.168.10.133",
    #     MYSQL_PORT=3306,
    #     MYSQL_DB="gmg_data_assets",
    #     MYSQL_USER_NAME="root",
    #     MYSQL_USER_PASS="123456",
    # )
    def download_midware(self,request):
        request.headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_gmg_artist_name = task.gmg_artist_name
        task_user_id = task.user_id
        task_sec_uid = task.sec_uid
        task_tiktok_url = task.tiktok_url
        yield feapder.Request(
            url=task_tiktok_url,
            task_gmg_artist_id = task_gmg_artist_id,
            task_gmg_artist_name = task_gmg_artist_name,
            task_user_id = task_user_id,
            task_sec_uid = task_sec_uid,
            task_tiktok_url = task_tiktok_url,
            task_id=task_id,
            render=True
        )

    def parse(self, request, response):
        item = TiktokUserNameBatchDataItem()
        browser: WebDriver = response.browser
        browser.set_page_load_timeout(3)
        browser.set_script_timeout(3)
        time.sleep(1)
        user_name = browser.find_element_by_xpath('//h2[@data-e2e="user-title"]').text
        item['gmg_artist_id'] = request.task_gmg_artist_id
        item['gmg_artist_name'] = request.task_gmg_artist_name
        item['user_id'] = request.task_user_id
        item['sec_uid'] = request.task_sec_uid
        item['tiktok_url'] = request.task_tiktok_url
        item['user_name'] = user_name
        response.close_browser(request)
        yield item
        yield self.update_task_state(request.task_id, 1)
    
        # 超过最大重试次数的请求, 在任务表中标记失败
    def failed_request(self, request, response,e):
        yield request
        yield self.update_task_state(request.task_id, -1)



if __name__ == "__main__":
    spider = TiktokInfoSeleniumSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="TiktokInfoSeleniumSpider爬虫")

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
    # python tiktok_info_selenium_spider.py --start_master  # 添加任务
    # python tiktok_info_selenium_spider.py --start_worker  # 启动爬虫
