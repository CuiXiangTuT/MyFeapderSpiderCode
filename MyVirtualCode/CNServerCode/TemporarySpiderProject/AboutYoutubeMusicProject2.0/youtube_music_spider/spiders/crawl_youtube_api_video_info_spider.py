# -*- coding: utf-8 -*-
"""
Created on 2024-01-03 10:50:29
---------
@summary:
---------
@author: QiuQiuRen
@description：
    获取youtube api下的歌曲信息，包含播放量
"""

import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *
from feapder.db.redisdb import RedisDB
from datetime import datetime
from feapder.utils.log import log
import os
import isodate


class CrawlYoutubeApiVideoInfoSpider(feapder.BatchSpider):
    redis_db = RedisDB(decode_responses=True)
    url = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=id&part=liveStreamingDetails&part=localizations&part=player&part=recordingDetails&part=snippet&part=statistics&part=status&part=topicDetails&maxResults=50"
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
        url = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=id&part=liveStreamingDetails&part=localizations&part=player&part=recordingDetails&part=snippet&part=statistics&part=status&part=topicDetails&maxResults=50"
        # url = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=id&part=liveStreamingDetails&part=localizations&part=player&part=recordingDetails&part=snippet&part=statistics&part=status&part=topicDetails&maxResults=50&key="
        task_id = task.id
        task_youtube_video_ids = task.youtube_video_ids
        # task_youtube_video_ids_md5 = task.youtube_video_ids_md5
        yield feapder.Request(url=url+str(task_youtube_video_ids),
                              task_id=task_id,
                              task_youtube_video_ids=task_youtube_video_ids,
                              )

    def parse(self, request, response):
        json_data_list = response.json['items']
        for per_json in json_data_list:
            api_youtube_video_info_data_item = ApiYoutubeVideoInfoDataItem()
            # 1-youtube_video_kind
            api_youtube_video_info_data_item["youtube_video_kind"] = per_json["kind"]
            # 2-youtube_video_etag
            api_youtube_video_info_data_item["youtube_video_etag"] = per_json["etag"]
            # 补：3-youtube_video_id
            api_youtube_video_info_data_item["youtube_video_id"] = per_json["id"]
            # 3-youtube_video_published_at
            api_youtube_video_info_data_item["origin_youtube_video_published_at"] = per_json["snippet"]["publishedAt"]
            api_youtube_video_info_data_item["youtube_video_published_at"] = datetime.strptime(api_youtube_video_info_data_item["origin_youtube_video_published_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
            # 4-youtube_video_channel_id
            api_youtube_video_info_data_item["youtube_video_channel_id"] = per_json["snippet"]["channelId"]
            # 5-youtube_video_name
            api_youtube_video_info_data_item["youtube_video_name"] = per_json["snippet"]["title"]
            # 6-description
            api_youtube_video_info_data_item["description"] = per_json["snippet"]["description"]
            # 7-image_url
            api_youtube_video_info_data_item["image_url"] = per_json["snippet"]["thumbnails"]["high"]["url"]
            # 8-youtube_video_owner_channel_title
            api_youtube_video_info_data_item["youtube_video_owner_channel_title"] = per_json["snippet"]["channelTitle"]
            # 9-youtube_video_relate_tags
            if "tags" in str(per_json["snippet"]):
                if len(per_json["snippet"]["tags"])>=1:
                    api_youtube_video_info_data_item["youtube_video_relate_tags"] = ','.join(per_json["snippet"]["tags"]) if len(per_json["snippet"]["tags"])>1 else per_json["snippet"]["tags"][0]
                else:
                    api_youtube_video_info_data_item["youtube_video_relate_tags"] = None
            else:
                api_youtube_video_info_data_item["youtube_video_relate_tags"] = None

            # 10-youtube_video_category_id
            api_youtube_video_info_data_item["youtube_video_category_id"] = per_json["snippet"]["categoryId"]
            # 11-youtube_video_localized_title
            api_youtube_video_info_data_item["youtube_video_localized_title"] = per_json["snippet"]["localized"]["title"]
            # 12-youtube_video_localized_description
            api_youtube_video_info_data_item["youtube_video_localized_description"] = per_json["snippet"]["localized"]["description"]
            # 13-origin_duration
            api_youtube_video_info_data_item["origin_duration"] = per_json["contentDetails"]["duration"]
            # 14-duration
            duration = isodate.parse_duration(api_youtube_video_info_data_item["origin_duration"])
            total_seconds = duration.total_seconds()
            api_youtube_video_info_data_item["duration"] = int(total_seconds)
            # 15-youtube_video_dimension
            api_youtube_video_info_data_item["youtube_video_dimension"] = per_json["contentDetails"]["dimension"]
            # 16-youtube_video_definition
            api_youtube_video_info_data_item["youtube_video_definition"] = per_json["contentDetails"]["definition"]
            # 17-youtube_video_caption
            api_youtube_video_info_data_item["youtube_video_caption"] = 1 if per_json["contentDetails"]["caption"]=="true" else 0
            # 18-youtube_video_license
            api_youtube_video_info_data_item["youtube_video_licensed_content"] = 1 if per_json["contentDetails"]["licensedContent"]=="true" else 0
            if "regionRestriction" in str(per_json["contentDetails"]):
                if "allowed" in str(per_json["contentDetails"]["regionRestriction"]):
                    # 19-youtube_video_region_restriction_allowed
                    api_youtube_video_info_data_item["youtube_video_region_restriction_allowed"] = ','.join(per_json["contentDetails"]["regionRestriction"]["allowed"]) if len(per_json["contentDetails"]["regionRestriction"]["allowed"])>1 else per_json["contentDetails"]["regionRestriction"]["allowed"][0]
                else:
                    api_youtube_video_info_data_item["youtube_video_region_restriction_allowed"] = None
                if 'blocked' in str(per_json["contentDetails"]["regionRestriction"]):
                    # 20-youtube_video_region_restriction_blocked
                    api_youtube_video_info_data_item["youtube_video_region_restriction_blocked"] = ','.join(per_json["contentDetails"]["regionRestriction"]["blocked"]) if len(per_json["contentDetails"]["regionRestriction"]["blocked"])>1 else per_json["contentDetails"]["regionRestriction"]["blocked"][0]
                else:
                    api_youtube_video_info_data_item["youtube_video_region_restriction_blocked"] = None
            else:
                api_youtube_video_info_data_item["youtube_video_region_restriction_allowed"] = None
                api_youtube_video_info_data_item["youtube_video_region_restriction_blocked"] = None
            # 21-youtube_video_content_rating
            api_youtube_video_info_data_item["youtube_video_content_rating"] = per_json["contentDetails"]["contentRating"]
            # 22-youtube_video_projection
            api_youtube_video_info_data_item["youtube_video_projection"] = per_json["contentDetails"]["projection"]
            # 23-youtube_video_upload_status
            api_youtube_video_info_data_item["youtube_video_upload_status"] = per_json["status"]["uploadStatus"]
            # 24-youtube_video_privacy_status
            api_youtube_video_info_data_item["youtube_video_privacy_status"] = per_json["status"]["privacyStatus"]
            # 25-youtube_video_license
            api_youtube_video_info_data_item["youtube_video_license"] = per_json["status"]["license"]
            # 26-youtube_video_embeddable
            api_youtube_video_info_data_item["youtube_video_embeddable"] = 1 if per_json["status"]["embeddable"]=="true" else 0
            # 27-youtube_video_public_stats_viewable
            api_youtube_video_info_data_item["youtube_video_public_stats_viewable"] = 1 if per_json["status"]["publicStatsViewable"]=="true" else 0
            # 28-youtube_video_made_for_kids
            api_youtube_video_info_data_item["youtube_video_made_for_kids"] = 1 if per_json["status"]["madeForKids"]=="true" else 0
            # 29-youtube_video_view_count
            api_youtube_video_info_data_item["youtube_video_view_count"] = per_json["statistics"]["viewCount"]
            # 30-youtube_video_like_count
            api_youtube_video_info_data_item["youtube_video_like_count"] = per_json["statistics"]["likeCount"]
            # 31-youtube_video_comment_count
            if "commentCount" in str(per_json["statistics"]):
                api_youtube_video_info_data_item["youtube_video_comment_count"] = per_json["statistics"]["commentCount"]
            else:
                api_youtube_video_info_data_item["youtube_video_comment_count"] = 0
            # 32-youtube_video_topic_categories
            if len(per_json["topicDetails"]["topicCategories"])>=1:
                api_youtube_video_info_data_item["youtube_video_topic_categories"] = ';'.join(per_json["topicDetails"]["topicCategories"]) if len(per_json["topicDetails"]["topicCategories"])>1 else per_json["topicDetails"]["topicCategories"][0]
            else:
                api_youtube_video_info_data_item["youtube_video_topic_categories"] = None
            api_youtube_video_info_data_item["batch"] = self.batch_date
            yield api_youtube_video_info_data_item
        yield self.update_task_state(request.task_id, 1)

if __name__ == "__main__":
    spider = CrawlYoutubeApiVideoInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeApiVideoInfoSpider爬虫")

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
    # python crawl_youtube_api_video_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_api_video_info_spider.py --start_worker  # 启动爬虫
