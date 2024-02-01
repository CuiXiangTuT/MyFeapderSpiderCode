# -*- coding: utf-8 -*-
"""
Created on 2024-02-01 18:09:50
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser


class CrawlYoutubeArtistVideosInfoSpider(feapder.BatchSpider):
    def start_requests(self, task):
        url = "https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"
        data = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20240131.01.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "originalUrl": "https://www.youtube.com/channnel/" + task.youtube_artist_channel_id + "/videos"
                }
            },
            "browseId": task.youtube_artist_channel_id
        }

        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_artist_channel_id = task.youtube_artist_channel_id
        task_youtube_artist_channel_name = task.youtube_artist_channel_name
        continuationCommand = None
        yield feapder.Request(url=url, json=data, task_id=task_id, task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_artist_channel_id=task_youtube_artist_channel_id,
                              task_youtube_artist_channel_name=task_youtube_artist_channel_name,
                              continuationCommand=continuationCommand)

    def parse(self, request, response):
        if request.continuationCommand==None:
            header_json_data = response.json["header"]
            header_item = dict()
            # 1-youtube_page_channel_id
            header_item["youtube_page_channel_id"] = header_json_data["c4TabbedHeaderRenderer"]["channelId"]
            # 2-youtube_page_channel_title
            header_item["youtube_page_channel_title"] = header_json_data["c4TabbedHeaderRenderer"]["title"]
            # 3-youtube_page_canonical_base_Url
            header_item["youtube_page_canonical_base_Url"] = header_json_data["c4TabbedHeaderRenderer"]["navigationEndpoint"]["browseEndpoint"]["canonicalBaseUrl"]
            # 4-youtube_page_channel_img_url
            header_item["youtube_page_channel_img_url"] = header_json_data["c4TabbedHeaderRenderer"]["avatar"]["thumbnails"][-1]["url"]
            # 5-youtube_page_channel_banner_img_url
            header_item["youtube_page_channel_banner_img_url"] = header_json_data["c4TabbedHeaderRenderer"]["banner"]["thumbnails"][-1]["url"]
            # 6-origin_subscriber_count
            origin_subscriber_count = header_json_data["c4TabbedHeaderRenderer"]["subscriberCountText"]["accessibility"]["accessibilityData"]["label"]
            header_item["origin_subscriber_count"] = origin_subscriber_count
            # 7-subscriber_count
            split_origin_subscriber_count = origin_subscriber_count.lower().replace(" subscribers","").lower(" subscriber","")
            header_item["subscriber_count"] = int(float(origin_subscriber_count.replace("k","").strip())*1000) if 'k' in split_origin_subscriber_count else int(float(origin_subscriber_count.replace("m","").strip())*1000000) if 'm' in split_origin_subscriber_count else int(float(origin_subscriber_count.replace("b","").strip())*1000000000) if 'b' in origin_subscriber_count else origin_subscriber_count
            # 8-youtube_page_channel_tv_banner_img_url
            header_item["youtube_page_channel_tv_banner_img_url"] = header_json_data["c4TabbedHeaderRenderer"]["tvBanner"]["thumbnails"][-1]["url"]
            # 9-videos_count
            header_item["videos_count"] = header_json_data["c4TabbedHeaderRenderer"]["videosCountText"]["runs"][0]["text"]
            meta_data_json = response.json["metadata"]["channelMetadataRenderer"]
            # 10-description
            header_item["description"] = meta_data_json["description"]
            # 11-rss_url
            header_item["rss_url"] = meta_data_json["rssUrl"]
            # 12-external_id
            header_item["external_id"] = meta_data_json["externalId"]
            # 13-keywords
            header_item["keywords"] = meta_data_json["keywords"]
            # 14-owner_urls
            ownerUrls_list = meta_data_json["ownerUrls"]
            header_item["owner_urls"] = ownerUrls_list[0] if len(ownerUrls_list)==1 else ';'.join(ownerUrls_list) if len(ownerUrls_list)>1 else None
            # 15-isFamilySafe
            header_item["is_family_safe"] = 1 if meta_data_json["isFamilySafe"]=="true" else 0
            # 16-available_country_codes
            available_country_codes_list = meta_data_json["availableCountryCodes"]
            header_item["available_country_codes"] = ';'.join(available_country_codes_list) if len(available_country_codes_list)>1 else available_country_codes_list[0] if len(available_country_codes_list)==1 else None
            # 17-section_

        else:
            pass


if __name__ == "__main__":
    spider = CrawlYoutubeArtistVideosInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeArtistVideosInfoSpider爬虫")

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
    # python crawl_youtube_artist_videos_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_artist_videos_info_spider.py --start_worker  # 启动爬虫
