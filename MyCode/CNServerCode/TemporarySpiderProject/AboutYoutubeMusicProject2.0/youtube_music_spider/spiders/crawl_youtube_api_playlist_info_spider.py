# -*- coding: utf-8 -*-
"""
Created on 2024-01-03 10:50:08
---------
@summary:
---------
@author: QiuQiuRen
@description：
    获取API接口下的所有歌曲列表Video id
"""

import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *
from feapder.db.redisdb import RedisDB
from datetime import datetime
from feapder.utils.log import log
import os

class CrawlYoutubeApiPlaylistInfoSpider(feapder.BatchSpider):
    redis_db = RedisDB(decode_responses=True)
    # url = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=id&part=liveStreamingDetails&part=localizations&part=player&part=recordingDetails&part=snippet&part=statistics&part=status&part=topicDetails&maxResults=50"
    youtube_key = "&key={}"

    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept': 'application/json'
        }
        keys = self.redis_db.zrangebyscore_increase_score('youtube_quota', 0, 9999, 1, count=1)
        if len(keys) == 1:
            request.url += self.youtube_key.format(keys[0])
            return request
        else:
            log.info("所有的key均不可用，终止爬虫")
            os._exit(0)

    def start_requests(self, task):
        url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&part=id&part=snippet&part=status&maxResults=50'
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_channel_id = task.youtube_music_channel_id
        task_crawl_condition_youtube_playlist_id = task.youtube_music_playlist_id
        task_youtube_plate_remark = task.youtube_music_plate_remark
        yield feapder.Request(url=url + str("&playlistId=" + task_crawl_condition_youtube_playlist_id),
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_channel_id=task_youtube_channel_id,
                              task_crawl_condition_youtube_playlist_id=task_crawl_condition_youtube_playlist_id,
                              task_youtube_plate_remark=task_youtube_plate_remark
                              )

    def parse(self, request, response):
        if response.json.get("items"):
            data_json_list = response.json["items"]

            for per_json_data in data_json_list:
                api_youtube_playlist_info_data_item = ApiYoutubePlaylistInfoDataItem()
                # 1-gmg_artist_id
                api_youtube_playlist_info_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                # 2-youtube_channel_id
                api_youtube_playlist_info_data_item["youtube_channel_id"] = request.task_youtube_channel_id
                # 3-crawl_condition_youtube_playlist_id
                api_youtube_playlist_info_data_item["crawl_condition_youtube_playlist_id"] = request.task_crawl_condition_youtube_playlist_id
                # 4-kind
                api_youtube_playlist_info_data_item["youtube_playlist_kind"] = per_json_data["kind"]
                # 5-etag
                api_youtube_playlist_info_data_item["youtube_playlist_etag"] = per_json_data["etag"]
                # 6-youtube_unique_id
                api_youtube_playlist_info_data_item["youtube_unique_id"] = per_json_data["id"]
                # 7-youtube_published_at
                api_youtube_playlist_info_data_item["origin_youtube_published_at"] = per_json_data["snippet"]["publishedAt"]
                api_youtube_playlist_info_data_item["youtube_published_at"] = datetime.strptime(api_youtube_playlist_info_data_item["origin_youtube_published_at"],
                                                              "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
                # 8-youtube_playlist_channel_id
                api_youtube_playlist_info_data_item["youtube_playlist_channel_id"] = per_json_data["snippet"]["channelId"]
                # 9-youtube_video_id
                api_youtube_playlist_info_data_item["youtube_video_id"] = per_json_data["contentDetails"]["videoId"]
                # 10-youtube_video_name
                api_youtube_playlist_info_data_item["youtube_video_name"] = per_json_data["snippet"]["title"]
                # 11-description
                api_youtube_playlist_info_data_item["description"] = per_json_data["snippet"]["description"]
                # 12-image_url
                api_youtube_playlist_info_data_item["image_url"] = per_json_data["snippet"]["thumbnails"]["high"]["url"]
                # 13-youtube_playlist_id
                api_youtube_playlist_info_data_item["youtube_playlist_id"] = per_json_data["snippet"]["playlistId"]
                # 14-youtube_video_position
                api_youtube_playlist_info_data_item["youtube_video_position"] = int(per_json_data["snippet"]["position"])+1
                # 15-youtube_resource_id_kind
                api_youtube_playlist_info_data_item["youtube_resource_id_kind"] = per_json_data["snippet"]["resourceId"]["kind"]
                # 16-youtube_resource_id_video_id
                api_youtube_playlist_info_data_item["youtube_resource_id_video_id"] = per_json_data["snippet"]["resourceId"]["videoId"]
                # 17-youtube_video_owner_channel_title
                api_youtube_playlist_info_data_item["youtube_video_owner_channel_title"] = per_json_data["snippet"]["videoOwnerChannelTitle"]
                # 18-youtube_video_owner_channel_id
                api_youtube_playlist_info_data_item["youtube_video_owner_channel_id"] = per_json_data["snippet"]["videoOwnerChannelId"]
                # 19-origin_youtube_video_publish_date
                api_youtube_playlist_info_data_item["origin_youtube_video_publish_date"] = per_json_data["contentDetails"]["videoPublishedAt"]
                # 20-youtube_video_publish_date
                api_youtube_playlist_info_data_item["youtube_video_publish_date"] = datetime.strptime(api_youtube_playlist_info_data_item["origin_youtube_video_publish_date"],
                                                                    "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
                # 21-youtube_video_privacy_status
                api_youtube_playlist_info_data_item["youtube_video_privacy_status"] = per_json_data["status"]["privacyStatus"]
                # 22-youtube_video_remark
                api_youtube_playlist_info_data_item["youtube_video_remark"] = request.task_youtube_plate_remark
                api_youtube_playlist_info_data_item["batch"] = self.batch_date
                yield api_youtube_playlist_info_data_item

            if response.json.get('nextPageToken'):
                next_page_token = response.json["nextPageToken"]
                next_url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&part=id&part=snippet&part=status&maxResults=50'
                task_id = request.task_id
                task_gmg_artist_id = request.task_gmg_artist_id
                task_youtube_channel_id = request.task_youtube_channel_id
                task_crawl_condition_youtube_playlist_id = request.task_crawl_condition_youtube_playlist_id
                task_youtube_plate_remark = request.task_youtube_plate_remark
                yield feapder.Request(url=next_url + str(
                    "&playlistId=" + request.task_crawl_condition_youtube_playlist_id) + "&pageToken=" + str(next_page_token),
                                      task_id=task_id,
                                      task_gmg_artist_id=task_gmg_artist_id,
                                      task_youtube_channel_id=task_youtube_channel_id,
                                      task_crawl_condition_youtube_playlist_id=task_crawl_condition_youtube_playlist_id,
                                      task_youtube_plate_remark=task_youtube_plate_remark
                                      )
            yield self.update_task_state(request.task_id, 1)
        else:
            yield self.update_task_state(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlYoutubeApiPlaylistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeApiPlaylistInfoSpider爬虫")

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
    # python crawl_youtube_api_playlist_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_api_playlist_info_spider.py --start_worker  # 启动爬虫
