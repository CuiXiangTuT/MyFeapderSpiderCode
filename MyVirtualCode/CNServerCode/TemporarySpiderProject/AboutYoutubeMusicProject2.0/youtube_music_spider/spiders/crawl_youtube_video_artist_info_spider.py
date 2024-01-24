# -*- coding: utf-8 -*-
"""
Created on 2023-12-29 18:18:12
---------
@summary:
---------
@author: QiuQiuRen
@description：
    获取当前歌曲的歌手及相关信息
"""

import feapder
from feapder import ArgumentParser
from datetime import datetime
from items.youtube_music_info_item import *


class CrawlYoutubeVideoArtistInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self, task):
        data = {
            "videoId": task.youtube_music_video_id,
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "US",
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20210101.00.00"
                }
            }
        }
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_video_id = task.youtube_music_video_id
        task_youtube_music_video_url = task.youtube_music_video_url
        task_youtube_music_source_remark = task.youtube_music_source_remark
        task_youtube_music_source_playlist_url = task.youtube_music_source_playlist_url
        url = "https://music.youtube.com/youtubei/v1/next?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        yield feapder.Request(url=url, method="POST", json=data,
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_video_id=task_youtube_music_video_id,
                              task_youtube_music_video_url=task_youtube_music_video_url,
                              task_youtube_music_source_remark=task_youtube_music_source_remark,
                              task_youtube_music_source_playlist_url=task_youtube_music_source_playlist_url,
                              )

    def parse(self, request, response):
        json_data = response.json["contents"]["singleColumnMusicWatchNextResultsRenderer"]["tabbedRenderer"][
            "watchNextTabbedResultsRenderer"]["tabs"][0]

        if json_data['tabRenderer']["content"]['musicQueueRenderer'].get("content"):
            youtube_music_video_artist_data_item = YoutubeMusicVideoArtistDataItem()
            youtube_music_video_artist_data_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_video_artist_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_video_artist_data_item["youtube_music_video_id"] = request.task_youtube_music_video_id
            youtube_music_video_artist_data_item["youtube_music_video_url"] = request.task_youtube_music_video_url
            youtube_music_video_artist_data_item["youtube_music_source_remark"] = request.task_youtube_music_source_remark
            youtube_music_video_artist_data_item["youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
            # 1-title
            youtube_music_video_artist_data_item["youtube_music_video_title"] = \
                json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"][
                    "contents"][
                    0]["playlistPanelVideoRenderer"]["title"]["runs"][0]["text"]
            # 2-artist
            youtube_music_video_artist_name_list = \
                json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"][
                    "contents"][
                    0]["playlistPanelVideoRenderer"]["longBylineText"]["runs"]
            index = next((i for i, d in enumerate(youtube_music_video_artist_name_list) if d.get("text") == " • "),
                         None)
            if index == 1:
                youtube_music_video_artist_data_item["youtube_music_video_artist_name"] = youtube_music_video_artist_name_list[0]["text"]
                if youtube_music_video_artist_name_list[0].get("navigationEndpoint"):
                    youtube_music_video_artist_data_item["youtube_music_video_artist_channel_id"] = \
                        youtube_music_video_artist_name_list[0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                else:
                    youtube_music_video_artist_data_item["youtube_music_video_artist_channel_id"] = None
            elif index > 1:
                youtube_music_video_artist_data_item["youtube_music_video_artist_name"] = ";".join(
                    [youtube_music_video_artist_name_list[i]["text"] for i in range(0, index) if i % 2 == 0])
                youtube_music_video_artist_data_item["youtube_music_video_artist_channel_id"] = ";".join(
                    [youtube_music_video_artist_name_list[i]["navigationEndpoint"]["browseEndpoint"]["browseId"] for i
                     in range(0, index) if i % 2 == 0 and youtube_music_video_artist_name_list[i].get("navigationEndpoint")])
            else:
                youtube_music_video_artist_data_item["youtube_music_video_artist_name"] = None
                youtube_music_video_artist_data_item["youtube_music_video_artist_channel_id"] = None

            origin_youtube_music_video_info = youtube_music_video_artist_name_list[index + 1]["text"]
            if "view" in origin_youtube_music_video_info:
                # 3-views
                origin_youtube_music_video_views = youtube_music_video_artist_name_list[index + 1]["text"]
                youtube_music_video_artist_data_item["origin_youtube_music_video_views"] = origin_youtube_music_video_views
                origin_youtube_music_video_views_split = origin_youtube_music_video_views.replace(" views", "").replace(
                    " view", "")
                youtube_music_video_artist_data_item["youtube_music_video_views"] = int(float(origin_youtube_music_video_views_split.lower().replace("k",
                                                                                                                  "")) * 1000) if "k" in origin_youtube_music_video_views_split.lower() else int(
                    float(origin_youtube_music_video_views_split.lower().replace('m',
                                                                                 "")) * 1000000) if "m" in origin_youtube_music_video_views_split.lower() else int(
                    origin_youtube_music_video_views_split.strip())
                # 4-likes
                other_info = youtube_music_video_artist_name_list[index+1:]
                if len(other_info)>1:
                    origin_youtube_music_video_likes = youtube_music_video_artist_name_list[index + 3]["text"]
                    youtube_music_video_artist_data_item["origin_youtube_music_video_likes"] = origin_youtube_music_video_likes
                    origin_youtube_music_video_likes_split = origin_youtube_music_video_likes.replace(" likes", "").replace(
                        " like", "")
                    youtube_music_video_artist_data_item["youtube_music_video_likes"] = int(float(origin_youtube_music_video_likes_split.lower().replace("k",
                                                                                                                  "")) * 1000) if "k" in origin_youtube_music_video_likes_split.lower() else int(
                    float(origin_youtube_music_video_likes_split.lower().replace('m',
                                                                                 "")) * 1000000) if "m" in origin_youtube_music_video_likes_split.lower() else int(
                    origin_youtube_music_video_likes_split.strip())
                elif len(other_info)==1:
                    youtube_music_video_artist_data_item["origin_youtube_music_video_likes"] = None
                    youtube_music_video_artist_data_item["youtube_music_video_likes"] = 0
            else:
                youtube_music_video_artist_data_item["origin_youtube_music_video_views"] = None
                youtube_music_video_artist_data_item["youtube_music_video_views"] = 0
                youtube_music_video_artist_data_item["origin_youtube_music_video_likes"] = None
                youtube_music_video_artist_data_item["youtube_music_video_likes"] = 0

            # 5-image_url
            youtube_music_video_artist_data_item["image_url"] = \
                json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"][
                    "contents"][
                    0]["playlistPanelVideoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
            # 6-duration
            if json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"][
                    "contents"][
                    0]["playlistPanelVideoRenderer"].get("lengthText"):
                origin_duration = \
                    json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"][
                        "contents"][
                        0]["playlistPanelVideoRenderer"]["lengthText"]["runs"][0]["text"]
                youtube_music_video_artist_data_item["origin_duration"] = origin_duration
                parts = origin_duration.split(":")
                if len(parts) == 3:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2])
                else:
                    hours = 0
                    minutes = int(parts[0])
                    seconds = int(parts[1])

                total_seconds = hours * 3600 + minutes * 60 + seconds
                youtube_music_video_artist_data_item["duration"] = total_seconds
            else:
                youtube_music_video_artist_data_item["origin_duration"] = None
                youtube_music_video_artist_data_item["duration"] = 0
            youtube_music_video_artist_data_item["batch"] = self.batch_date
            yield youtube_music_video_artist_data_item

            youtube_music_video_artist_crawl_situation_batch_record_item = YoutubeMusicVideoArtistCrawlSituationBatchRecordItem()
            youtube_music_video_artist_crawl_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_video_artist_crawl_situation_batch_record_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_video_artist_crawl_situation_batch_record_item["youtube_music_video_id"] = request.task_youtube_music_video_id
            youtube_music_video_artist_crawl_situation_batch_record_item["youtube_music_video_url"] = request.task_youtube_music_video_url
            youtube_music_video_artist_crawl_situation_batch_record_item["youtube_music_source_remark"] = request.task_youtube_music_source_remark
            youtube_music_video_artist_crawl_situation_batch_record_item["youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
            youtube_music_video_artist_crawl_situation_batch_record_item["youtube_music_video_artists_infomation_remark"] = "EI"
            youtube_music_video_artist_crawl_situation_batch_record_item["batch"] = self.batch_date
            yield youtube_music_video_artist_crawl_situation_batch_record_item
        else:
            youtube_music_video_artist_crawl_situation_batch_record_item = YoutubeMusicVideoArtistCrawlSituationBatchRecordItem()
            youtube_music_video_artist_crawl_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_video_artist_crawl_situation_batch_record_item[
                "youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_video_artist_crawl_situation_batch_record_item[
                "youtube_music_video_id"] = request.task_youtube_music_video_id
            youtube_music_video_artist_crawl_situation_batch_record_item[
                "youtube_music_video_url"] = request.task_youtube_music_video_url
            youtube_music_video_artist_crawl_situation_batch_record_item[
                "youtube_music_source_remark"] = request.task_youtube_music_source_remark
            youtube_music_video_artist_crawl_situation_batch_record_item[
                "youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
            youtube_music_video_artist_crawl_situation_batch_record_item[
                "youtube_music_video_artists_infomation_remark"] = "NI"
            youtube_music_video_artist_crawl_situation_batch_record_item["batch"] = self.batch_date
            yield youtube_music_video_artist_crawl_situation_batch_record_item
        yield self.update_task_state(request.task_id, 1)

if __name__ == "__main__":
    spider = CrawlYoutubeVideoArtistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeVideoArtistInfoSpider爬虫")

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
    # python crawl_youtube_video_artist_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_video_artist_info_spider.py --start_worker  # 启动爬虫
