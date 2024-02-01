# -*- coding: utf-8 -*-
"""
Created on 2023-11-30 11:09:31
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用于通过YouTube Music Channel Id获取该页面下全部歌曲、专辑及单曲、视频的playlist的链接URL
    即页面歌曲栏下的所有歌曲的列表链接
    例如：
        YouTube Music页面：https://music.youtube.com/channel/UCPC0L1d253x-KuMNwa05TpA
        艺人：Taylor Swift
        全部显示歌曲的playlist列表链接【即获取结果】：
            https://music.youtube.com/playlist?list=OLAK5uy_kRl6HdICkQpZF7zuHu_Yx-RDVHw-hboxo
        全部显示专辑及单曲的playlist列表链接【即获取结果】：
            https://music.youtube.com/channel/UCPC0L1d253x-KuMNwa05TpA
        全部显示视频的playlist列表链接【即获取结果】
            https://music.youtube.com/playlist?list=OLAK5uy_loEjsMw6hRHXqBnM7tPvxZodwPc4BN3RY
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
from feapder.utils.webdriver import WebDriver
import time
from pprint import pprint


class CrawlYoutubeMusicArtistPageInfoSpider(feapder.BatchSpider):
    def start_requests(self, task):
        task_id = task.id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_channel_name = task.youtube_music_channel_name
        task_youtube_music_artist_name = task.youtube_music_artist_name
        yield feapder.Request("https://music.youtube.com/channel/" + task_youtube_music_channel_id,
                              render=True,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_channel_name=task_youtube_music_channel_name,
                              task_youtube_music_artist_name=task_youtube_music_artist_name,
                              task_id=task_id
                              )

    def parse(self, request, response):
        browser: WebDriver = response.browser
        js = "window.scrollTo(0, document.body.scrollHeight)"
        browser.execute_script(js)

        youtube_music_channel_id_batch_data_item = YoutubeMusicChannelIdBatchDataItem()

        # 1.歌手频道id
        youtube_music_channel_id_batch_data_item['youtube_music_channel_id'] = request.task_youtube_music_channel_id
        # 2.歌手名
        youtube_music_channel_id_batch_data_item['youtube_music_artist_name'] = request.task_youtube_music_artist_name
        # 3.歌手频道名
        youtube_music_channel_id_batch_data_item['youtube_music_channel_name'] = request.task_youtube_music_channel_name
        # 4.歌手【歌曲-全部显示】URL
        track_list_info = browser.find_element_by_xpath(
            '//a[@class="yt-simple-endpoint style-scope ytmusic-shelf-renderer"]')
        youtube_music_channel_id_batch_data_item['youtube_music_track_playlist_url'] = track_list_info.get_attribute(
            'href')

        list_info = browser.find_elements_by_xpath(
            '//yt-formatted-string[@class="title text style-scope ytmusic-carousel-shelf-basic-header-renderer"]/a')

        if len(list_info):
            d = dict()
            for i in range(len(list_info)):
                banner_info = list_info[i].text
                d[banner_info] = list_info[i].get_attribute('href')

        youtube_music_channel_id_batch_data_item[
            'youtube_music_album_single_playlist_url'] = d["专辑"]
        youtube_music_channel_id_batch_data_item["youtube_music_video_playlist_url"] = d["视频"]
        

        # youtube_music_channel_id_playlist_batch_task_item[
        #     'youtube_music_channel_id'] = request.task_youtube_music_channel_id
        # youtube_music_channel_id_playlist_batch_task_item[
        #     'youtube_music_track_playlist_url'] = track_list_info.get_attribute('href')
        # youtube_music_channel_id_playlist_batch_task_item[
        #     'youtube_music_album_single_playlist_url'] = 'https://music.youtube.com/channel/MPAD' + request.task_youtube_music_channel_id
        # if len(list_info) == 2:
        #     youtube_music_channel_id_playlist_batch_task_item['youtube_music_video_playlist_url'] = list_info[
        #         1].get_attribute('href')
        # else:
        #     youtube_music_channel_id_playlist_batch_task_item['youtube_music_video_playlist_url'] = list_info[
        #         2].get_attribute('href')

        # for u in l:
        #     youtube_artist_playlist_batch_task_item = YoutubeArtistPlaylistBatchTaskItem()
        #     youtube_artist_playlist_batch_task_item[
        #         'crawl_condition_youtube_artist_channel_id'] = request.task_youtube_music_channel_id
        #     youtube_artist_playlist_batch_task_item['youtube_playlist_id'] = u
        #     yield youtube_artist_playlist_batch_task_item
        # yield youtube_music_channel_id_playlist_batch_task_item
        yield youtube_music_channel_id_batch_data_item
        yield self.update_task_state(request.task_id, 1)


if __name__ == "__main__":
    spider = CrawlYoutubeMusicArtistPageInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeMusicArtistPageInfoSpider爬虫")

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
    # python crawl_youtube_music_artist_page_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_music_artist_page_info_spider.py --start_worker  # 启动爬虫
