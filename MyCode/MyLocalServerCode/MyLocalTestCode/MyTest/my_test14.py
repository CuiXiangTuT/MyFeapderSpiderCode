# -*- coding: utf-8 -*-

"""
@Time    : 2024/1/6 17:24
@Author  : HuTao
@File    : my_spider_1
@Description :
"""

import feapder
import re
import json
from pprint import pprint
from datetime import datetime


class MySpider(feapder.AirSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        task_id = 1
        task_gmg_artist_id = "test_001"
        task_gmg_artist_name = "Jay Chou"
        task_youtube_music_channel_id = "UCYANtjjdDo8hUEcLHsp4MnA"
        task_youtube_music_channel_name = "Jay Chou"
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        data = {
            "context": {
                "client": {
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20240103.01.00",
                    "osName": "Windows",
                    "osVersion": "10.0"
                }
            },
            "browseId": "UCYANtjjdDo8hUEcLHsp4MnA"
        }
        yield feapder.Request(url=url, json=data, task_id=task_id, task_gmg_artist_id=task_gmg_artist_id,
                              task_gmg_artist_name=task_gmg_artist_name,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_channel_name=task_youtube_music_channel_name,
                              )

    def parse(self, request, response):
        task_gmg_artist_id = request.task_gmg_artist_id
        task_gmg_artist_name = request.task_gmg_artist_name
        task_youtube_music_channel_id = request.task_youtube_music_channel_id
        task_youtube_music_channel_name = request.task_youtube_music_channel_name
        if response.json.get("header"):
            d = dict()
            # youtube_music_artist_name
            d["youtube_music_artist_name"] = response.json["header"]["musicImmersiveHeaderRenderer"]["title"]["runs"][0]["text"]
            # youtube_music_artist_channel_id
            d["youtube_music_artist_channel_id"] = response.json["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"]["channelId"]
            # origin_youtube_music_artist_subscriber_count
            origin_youtube_music_artist_subscriber_count = response.json["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"]["subscriberCountWithSubscribeText"]["runs"][0]["text"]
            d["origin_youtube_music_artist_subscriber_count"] = origin_youtube_music_artist_subscriber_count
            # youtube_music_artist_subscriber_count
            d["youtube_music_artist_subscriber_count"] = int(float(
                        origin_youtube_music_artist_subscriber_count.lower().replace("k", "")) * 1000) if "k" in origin_youtube_music_artist_subscriber_count.lower() else int(
                        float(origin_youtube_music_artist_subscriber_count.lower().replace('m',
                                                              "")) * 1000000) if "m" in origin_youtube_music_artist_subscriber_count.lower() else int(
                        float(origin_youtube_music_artist_subscriber_count.lower().replace("b",
                                                              "").strip()) * 1000000000) if "b" in origin_youtube_music_artist_subscriber_count.lower() else int(
                        origin_youtube_music_artist_subscriber_count.strip())
            # youtube_music_artist_description
            d["youtube_music_artist_description"] = response.json["header"]["musicImmersiveHeaderRenderer"]["description"]["runs"][0]["text"]
            # youtube_music_artist_background_image_url
            d["youtube_music_artist_background_image_url"] = response.json["header"]["musicImmersiveHeaderRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]

            json_data_list = response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
            inner_item = dict()
            for per_json_data in json_data_list:
                if per_json_data.get("musicShelfRenderer"):
                    if per_json_data["musicShelfRenderer"]["title"]["runs"][0]["text"] == "Songs":
                        if per_json_data["musicShelfRenderer"]["title"]["runs"][0].get("navigationEndpoint"):
                            # youtube_music_all_songs_id
                            youtube_music_all_songs_id = per_json_data["musicShelfRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            inner_item["youtube_music_all_songs_id"] = youtube_music_all_songs_id
                            inner_item["youtube_music_all_songs_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_all_songs_id[2:]
                        else:
                            contents_list = per_json_data["musicShelfRenderer"]["contents"][0]["musicResponsiveListItemRenderer"]["flexColumns"]
                            if len(contents_list):
                                if contents_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0].get("navigationEndpoint"):
                                    playlist_id = contents_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"]["watchEndpoint"]["playlistId"]
                                    inner_item["youtube_music_all_songs_id"] = playlist_id
                                    inner_item["youtube_music_all_songs_url"] = "https://music.youtube.com/playlist?list=" + playlist_id
                                else:
                                    inner_item["youtube_music_all_songs_id"] = None
                                    inner_item["youtube_music_all_songs_url"] = None
                            else:
                                inner_item["youtube_music_all_songs_id"] = None
                                inner_item["youtube_music_all_songs_url"] = None

                elif per_json_data.get("musicDescriptionShelfRenderer"):
                    if per_json_data["musicDescriptionShelfRenderer"]["header"]["runs"][0]["text"]== "About":
                        origin_views = per_json_data["musicDescriptionShelfRenderer"]["subheader"]["runs"][0]["text"]
                        inner_item["origin_views"] = origin_views
                        inner_item["views"] = origin_views.replace("views","").replace("view","").replace(",","").strip()
                        inner_item["youtube_music_artist_about_description"] =per_json_data["musicDescriptionShelfRenderer"]["description"]["runs"][0]["text"]
                else:
                    if per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Albums":
                        if per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0].get("navigationEndpoint"):
                            youtube_music_all_albums_singles_id= per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            inner_item["youtube_music_all_albums_singles_id"] = youtube_music_all_albums_singles_id
                            inner_item["youtube_music_all_albums_singles_url"] = "https://music.youtube.com/channel/" + youtube_music_all_albums_singles_id
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Singles":
                        if per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0].get("navigationEndpoint"):
                            youtube_music_all_singles_id = per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            inner_item["youtube_music_all_albums_singles_id"] = youtube_music_all_singles_id
                            inner_item["youtube_music_all_albums_singles_url"] = "https://music.youtube.com/channel/" + youtube_music_all_singles_id
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Videos":
                        if per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0].get("navigationEndpoint"):
                            youtube_music_all_videos_id = per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            inner_item["youtube_music_all_videos_id"] = youtube_music_all_videos_id
                            inner_item["youtube_music_all_videos_url"] = "https://music.youtube.com/playlist?list="+youtube_music_all_videos_id[2:]
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Featured on":
                        inner_featured_on_json_data_list = per_json_data["musicCarouselShelfRenderer"]["contents"]
                        for per_inner_featured_on_json_data in inner_featured_on_json_data_list:
                            # youtube_music_artist_plate_task
                            youtube_music_artist_plate_task_item = dict()
                            youtube_music_artist_plate_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_plate_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_playlist_id = per_inner_featured_on_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            youtube_music_artist_plate_task_item["youtube_music_playlist_id"] = youtube_music_playlist_id
                            youtube_music_artist_plate_task_item["youtube_music_playlist_url"] = "https://music.youtube.com/playlist?list="+youtube_music_playlist_id[2:]
                            youtube_music_artist_plate_task_item["youtube_music_plate_remark"] = "Featured on"

                            youtube_music_artist_page_featured_batch_data_item = dict()
                            youtube_music_artist_page_featured_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_page_featured_batch_data_item["youtube_music_artist_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_artist_page_featured_batch_data_item["youtube_music_artist_channel_name"] = request.task_youtube_music_channel_name
                            youtube_music_artist_page_featured_batch_data_item["featured_title"] = per_inner_featured_on_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                            youtube_music_artist_page_featured_batch_data_item["featured_id"] = youtube_music_playlist_id
                            youtube_music_artist_page_featured_batch_data_item["featured_url"] = "https://music.youtube.com/playlist?list="+youtube_music_playlist_id[2:]
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Fans might also like":
                        inner_fans_might_also_like_json_data_list = per_json_data["musicCarouselShelfRenderer"]["contents"]
                        for per_inner_fans_might_also_like_json_data in inner_fans_might_also_like_json_data_list:
                            youtube_music_artist_fans_also_like_batch_data_item = dict()
                            youtube_music_artist_fans_also_like_batch_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_fans_also_like_batch_data_item["gmg_artist_name"] = request.task_gmg_artist_name
                            youtube_music_artist_fans_also_like_batch_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_artist_fans_also_like_batch_data_item["youtube_music_channel_name"] = request.task_youtube_music_channel_name
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_name"] = per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                            if per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0].get("navigationEndpoint"):
                                fans_also_like_artist_channel_id = per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                                youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_channel_id"] = fans_also_like_artist_channel_id
                                youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_channel_url"] = "https://music.youtube.com/channel/" + fans_also_like_artist_channel_id
                            else:
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_channel_id"] = None
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_channel_url"] = None
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_img_url"] = per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
                            if per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"].get("subtitle"):
                                origin_fans_also_like_artist_subscriber_count = per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
                                youtube_music_artist_fans_also_like_batch_data_item["origin_fans_also_like_artist_subscriber_count"] = origin_fans_also_like_artist_subscriber_count
                                origin_fans_also_like_artist_subscriber_count_fixed = origin_fans_also_like_artist_subscriber_count.replace(" subscribers","").replace(" subscriber","").strip()
                                youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_subscriber_count"] = int(float(origin_fans_also_like_artist_subscriber_count_fixed.lower().replace("k",""))*1000) if "k" in origin_fans_also_like_artist_subscriber_count_fixed.lower() else int(float(origin_fans_also_like_artist_subscriber_count_fixed.lower().replace('m',""))*1000000) if "m" in origin_fans_also_like_artist_subscriber_count_fixed.lower() else int(origin_fans_also_like_artist_subscriber_count_fixed.strip()) if "b" not in origin_fans_also_like_artist_subscriber_count_fixed.lower() else int(float(origin_fans_also_like_artist_subscriber_count_fixed.lower().replace("b","").strip()) * 1000000000)
                            else:
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "origin_fans_also_like_artist_subscriber_count"] = None
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_subscriber_count"] = 0
                            # pprint(youtube_music_artist_fans_also_like_batch_data_item)
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Latest episodes":
                        pass
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["text"] == "Podcasts":
                        pass

            pprint(inner_item)




if __name__ == "__main__":
    MySpider().start()
