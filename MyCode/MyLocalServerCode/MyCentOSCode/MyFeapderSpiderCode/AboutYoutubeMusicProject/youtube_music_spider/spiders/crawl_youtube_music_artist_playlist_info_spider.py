# -*- coding: utf-8 -*-
"""
Created on 2023-10-08 14:43:18
---------
@summary:
---------
@author: QiuQiuRen
"""
import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *
from feapder.utils.webdriver import WebDriver
import time

class CrawlYoutubeMusicArtistPlaylistInfoSpider(feapder.BatchSpider):
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
        youtube_music_channel_id_playlist_batch_task_item = YoutubeMusicChannelIdPlaylistBatchTaskItem()
        l = list()
        l.clear()

        youtube_music_channel_id_batch_data_item['youtube_music_channel_id'] = request.task_youtube_music_channel_id

        youtube_music_channel_id_batch_data_item['youtube_music_artist_name'] = request.task_youtube_music_artist_name
        youtube_music_channel_id_batch_data_item['youtube_music_channel_name'] = request.task_youtube_music_channel_name
        track_list_info = browser.find_element_by_xpath(
            '//a[@class="yt-simple-endpoint style-scope ytmusic-shelf-renderer"]')
        youtube_music_channel_id_batch_data_item['youtube_music_track_playlist_url'] = track_list_info.get_attribute(
            'href')

        l.append(track_list_info.get_attribute('href').split('=')[1])

        list_info = browser.find_elements_by_xpath(
            '//yt-formatted-string[@class="title text style-scope ytmusic-carousel-shelf-basic-header-renderer"]/a')

        youtube_music_channel_id_batch_data_item[
            'youtube_music_album_single_playlist_url'] = 'https://music.youtube.com/channel/MPAD' + request.task_youtube_music_channel_id
        if len(list_info) == 2:
            youtube_music_channel_id_batch_data_item['youtube_music_video_playlist_url'] = list_info[1].get_attribute(
                'href')
            l.append(list_info[1].get_attribute('href').split('=')[1])
        else:
            youtube_music_channel_id_batch_data_item['youtube_music_video_playlist_url'] = list_info[2].get_attribute(
                'href')
            l.append(list_info[2].get_attribute('href').split('=')[1])
        youtube_music_channel_id_batch_data_item['batch'] = self.batch_date

        youtube_music_channel_id_playlist_batch_task_item[
            'youtube_music_channel_id'] = request.task_youtube_music_channel_id
        youtube_music_channel_id_playlist_batch_task_item[
            'youtube_music_track_playlist_url'] = track_list_info.get_attribute('href')
        youtube_music_channel_id_playlist_batch_task_item[
            'youtube_music_album_single_playlist_url'] = 'https://music.youtube.com/channel/MPAD' + request.task_youtube_music_channel_id
        if len(list_info) == 2:
            youtube_music_channel_id_playlist_batch_task_item['youtube_music_video_playlist_url'] = list_info[
                1].get_attribute('href')
        else:
            youtube_music_channel_id_playlist_batch_task_item['youtube_music_video_playlist_url'] = list_info[
                2].get_attribute('href')

        for u in l:
            youtube_artist_playlist_batch_task_item = YoutubeArtistPlaylistBatchTaskItem()
            youtube_artist_playlist_batch_task_item[
                'crawl_condition_youtube_artist_channel_id'] = request.task_youtube_music_channel_id
            youtube_artist_playlist_batch_task_item['youtube_playlist_id'] = u
            yield youtube_artist_playlist_batch_task_item
        yield youtube_music_channel_id_playlist_batch_task_item
        yield youtube_music_channel_id_batch_data_item
        yield self.update_task_state(request.task_id, 1)


if __name__ == "__main__":
    spider = CrawlYoutubeMusicArtistPlaylistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeMusicArtistPlaylistInfoSpider爬虫")

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
    # python crawl_youtube_music_artist_playlist_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_music_artist_playlist_info_spider.py --start_worker  # 启动爬虫
