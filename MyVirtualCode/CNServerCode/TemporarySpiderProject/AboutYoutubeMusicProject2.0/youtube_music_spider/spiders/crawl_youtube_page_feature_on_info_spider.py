# -*- coding: utf-8 -*-
"""
Created on 2024-01-06 17:49:58
---------
@summary:
---------
@author: AirWolf
@description：
    获取feature on页面下的信息
"""

import feapder
from feapder import ArgumentParser


class CrawlYoutubeFeatureOnInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {

        }
        return request

    def start_requests(self, task):
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        data = {
            "context": {
                "client": {
                    "hl": "en",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0,gzip(gfe)",
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20231214.00.00",
                }

            },
            "browseId": "VLRDCLAK5uy_mijutvVbzp7bbNlWt-B5U90qb5KplCkSQ"
        }
        yield feapder.Request(url=url,json=data)

    def parse(self, request, response):
        # 提取网站title
        print(response.xpath("//title/text()").extract_first())
        # 提取网站描述
        print(response.xpath("//meta[@name='description']/@content").extract_first())
        print("网站地址: ", response.url)


if __name__ == "__main__":
    spider = CrawlYoutubeFeatureOnInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeFeatureOnInfoSpider爬虫")

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
    # python crawl_youtube_page_feature_on_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_page_feature_on_info_spider.py --start_worker  # 启动爬虫
