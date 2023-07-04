# -*- coding: utf-8 -*-
"""
Created on 2023-01-18 15:39:02
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.my_batch_spider_task_baidu_news_test_item import MyBatchSpiderTaskBaiduNewsTestItem
import datetime


class BatchSpiderTest(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    # __custom_setting__ = dict(
    #     REDISDB_IP_PORTS="localhost:6379",
    #     REDISDB_USER_PASS="",
    #     REDISDB_DB=0,
    #     MYSQL_IP="localhost",
    #     MYSQL_PORT=3306,
    #     MYSQL_DB="",
    #     MYSQL_USER_NAME="",
    #     MYSQL_USER_PASS="",
    # )
    def download_midware(self, request):
        request.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        # task为在任务表中取出的每一条任务
        id,url = task
        yield feapder.Request(url,task_id=id)

    def parse(self, request, response):
        div_list = response.xpath('..//div[contains(@class,"category-wrap_iQLoo") and contains(@class,"horizontal_1eKyQ")]')
        for per_div in div_list:
            item = MyBatchSpiderTaskBaiduNewsTestItem()
            # 标题
            item["title"] = per_div.xpath('.//div[@class="c-single-text-ellipsis"]/text()').extract_first().strip()
            # 热度值
            item["hot_search_index"] = per_div.xpath('.//div[@class="hot-index_1Bl1a"]/text()').extract_first().strip()
            # 插入时间
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield item
        yield self.update_task_batch(request.task_id,1) #  更新状态为1


if __name__ == "__main__":
    spider = BatchSpiderTest(
        redis_key="feapder:my_batch_spider_task_test",  # 分布式爬虫调度信息存储位置
        task_table="my_batch_spider_task_test",  # mysql中的任务表
        task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="my_batch_spider_task_test_batch_record",  # mysql中的批次记录表
        batch_name="百度新闻采集",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="BatchSpiderTest爬虫")

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
    # python batch_spider_test.py --start_master  # 添加任务
    # python batch_spider_test.py --start_worker  # 启动爬虫
