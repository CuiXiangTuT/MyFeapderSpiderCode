# -*- coding: utf-8 -*-
"""
Created on 2023-12-29 15:40:50
---------
@summary:
---------
@author: QiuQiuRen
@description：
    解决关于部分Playlist URL重定向的问题
"""

import feapder
from feapder import ArgumentParser
from feapder.utils.webdriver import WebDriver
from items.youtube_music_info_item import *


class CrawlYoutubePlaylistUrlRedirectSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en-US',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_playlist_id = task.youtube_music_playlist_id
        task_youtube_music_playlist_url = task.youtube_music_playlist_url
        task_youtube_music_playlist_url_pre_redirect = task.youtube_music_playlist_url_pre_redirect
        task_title = task.title
        task_youtube_music_plate_remark = task.youtube_music_plate_remark
        yield feapder.Request(
            url=task_youtube_music_playlist_url_pre_redirect,
            task_id=task_id,
            task_gmg_artist_id=task_gmg_artist_id,
            task_youtube_music_channel_id=task_youtube_music_channel_id,
            task_youtube_music_playlist_id=task_youtube_music_playlist_id,
            task_youtube_music_playlist_url=task_youtube_music_playlist_url,
            task_youtube_music_playlist_url_pre_redirect=task_youtube_music_playlist_url_pre_redirect,
            task_title=task_title,
            task_youtube_music_plate_remark=task_youtube_music_plate_remark,
            render=True,
        )

    def parse(self, request, response):
        browser: WebDriver = response.browser
        current_url = browser.current_url

        youtube_music_plate_url_data_item = YoutubeMusicPlateUrlDataItem()
        youtube_music_plate_url_data_item['gmg_artist_id'] = request.task_gmg_artist_id
        youtube_music_plate_url_data_item['youtube_music_channel_id'] = request.task_youtube_music_channel_id
        youtube_music_plate_url_data_item['youtube_music_playlist_id'] = request.task_youtube_music_playlist_id
        youtube_music_plate_url_data_item['youtube_music_playlist_url'] = request.task_youtube_music_playlist_url
        youtube_music_plate_url_data_item['youtube_music_playlist_url_pre_redirect'] = request.task_youtube_music_playlist_url_pre_redirect
        youtube_music_plate_url_data_item['title'] = request.task_title
        youtube_music_plate_url_data_item['youtube_music_plate_remark'] = request.task_youtube_music_plate_remark
        youtube_music_plate_url_data_item['youtube_music_playlist_url_after_redirect'] = current_url
        youtube_music_plate_url_data_item['batch'] = self.batch_date
        yield youtube_music_plate_url_data_item

        youtube_music_artist_plate_task_item = YoutubeMusicArtistPlateTaskItem()
        youtube_music_artist_plate_task_item['gmg_artist_id'] = request.task_gmg_artist_id
        youtube_music_artist_plate_task_item['youtube_music_channel_id'] = request.task_youtube_music_channel_id
        youtube_music_artist_plate_task_item['youtube_music_playlist_id'] = current_url.split("list=")[1]
        youtube_music_artist_plate_task_item['youtube_music_playlist_url'] = current_url
        youtube_music_artist_plate_task_item['youtube_music_plate_remark'] = request.task_youtube_music_plate_remark
        yield youtube_music_artist_plate_task_item
        yield self.update_task_batch(request.task_id, 1)


if __name__ == "__main__":
    spider = CrawlYoutubePlaylistUrlRedirectSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubePlaylistUrlRedirectSpider爬虫")

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
    # python crawl_youtube_playlist_url_redirect_spider.py --start_master  # 添加任务
    # python crawl_youtube_playlist_url_redirect_spider.py --start_worker  # 启动爬虫
