# -*- coding: utf-8 -*-
"""
Created on 2023-01-19 14:10:01
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
import re
import time
from items.my_batch_spider_integrated_wangyi_news_test_item import MyBatchSpiderIntegratedWangyiNewsTestItem
import datetime
from feapder.dedup import Dedup



class MyBatchSpiderWangyiNewsParserTest(feapder.BatchParser):
    """
    注意 这里继承的是BatchParser，而不是BatchSpider
    """
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
    # def __init__(self, *args,**kwargs):
    dedup = Dedup()

    def download_midware(self, request):
        request.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self,task):
        task_id = task.id
        task_url = task.url
        yield feapder.Request(url=task_url,task_id=task_id)

    def parse(self, request, response):
        pattern = re.compile(r'data_callback\((.*?)\)',re.S)
        result = re.findall(pattern=pattern, string=response.text)[0]
        for per_dict in eval(result):
            # keywords处理
            if len(per_dict["keywords"]) == 0:
                item = MyBatchSpiderIntegratedWangyiNewsTestItem()
                item["title"] = per_dict["title"]
                item["channel_name"] = per_dict["channelname"]
                item["comment_url"] = per_dict["commenturl"]
                item["doc_url"] = per_dict["docurl"]
                item["img_url"] = per_dict["imgurl"]
                item["label"] = per_dict["label"]
                item["news_type"] = per_dict["newstype"]
                item["source"] = per_dict["source"]
                item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(per_dict["time"], "%m/%d/%Y %H:%M:%S"))
                item["tienum"] = per_dict["tienum"]
                item["keywords_akey_link"] = ""
                item["keywords_keyname"] = ""
                if self.dedup.add(item):
                    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    yield item
            else:
                for per_keywords_dict in per_dict["keywords"]:
                    item = MyBatchSpiderIntegratedWangyiNewsTestItem()
                    item["title"] = per_dict["title"]
                    item["channel_name"] = per_dict["channelname"]
                    item["comment_url"] = per_dict["commenturl"]
                    item["doc_url"] = per_dict["docurl"]
                    item["img_url"] = per_dict["imgurl"]
                    item["label"] = per_dict["label"]
                    item["news_type"] = per_dict["newstype"]
                    item["source"] = per_dict["source"]
                    item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(per_dict["time"], "%m/%d/%Y %H:%M:%S"))
                    item["tienum"] = per_dict["tienum"]
                    item["keywords_akey_link"] = per_keywords_dict["akey_link"]
                    item["keywords_keyname"] = per_keywords_dict["keyname"]
                    if self.dedup.add(item):
                        item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        yield item
        yield self.update_task_batch(request.task_id,1)



if __name__ == "__main__":
    spider = MyBatchSpiderWangyiNewsTest(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="MyBatchSpiderWangyiNewsTest爬虫")

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
    # python my_batch_spider_wangyi_news_test.py --start_master  # 添加任务
    # python my_batch_spider_wangyi_news_test.py --start_worker  # 启动爬虫
