# -*- coding: utf-8 -*-
"""
Created on 2023-12-29 18:18:01
---------
@summary:
---------
@author: QiuQiuRen
@description：
    获取当前歌曲的播放量及相关信息
"""

import feapder
from feapder import ArgumentParser
from datetime import datetime
from items.youtube_music_info_item import *


class CrawlYoutubeVideoViewsInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
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
                    "clientVersion": "1.20210101.00.00",
                    "osName": "Windows",
                    "osVersion": "10.0"
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
        url = "https://music.youtube.com/youtubei/v1/player?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        yield feapder.Request(url=url, method="POST", json=data,
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_video_id=task_youtube_music_video_id,
                              task_youtube_music_video_url=task_youtube_music_video_url,
                              task_youtube_music_source_remark=task_youtube_music_source_remark,
                              task_youtube_music_source_playlist_url=task_youtube_music_source_playlist_url,
                              )

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("response code not 200")  # 重试
            


    def parse(self, request, response):
        json_data = response.json
        youtube_music_video_views_data_item = YoutubeMusicVideoViewsDataItem()
        youtube_music_video_views_data_item["gmg_artist_id"] = request.task_gmg_artist_id
        youtube_music_video_views_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
        youtube_music_video_views_data_item["youtube_music_video_id"] = request.task_youtube_music_video_id
        youtube_music_video_views_data_item["youtube_music_video_url"] = request.task_youtube_music_video_url
        youtube_music_video_views_data_item["youtube_music_source_remark"] = request.task_youtube_music_source_remark
        youtube_music_video_views_data_item[
            "youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url


        # 歌曲是否可看
        youtube_music_video_views_data_item["origin_is_playable"] = json_data["playabilityStatus"]["status"]
        if youtube_music_video_views_data_item["origin_is_playable"] in ["OK","UNPLAYABLE","CONTENT_CHECK_REQUIRED","LOGIN_REQUIRED"]:
            # 1-youtube_video_id
            youtube_music_video_views_data_item["is_playable"] = 1 if youtube_music_video_views_data_item["origin_is_playable"]=="OK" else 2
            # 2-youtube_video_name
            youtube_music_video_views_data_item["youtube_music_video_name"] = json_data["videoDetails"]["title"]
            # 3-duration
            youtube_music_video_views_data_item["duration"] = json_data["videoDetails"]["lengthSeconds"]
            # 4-image_url
            youtube_music_video_views_data_item["image_url"] = json_data["videoDetails"]["thumbnail"]["thumbnails"][-1][
                "url"]
            # 5-view_count
            youtube_music_video_views_data_item["youtube_music_view_count"] = json_data["videoDetails"]["viewCount"]
            # 6-author
            youtube_music_video_views_data_item["youtube_music_author"] = json_data["videoDetails"]["author"]
            # 7-isPrivate
            youtube_music_video_views_data_item["youtube_music_video_is_private"] = 1 if json_data["videoDetails"][
                                                                                             "isPrivate"] == "true" else 0
            # 8-urlCanonical
            youtube_music_video_views_data_item["youtube_music_video_url_canonical"] = \
            json_data["microformat"]["microformatDataRenderer"]["urlCanonical"]
            # 9-title
            youtube_music_video_views_data_item["youtube_music_video_title"] = \
            json_data["microformat"]["microformatDataRenderer"]["title"]
            # 10-description
            youtube_music_video_views_data_item["description"] = json_data["microformat"]["microformatDataRenderer"][
                "description"]
            # 11-tags
            if response.json["microformat"]["microformatDataRenderer"].get('tags'):
                tags_list = json_data["microformat"]["microformatDataRenderer"]["tags"]
                if len(tags_list) >= 1:
                    youtube_music_video_views_data_item["youtube_music_video_tags"] = ','.join(tags_list) if len(
                        tags_list) > 1 else tags_list[0]
                else:
                    youtube_music_video_views_data_item["youtube_music_video_tags"] = None
            else:
                youtube_music_video_views_data_item["youtube_music_video_tags"] = None
            # 12-name
            youtube_music_video_views_data_item["youtube_music_external_channel_name"] = \
                json_data["microformat"]["microformatDataRenderer"]["pageOwnerDetails"]["name"]
            # 13-external_channel_id
            youtube_music_video_views_data_item["youtube_music_external_channel_id"] = \
            json_data["microformat"]["microformatDataRenderer"]["pageOwnerDetails"][
                "externalChannelId"]
            youtube_music_video_views_data_item[
                "youtube_music_external_channel_url"] = "https://www.youtube.com/channel/" + \
                                                        youtube_music_video_views_data_item[
                                                            "youtube_music_external_channel_id"]
            # 14-youtube_profile_url
            youtube_music_video_views_data_item["youtube_music_profile_url"] = \
            json_data["microformat"]["microformatDataRenderer"]["pageOwnerDetails"][
                "youtubeProfileUrl"]
            # 15-youtube_external_video_id
            youtube_music_video_views_data_item["youtube_music_external_video_id"] = \
            json_data["microformat"]["microformatDataRenderer"]["videoDetails"][
                "externalVideoId"]
            # 16-youtube_external_duration
            youtube_music_video_views_data_item["youtube_music_external_duration"] = \
            json_data["microformat"]["microformatDataRenderer"]["videoDetails"][
                "durationSeconds"]
            # 17-youtube_external_duration_iso
            youtube_music_video_views_data_item["youtube_music_external_duration_iso"] = \
            json_data["microformat"]["microformatDataRenderer"]["videoDetails"][
                "durationIso8601"]
            # 18-publish_date
            origin_youtube_video_publish_date = json_data["microformat"]["microformatDataRenderer"]["publishDate"]
            youtube_music_video_views_data_item[
                "origin_youtube_music_video_publish_date"] = origin_youtube_video_publish_date
            youtube_music_video_views_data_item["youtube_music_video_publish_date"] = datetime.fromisoformat(
                origin_youtube_video_publish_date).strftime(
                "%Y-%m-%d %H:%M:%S")
            # 19-category
            youtube_music_video_views_data_item["youtube_music_video_category"] = \
            json_data["microformat"]["microformatDataRenderer"]["category"]
            # 20-upload_date
            origin_youtube_video_upload_date = json_data["microformat"]["microformatDataRenderer"]["uploadDate"]
            youtube_music_video_views_data_item[
                "origin_youtube_music_video_upload_date"] = origin_youtube_video_upload_date
            youtube_music_video_views_data_item["youtube_music_video_upload_date"] = datetime.fromisoformat(
                origin_youtube_video_upload_date).strftime(
                "%Y-%m-%d %H:%M:%S")
            # 21-availableCountries
            if response.json["microformat"]["microformatDataRenderer"].get("availableCountries"):
                youtube_video_available_countries_list = json_data["microformat"]["microformatDataRenderer"][
                    "availableCountries"]
                if len(youtube_video_available_countries_list) >= 1:
                    youtube_music_video_views_data_item["youtube_music_video_available_countries"] = ','.join(
                        youtube_video_available_countries_list) if len(
                        youtube_video_available_countries_list) > 1 else youtube_video_available_countries_list[0]
                else:
                    youtube_music_video_views_data_item["youtube_music_video_available_countries"] = None
            else:
                youtube_music_video_views_data_item["youtube_music_video_available_countries"] = None
            youtube_music_video_views_data_item["batch"] = self.batch_date
            yield youtube_music_video_views_data_item

            youtube_music_video_views_situation_batch_record_item = YoutubeMusicVideoViewsCrawlSituationBatchRecordItem()
            youtube_music_video_views_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_video_id"] = request.task_youtube_music_video_id
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_source_remark"] = request.task_youtube_music_source_remark
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
            youtube_music_video_views_situation_batch_record_item["youtube_music_video_views_infomation_remark"] = "EI"
            if json_data["playabilityStatus"].get("reason"):
                youtube_music_video_views_situation_batch_record_item["exception_info"] = None if youtube_music_video_views_data_item["origin_is_playable"]=="OK" else json_data["playabilityStatus"]["reason"]
            elif json_data["playabilityStatus"].get("errorScreen"):
                youtube_music_video_views_situation_batch_record_item["exception_info"] = None if youtube_music_video_views_data_item["origin_is_playable"] == "OK" else json_data["playabilityStatus"]["errorScreen"]["playerErrorMessageRenderer"]["reason"]["runs"][0]["text"]
            else:
                youtube_music_video_views_situation_batch_record_item["exception_info"] = None if youtube_music_video_views_data_item["origin_is_playable"] == "OK" else "需要标记"
            youtube_music_video_views_situation_batch_record_item["batch"] = self.batch_date
            yield youtube_music_video_views_situation_batch_record_item
        else:
            youtube_music_video_views_situation_batch_record_item = YoutubeMusicVideoViewsCrawlSituationBatchRecordItem()
            youtube_music_video_views_situation_batch_record_item["origin_is_playable"] = json_data["playabilityStatus"]["reason"]
            youtube_music_video_views_situation_batch_record_item["is_playable"] = 0
            youtube_music_video_views_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_video_id"] = request.task_youtube_music_video_id
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_source_remark"] = request.task_youtube_music_source_remark
            youtube_music_video_views_situation_batch_record_item[
                "youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
            youtube_music_video_views_situation_batch_record_item["youtube_music_video_views_infomation_remark"] = "NI"
            if json_data["playabilityStatus"].get("reason"):
                youtube_music_video_views_situation_batch_record_item["exception_info"] = json_data["playabilityStatus"][
                    "reason"]
            else:
                youtube_music_video_views_situation_batch_record_item["exception_info"] = None
            youtube_music_video_views_situation_batch_record_item["batch"] = self.batch_date
            yield youtube_music_video_views_situation_batch_record_item
        yield self.update_task_state(request.task_id, 1)

if __name__ == "__main__":
    spider = CrawlYoutubeVideoViewsInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeVideoViewsInfoSpider爬虫")

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
    # python crawl_youtube_video_views_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_video_views_info_spider.py --start_worker  # 启动爬虫
