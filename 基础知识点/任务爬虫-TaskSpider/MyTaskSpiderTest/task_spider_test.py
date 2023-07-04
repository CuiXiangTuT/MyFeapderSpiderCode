# -*- coding: utf-8 -*-
"""
Created on 2023-01-18 11:57:00
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from my_spider_task_baidu_news_test_item import MySpiderTaskBaiduNewsTestItem
import datetime


class TaskSpiderTest(feapder.TaskSpider):
    # # 自定义数据库，若项目中有setting.py文件，此自定义可删除
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

    def start_requests(self, task):
        task_id = task.id
        url = task.url
        print(task_id)
        print(url)
        yield feapder.Request(url, task_id=task_id)

    def parse(self, request, response):
        # # 提取网站title
        # print(response.xpath("//title/text()").extract_first())
        # # 提取网站描述
        # print(response.xpath("//meta[@name='description']/@content").extract_first())
        # print("网站地址: ", response.url)
        div_list = response.xpath('..//div[contains(@class,"category-wrap_iQLoo") and contains(@class,"horizontal_1eKyQ")]')
        for per_div in div_list:
            item = MySpiderTaskBaiduNewsTestItem()
            # 标题
            item["title"] = per_div.xpath('.//div[@class="c-single-text-ellipsis"]/text()').extract_first().strip()
            # 热度值
            item["hot_search_index"] = per_div.xpath('.//div[@class="hot-index_1Bl1a"]/text()').extract_first().strip()
            # 插入时间
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # yield item
            yield item

        # mysql 需要更新任务状态为做完 即 state=1
        yield self.update_task_batch(request.task_id)

def start(args):
    """
    用MySQL做种子表
    """
    spider = TaskSpiderTest(
        # redis_key="feapder:my_spider_task_test", 
        task_table="my_spider_task_test",
        task_keys=["id","url"],
        redis_key = "feapder:my_spider_task_test",
        keep_alive=True,    # 是否常驻
        delete_keys=True,   # 重启时是否删除Redis里的key，若想断点续爬，设置为False 
        )
    if args == 1:
        spider.start_monitor_task()
    else:
        spider.start()


if __name__ == "__main__":
    # 用mysql做任务表，需要先建好任务任务表
    # spider = TaskSpiderTest(
    #     redis_key="feapder:my_spider_task_test",  # 分布式爬虫调度信息存储位置
    #     task_table="my_spider_task_test",  # mysql中的任务表
    #     task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
    #     task_state="state",  # mysql中任务状态字段
    # )

    # 用redis做任务表
    # spider = TaskSpiderTest(
    #     redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
    #     task_table="", # 任务表名
    #     task_table_type="redis", # 任务表类型为redis
    # )

    parser = ArgumentParser(description="TaskSpiderTest爬虫")

    parser.add_argument(
        "--start",
        type = int,
        nargs = 1,
        help="使用MySQL当做种子表",
        function=start,
    )
    parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python task_spider_test.py --start_master  # 添加任务
    # python task_spider_test.py --start_worker  # 启动爬虫