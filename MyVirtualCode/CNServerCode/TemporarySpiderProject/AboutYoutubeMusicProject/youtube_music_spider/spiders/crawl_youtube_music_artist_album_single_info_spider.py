# -*- coding: utf-8 -*-
"""
Created on 2023-11-30 11:07:04
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用于通过获取YouTube Music下专辑及单曲的页面，获取其全部的专辑及单曲信息，主要是其专辑及单曲对应的playlistid
    例如：
        https://music.youtube.com/channel/MPADUCPC0L1d253x-KuMNwa05TpA
        获取到的专辑及单曲的URL，均为重定向前的URL，无法使用API接口进行数据获取，需要额外多一步处理
        def parse_redirect(self,request,response)即为获取重定向后的URL
"""

import feapder
from feapder import ArgumentParser
from items.youtube_info_item import *
import time


class CrawlYoutubeMusicArtistAlbumSingleInfoSpider(feapder.BatchSpider):
    def start_requests(self, task):
        # 'youtube_music_channel_id','youtube_music_album_single_playlist_url'
        task_id = task.id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_album_single_playlist_url = task.youtube_music_album_single_playlist_url
        yield feapder.Request(url=task_youtube_music_album_single_playlist_url,
                              render=True,
                              task_id=task_id,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_album_single_playlist_url=task_youtube_music_album_single_playlist_url
                              )

    def parse(self, request, response):
        browser: WebDriver = response.browser
        js = "window.scrollTo(0, document.body.scrollHeight)"
        browser.execute_script(js)
        time.sleep(4)

        playlist_list = browser.find_elements_by_xpath(
            '//ytmusic-two-row-item-renderer[@aspect-ratio="MUSIC_TWO_ROW_ITEM_THUMBNAIL_ASPECT_RATIO_SQUARE"]/a')
        for i in playlist_list:
            # 获取的值为重定向前的URL
            pre_redirect_url = i.get_attribute('href')
            title = i.get_attribute('title')
            yield feapder.Request(
                url=pre_redirect_url,
                render=True,
                title=title,
                pre_redirect_url=pre_redirect_url,
                callback=self.parse_redirect,
                task_youtube_music_channel_id=request.task_youtube_music_channel_id,
                task_youtube_music_album_single_playlist_url=request.task_youtube_music_album_single_playlist_url
            )

        yield self.update_task_batch(request.task_id, 1)

    def parse_redirect(self, request, response):
        browser1: WebDriver = response.browser
        current_url = browser1.current_url

        youtube_music_channel_id_playlist_batch_data_item = YoutubeMusicChannelIdPlaylistBatchDataItem()
        youtube_music_channel_id_playlist_batch_data_item[
            'youtube_music_channel_id'] = request.task_youtube_music_channel_id
        youtube_music_channel_id_playlist_batch_data_item[
            'youtube_music_album_single_playlist_url'] = request.task_youtube_music_album_single_playlist_url
        youtube_music_channel_id_playlist_batch_data_item[
            'youtube_music_album_single_url_pre_redirect'] = request.pre_redirect_url
        youtube_music_channel_id_playlist_batch_data_item['youtube_music_album_single_url'] = current_url
        youtube_music_channel_id_playlist_batch_data_item['batch'] = self.batch_date

        youtube_artist_playlist_batch_task_item = YoutubeArtistPlaylistBatchTaskItem()
        youtube_artist_playlist_batch_task_item[
            'crawl_condition_youtube_artist_channel_id'] = request.task_youtube_music_channel_id
        youtube_artist_playlist_batch_task_item['youtube_playlist_id'] = current_url.split('=')[1]
        yield youtube_music_channel_id_playlist_batch_data_item
        yield youtube_artist_playlist_batch_task_item


if __name__ == "__main__":
    spider = CrawlYoutubeMusicArtistAlbumSingleInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeMusicArtistAlbumSingleInfoSpider爬虫")

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
    # python crawl_youtube_music_artist_album_single_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_music_artist_album_single_info_spider.py --start_worker  # 启动爬虫
