import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os
import isodate
from pprint import pprint
from datetime import datetime,timedelta
from copy import deepcopy
import re

class MyTestAirspider(feapder.AirSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
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
            "browseId": "VL" + "RDCLAK5uy_mijutvVbzp7bbNlWt-B5U90qb5KplCkSQ"
        }
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        task_id = 1
        task_gmg_artist_id = None
        task_youtube_music_channel_id = None
        task_youtube_music_playlist_id = None
        task_youtube_music_playlist_url = None
        task_youtube_music_plate_remark = None

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
        origin_songs_count = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][0]["text"]
        d["origin_songs_count"] = origin_songs_count
        # songs_count
        d["songs_count"] = origin_songs_count.replace(" songs", "").replace(" song", "").strip()
        # origin_duration
        origin_total_duration = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][2]["text"]
        d["origin_total_duration"] = origin_total_duration
        # duration
        parts = origin_total_duration.split(",")
        hours = 0
        minutes = 0
        seconds = 0

        for part in parts:
            if "hours" in part:
                hours = int(part.strip().split()[0])
            elif "minutes" in part:
                minutes = int(part.strip().split()[0])
            elif "seconds" in part:
                seconds = int(part.strip().split()[0])

        total_seconds = hours * 3600 + minutes * 60 + seconds
        d["total_duration"] = total_seconds
        d["url_canonical"] = None
        # description
        d["description"] = response.json["header"]["musicDetailHeaderRenderer"]["description"]["runs"][0]["text"]
        # image_url
        d["image_url"] = \
            response.json["header"]["musicDetailHeaderRenderer"]["thumbnail"]["croppedSquareThumbnailRenderer"][
                "thumbnail"]["thumbnails"][-1]["url"]

        songs_info_list = \
            response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]
        for per_song_info in songs_info_list:
            youtube_music_artist_plate_data_item = dict()
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
            youtube_music_artist_plate_data_item["image_url"] = d["image_url"]


            # songs_url
            youtube_music_artist_plate_data_item["youtube_music_video_image_url"] = \
                per_song_info["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"][0]["url"]
            # youtube_music_video_id
            youtube_music_artist_plate_data_item["youtube_music_video_id"] = per_song_info["musicResponsiveListItemRenderer"]["playlistItemData"][
                "videoId"]
            youtube_music_artist_plate_data_item["youtube_music_video_url"] = "https://music.youtube.com/watch?v="+youtube_music_artist_plate_data_item["youtube_music_video_id"]
            youtube_music_artist_plate_data_item["origin_youtube_music_video_url"] = None
            youtube_music_artist_plate_data_item["youtube_music_video_url_split_playlist_id"] = None
            youtube_music_artist_plate_data_item["youtube_music_video_url_split_playlist_url"] = None
            youtube_music_artist_plate_data_item["origin_youtube_music_video_play_count"] = None
            youtube_music_artist_plate_data_item["youtube_music_video_play_count"] = None

            # youtube_music_video_name
            youtube_music_artist_plate_data_item["youtube_music_video_name"] = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][0][
                "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
            # youtube_music_video_artist_name
            youtube_music_video_artist_name_list = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][1][
                "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"]
            if len(youtube_music_video_artist_name_list) == 1:
                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = youtube_music_video_artist_name_list[0]["text"]
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
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_name"] = other_info["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_id"] = \
                        other_info["text"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                    youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"] = "https://music.youtube.com/browse/" + str(
                        youtube_music_artist_plate_data_item["youtube_music_playlist_id"])
                    youtube_music_artist_plate_data_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"]
                else:
                    youtube_music_artist_plate_data_item["other_info"] = other_info["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_name"] = None
                    youtube_music_artist_plate_data_item["youtube_music_video_playlist_id"] = None
                    youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"] = None
                    youtube_music_artist_plate_data_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"]

            else:
                youtube_music_artist_plate_data_item["other_info"] = None
                youtube_music_artist_plate_data_item["youtube_music_video_playlist_name"] = None
                youtube_music_artist_plate_data_item["youtube_music_video_playlist_id"] = None
                youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"] = None
                youtube_music_artist_plate_data_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_artist_plate_data_item["origin_youtube_music_playlist_url"]

                # origin_duration
            origin_duration = per_song_info["musicResponsiveListItemRenderer"]["fixedColumns"][0][
                "musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
            youtube_music_artist_plate_data_item["origin_duration"] = origin_duration
            # duration
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
            youtube_music_artist_plate_data_item["duration"] = total_seconds
            # playlist_set_video_id
            youtube_music_artist_plate_data_item["youtube_music_playlist_set_video_id"] = \
                per_song_info["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
            youtube_music_artist_plate_data_item["is_playable"] = 1
            pprint(youtube_music_artist_plate_data_item)

if __name__ == "__main__":
    MyTestAirspider().start()