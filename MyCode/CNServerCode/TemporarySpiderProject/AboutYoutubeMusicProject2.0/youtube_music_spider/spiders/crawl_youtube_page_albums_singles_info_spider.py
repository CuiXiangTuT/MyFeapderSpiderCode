# -*- coding: utf-8 -*-
"""
Created on 2023-12-21 10:49:46
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用于获取歌手【专辑-单曲】下的所有信息，该页面下的【专辑、单曲】链接需要做二次处理，
    处理前类似为：https://music.youtube.com/browse/MPREb_uCGLYKfIZNj
    需要获取重定向后的URL：https://music.youtube.com/playlist?list=OLAK5uy_lXoaeeV3xX4z5honDCOF8ryRqrzbbdrP4
    且当前页面无法获取到OLAK5uy_lXoaeeV3xX4z5honDCOF8ryRqrzbbdrP4，因此必须做二次处理
"""

import feapder
from feapder import ArgumentParser
import time
from feapder.utils.webdriver import WebDriver
from selenium.webdriver.common.by import By
from items.youtube_music_info_item import *


class CrawlYoutubePageAlbumsSinglesInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_albums_singles_id = task.youtube_music_albums_singles_id
        task_youtube_music_albums_singles_url = task.youtube_music_albums_singles_url
        yield feapder.Request(url=task_youtube_music_albums_singles_url,
            render=True,
            task_id=task_id,
            task_gmg_artist_id=task_gmg_artist_id,
            task_youtube_music_channel_id=task_youtube_music_channel_id,
            task_youtube_music_albums_singles_id=task_youtube_music_albums_singles_id,
            task_youtube_music_albums_singles_url=task_youtube_music_albums_singles_url
        )

    def parse(self, request, response):
        browser: WebDriver = response.browser
        js = "window.scrollTo(0, document.body.scrollHeight)"
        browser.execute_script(js)
        time.sleep(4)

        playlist_list = browser.find_elements(By.XPATH,'//ytmusic-two-row-item-renderer[@aspect-ratio="MUSIC_TWO_ROW_ITEM_THUMBNAIL_ASPECT_RATIO_SQUARE"]/a')
        for i in playlist_list:
            # 获取的值为重定向前的URL
            pre_redirect_url = i.get_attribute('href')
            title = i.get_attribute('title')
            yield feapder.Request(
                url=pre_redirect_url,
                render=True,
                title=title,
                pre_redirect_url=pre_redirect_url,
                task_gmg_artist_id=request.task_gmg_artist_id,
                callback=self.parse_redirect,
                task_youtube_music_channel_id = request.task_youtube_music_channel_id,
                task_youtube_music_albums_singles_id = request.task_youtube_music_albums_singles_id,
                task_youtube_music_albums_singles_url = request.task_youtube_music_albums_singles_url
            )
            
        yield self.update_task_batch(request.task_id, 1)
    
    def parse_redirect(self,request,response):
        browser1: WebDriver = response.browser
        current_url = browser1.current_url

        youtube_music_albums_singles_data_item = YoutubeMusicAlbumsSinglesDataItem()
        youtube_music_albums_singles_data_item["gmg_artist_id"] = request.task_gmg_artist_id
        youtube_music_albums_singles_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
        youtube_music_albums_singles_data_item["youtube_music_albums_singles_id"] = request.task_youtube_music_albums_singles_id
        youtube_music_albums_singles_data_item['youtube_music_albums_singles_url'] = request.task_youtube_music_albums_singles_url
        youtube_music_albums_singles_data_item["title"] = request.title
        youtube_music_albums_singles_data_item['youtube_music_albums_singles_url_pre_redirect'] = request.pre_redirect_url
        youtube_music_albums_singles_data_item['youtube_music_albums_singles_url_after_redirect'] = current_url
        youtube_music_albums_singles_data_item["batch"] = self.batch_date

        youtube_music_artist_plate_batch_task_item = YoutubeMusicArtistPlateBatchTaskItem()
        youtube_music_artist_plate_batch_task_item['gmg_artist_id'] = request.task_gmg_artist_id
        youtube_music_artist_plate_batch_task_item['youtube_music_channel_id'] = request.task_youtube_music_channel_id
        youtube_music_artist_plate_batch_task_item["youtube_music_playlist_id"] = current_url.split("?list=")[1]
        youtube_music_artist_plate_batch_task_item["youtube_music_playlist_url"] = current_url
        youtube_music_artist_plate_batch_task_item["youtube_music_playe_remark"] = "Albums/Singles"

        yield youtube_music_albums_singles_data_item
        yield youtube_music_artist_plate_batch_task_item
        


if __name__ == "__main__":
    spider = CrawlYoutubePageAlbumsSinglesInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubePageAlbumsSinglesInfoSpider爬虫")

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
    # python crawl_youtube_page_albums_singles_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_page_albums_singles_info_spider.py --start_worker  # 启动爬虫
