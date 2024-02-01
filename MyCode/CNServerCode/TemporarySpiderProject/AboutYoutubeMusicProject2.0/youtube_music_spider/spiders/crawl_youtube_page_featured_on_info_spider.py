# -*- coding: utf-8 -*-
"""
Created on 2024-01-08 10:43:24
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *
import re


class CrawlYoutubePageFeaturedOnInfoSpider(feapder.BatchSpider):
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
            "context": {
                "client": {
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20231214.00.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "browserName": "Edge Chromium",
                    "browserVersion": "120.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"

                }
            },
            # "browseId": "VL" + task.youtube_music_playlist_id
            "browseId": task.youtube_music_playlist_id
        }
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_playlist_id = task.youtube_music_playlist_id
        task_youtube_music_playlist_url = task.youtube_music_playlist_url
        task_youtube_music_plate_remark = task.youtube_music_plate_remark

        yield feapder.Request(url=url, json=data,
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_playlist_id=task_youtube_music_playlist_id,
                              task_youtube_music_playlist_url=task_youtube_music_playlist_url,
                              task_youtube_music_plate_remark=task_youtube_music_plate_remark,
                              )

    def parse(self, request, response):
        d = dict()
        d["gmg_artist_id"] = request.task_gmg_artist_id
        d["youtube_music_channel_id"] = request.task_youtube_music_channel_id
        d["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
        d["youtube_music_playlist_url"] = request.task_youtube_music_playlist_id
        d["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
        if response.json.get("header"):
            # title
            d["title"] = response.json["header"]["musicDetailHeaderRenderer"]["title"]["runs"][0]["text"]
            d["serial_number"] = 0
            # playlist_type
            d["playlist_type"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][0]["text"]
            # artist_name
            d["artist_name"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2]["text"]
            # publish_date
            d["publish_date"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][4]["text"]
            d["artist_channel_id"] = None
            # origin_songs_count
            origin_songs_count = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][0][
                "text"]
            d["origin_songs_count"] = origin_songs_count
            # songs_count
            d["songs_count"] = origin_songs_count.replace(" songs", "").replace(" song", "").strip()
            # origin_duration
            origin_total_duration = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][2][
                "text"]
            d["origin_total_duration"] = origin_total_duration

            parts = origin_total_duration.split(",")
            hours = 0
            minutes = 0

            for part in parts:
                if "hours" in part or "+" in part:
                    hours = int(part.strip().split()[0].replace("+", "").strip())
                elif "minutes" in part:
                    minutes = int(part.strip().split()[0].replace("+", "").strip())

            total_seconds = hours * 3600 + minutes * 60

            d["total_duration"] = total_seconds
            d["url_canonical"] = None
            # description
            if response.json["header"]["musicDetailHeaderRenderer"].get("description"):
                d["description"] = response.json["header"]["musicDetailHeaderRenderer"]["description"]["runs"][0][
                    "text"]
            else:
                d["description"] = None
            # img_url
            d["img_url"] = \
                response.json["header"]["musicDetailHeaderRenderer"]["thumbnail"]["croppedSquareThumbnailRenderer"][
                    "thumbnail"]["thumbnails"][-1]["url"]
        else:
            d["title"] = None
            d["serial_number"] = None
            d["playlist_type"] = None
            d["artist_name"] = None
            d["publish_date"] = None
            d["artist_channel_id"] = None
            d["origin_songs_count"] = None
            d["songs_count"] = None
            d["origin_total_duration"] = None
            d["total_duration"] = 0
            d["url_canonical"] = None
            d["description"] = None
            d["img_url"] = None

        songs_info_list = \
            response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]
        for per_song_info in songs_info_list:
            youtube_music_artist_plate_data_item = YoutubeMusicArtistPlateDataNewItem()
            youtube_music_artist_plate_data_item["gmg_artist_id"] = d["gmg_artist_id"]
            youtube_music_artist_plate_data_item["youtube_music_channel_id"] = d["youtube_music_channel_id"]
            youtube_music_artist_plate_data_item["youtube_music_playlist_id"] = d["youtube_music_playlist_id"]
            youtube_music_artist_plate_data_item["youtube_music_playlist_url"] = d["youtube_music_playlist_url"]
            youtube_music_artist_plate_data_item["youtube_music_plate_remark"] = d["youtube_music_plate_remark"]
            youtube_music_artist_plate_data_item["title"] = d["title"]
            youtube_music_artist_plate_data_item["serial_number"] = d["serial_number"]
            youtube_music_artist_plate_data_item["playlist_type"] = d["playlist_type"]
            youtube_music_artist_plate_data_item["artist_name"] = d["artist_name"]
            youtube_music_artist_plate_data_item["publish_date"] = d["publish_date"]
            youtube_music_artist_plate_data_item["artist_channel_id"] = d["artist_channel_id"]
            youtube_music_artist_plate_data_item["origin_songs_count"] = d["origin_songs_count"]
            youtube_music_artist_plate_data_item["songs_count"] = d["songs_count"]
            youtube_music_artist_plate_data_item["origin_total_duration"] = d["origin_total_duration"]
            youtube_music_artist_plate_data_item["total_duration"] = d["total_duration"]
            youtube_music_artist_plate_data_item["url_canonical"] = d["url_canonical"]
            youtube_music_artist_plate_data_item["description"] = d["description"]
            youtube_music_artist_plate_data_item["img_url"] = d["img_url"]

            # songs_url
            youtube_music_artist_plate_data_item["youtube_music_video_img_url"] = \
                per_song_info["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"][0]["url"]
            # youtube_music_video_id
            youtube_music_artist_plate_data_item["youtube_music_video_id"] = \
                per_song_info["musicResponsiveListItemRenderer"]["playlistItemData"][
                    "videoId"]
            youtube_music_artist_plate_data_item["youtube_music_video_url"] = "https://music.youtube.com/watch?v=" + \
                                                                              youtube_music_artist_plate_data_item[
                                                                                  "youtube_music_video_id"]
            youtube_music_artist_plate_data_item["origin_youtube_music_video_url"] = None
            youtube_music_artist_plate_data_item["youtube_music_video_url_split_playlist_id"] = None
            youtube_music_artist_plate_data_item["youtube_music_video_url_split_playlist_url"] = None
            youtube_music_artist_plate_data_item["origin_youtube_music_video_play_count"] = None
            youtube_music_artist_plate_data_item["youtube_music_video_play_count"] = None

            # youtube_music_video_name
            youtube_music_artist_plate_data_item["youtube_music_video_name"] = \
                per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][0][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
            # youtube_music_video_artist_name
            youtube_music_video_artist_name_list = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][1][
                "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"]
            if len(youtube_music_video_artist_name_list) == 1:
                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = \
                    youtube_music_video_artist_name_list[0]["text"]
                if youtube_music_video_artist_name_list[0].get("navigationEndpoint"):
                    youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = \
                        youtube_music_video_artist_name_list[0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                else:
                    youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = None
            elif len(youtube_music_video_artist_name_list) > 1:
                artist_names = ";".join([k["text"] for k in youtube_music_video_artist_name_list if k["text"] != " & "])
                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = artist_names

                artist_channel_ids = ";".join(
                    [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in youtube_music_video_artist_name_list
                     if k.get("navigationEndpoint")])
                youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = artist_channel_ids
            else:
                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = None
                youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = None
            # addition_infomation
            other_info = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][2][
                "musicResponsiveListItemFlexColumnRenderer"]
            if other_info["text"].get("runs"):
                if other_info["text"]["runs"][0].get("navigationEndpoint"):
                    youtube_music_artist_plate_data_item["other_info"] = other_info["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_name"] = \
                        other_info["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_id"] = \
                        other_info["text"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                    youtube_music_artist_plate_data_item[
                        "origin_youtube_music_playlist_url"] = "https://music.youtube.com/browse/" + str(
                        youtube_music_artist_plate_data_item["youtube_music_playlist_id"])
                    youtube_music_artist_plate_data_item["youtube_music_playlist_url_pre_redirect"] = \
                        youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"]
                else:
                    youtube_music_artist_plate_data_item["other_info"] = other_info["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_name"] = None
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_id"] = None
                    youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"] = None
                    youtube_music_artist_plate_data_item["youtube_music_playlist_url_pre_redirect"] = \
                        youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"]

            else:
                youtube_music_artist_plate_data_item["other_info"] = None
                youtube_music_artist_plate_data_item["youtube_music_video_playlist_name"] = None
                youtube_music_artist_plate_data_item["youtube_music_video_playlist_id"] = None
                youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"] = None
                youtube_music_artist_plate_data_item["youtube_music_playlist_url_pre_redirect"] = \
                    youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"]

                # origin_duration
            origin_duration = per_song_info["musicResponsiveListItemRenderer"]["fixedColumns"][0][
                "musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
            youtube_music_artist_plate_data_item["origin_duration"] = origin_duration
            # duration
            if "+" not in origin_duration:
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
            else:
                match = re.search(r"(\d+)\s*\+\s*hours", origin_duration)
                if match:
                    hours = int(match.group(1))
                    total_seconds = hours * 3600
                else:
                    total_seconds = 0
            youtube_music_artist_plate_data_item["duration"] = total_seconds
            # playlist_set_video_id
            youtube_music_artist_plate_data_item["youtube_music_playlist_set_video_id"] = \
                per_song_info["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
            youtube_music_artist_plate_data_item["is_playable"] = 1
            youtube_music_artist_plate_data_item["batch"] = self.batch_date
            yield youtube_music_artist_plate_data_item

        if response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"].get("continuations"):
            continuation = \
                response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                    "sectionListRenderer"]["continuations"][0]["nextContinuationData"]["continuation"]
            related_playlists_params_data = {
                "context": {
                    "client": {
                        "clientName": "WEB_REMIX",
                        "clientVersion": "1.20231214.00.00",
                    }
                }
            }
            related_playlists_url = "https://music.youtube.com/youtubei/v1/browse?continuation={}&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false".format(
                continuation)
            yield feapder.Request(url=related_playlists_url, json=related_playlists_params_data,
                                  task_id=request.task_id,
                                  task_gmg_artist_id=request.task_gmg_artist_id,
                                  task_youtube_music_channel_id=request.task_youtube_music_channel_id,
                                  task_youtube_music_playlist_id=request.task_youtube_music_playlist_id,
                                  task_youtube_music_playlist_url=request.task_youtube_music_playlist_url,
                                  task_youtube_music_plate_remark=request.task_youtube_music_plate_remark,
                                  callback=self.parse1
                                  )
        yield self.update_task_batch(request.task_id, 1)

    def parse1(self, request, response):
        json_data = \
            response.json["continuationContents"]["sectionListContinuation"]["contents"][0][
                "musicCarouselShelfRenderer"][
                "contents"]
        for per_json_data in json_data:
            youtube_music_related_playlists_info_batch_data_item = YoutubeMusicRelatedPlaylistsInfoBatchDataItem()
            youtube_music_related_playlists_info_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_related_playlists_info_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_related_playlists_info_batch_data_item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
            youtube_music_related_playlists_info_batch_data_item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_id
            youtube_music_related_playlists_info_batch_data_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark

            # img_url
            youtube_music_related_playlists_info_batch_data_item["img_url"] = \
                per_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"]["musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"][-1]["url"]
            # title
            youtube_music_related_playlists_info_batch_data_item["title"] = per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
            # youtube_music_playlist_id
            youtube_music_related_playlist_id = \
                per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"][
                    "browseId"]
            youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_id"] = youtube_music_related_playlist_id
            # youtube_music_related_playlist_url
            youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_url"] = "https://music.youtube.com/playlist?list="+youtube_music_related_playlist_id[2:]
            info = per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"]
            youtube_music_related_playlists_info_batch_data_item["playlist_type"] = info[0]["text"]
            # youtube_music_related_playlist_artist_name
            youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_artist_name"] = info[2]["text"]
            if info[2].get("navigationEndpoint"):
                youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_artist_channel_id"] = info[2]["navigationEndpoint"]["browseEndpoint"][
                    "browseId"]
                youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_artist_channel_url"] = "https://music.youtube.com/channel/" + str(
                    youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_artist_channel_id"])
            else:
                youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_artist_channel_id"] = None
                youtube_music_related_playlists_info_batch_data_item["youtube_music_related_playlist_artist_channel_url"] = None
            if len(per_json_data["musicTwoRowItemRenderer"]["subtitle"]) == 5:
                origin_views = info[-1]["text"]
                youtube_music_related_playlists_info_batch_data_item["origin_views"] = origin_views
                flex_views = origin_views.replace(" views", "").replace(" view", "")
                youtube_music_related_playlists_info_batch_data_item["views"] = int(
                    float(flex_views.lower().replace("k", "")) * 1000) if "k" in flex_views.lower() else int(
                    float(flex_views.lower().replace('m', "")) * 1000000) if "m" in flex_views.lower() else int(
                    float(flex_views.lower().replace("b", "")) * 1000000000) if "b" in flex_views.lower() else int(
                    flex_views)
            else:
                youtube_music_related_playlists_info_batch_data_item["origin_views"] = None
                youtube_music_related_playlists_info_batch_data_item["views"] = 0
            youtube_music_related_playlists_info_batch_data_item["batch"] = self.batch_date
            yield youtube_music_related_playlists_info_batch_data_item

if __name__ == "__main__":
    spider = CrawlYoutubePageFeaturedOnInfoSpider(

        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24

    )

    parser = ArgumentParser(description="CrawlYoutubePageFeaturedOnInfoSpider爬虫")

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
# python crawl_youtube_page_featured_on_info_spider.py --start_master  # 添加任务
# python crawl_youtube_page_featured_on_info_spider.py --start_worker  # 启动爬虫
