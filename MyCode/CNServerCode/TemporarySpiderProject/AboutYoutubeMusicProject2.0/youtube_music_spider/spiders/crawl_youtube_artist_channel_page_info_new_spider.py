# -*- coding: utf-8 -*-
"""
Created on 2024-01-13 09:03:27
---------
@summary:
---------
@author: AirWolf
"""

import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *

class CrawlYoutubeArtistChannelPageInfoNewSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self,task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_gmg_artist_name = task.gmg_artist_name
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_channel_name = task.youtube_music_channel_name
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
            "browseId": task.youtube_music_channel_id
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

        youtube_music_infomation_is_exist_remark = False
        youtube_music_songs_plate_is_exist_remark = False
        youtube_music_album_plate_is_exist_remark = False
        youtube_music_singles_plate_is_exist_remark = False
        youtube_music_videos_plate_is_exist_remark = False
        youtube_music_featured_on_plate_is_exist_remark = False
        youtube_music_fans_might_also_like_plate_is_exist_remark = False
        youtube_music_latest_episodes_plate_is_exist_remark = False
        youtube_music_podcasts_plate_is_exist_remark = False

        if response.json.get("header"):
            youtube_music_channel_id_batch_data_new_item = YoutubeMusicChannelIdBatchDataNewItem()
            youtube_music_channel_id_batch_data_new_item["gmg_artist_id"] = task_gmg_artist_id
            youtube_music_channel_id_batch_data_new_item["gmg_artist_name"] = task_gmg_artist_name
            youtube_music_channel_id_batch_data_new_item["youtube_music_channel_id"] = task_youtube_music_channel_id
            youtube_music_channel_id_batch_data_new_item["youtube_music_channel_name"] = task_youtube_music_channel_name
            # youtube_music_artist_name
            youtube_music_channel_id_batch_data_new_item["youtube_music_artist_name"] = \
            response.json["header"]["musicImmersiveHeaderRenderer"]["title"]["runs"][0]["text"]
            # youtube_music_artist_channel_id
            youtube_music_channel_id_batch_data_new_item["youtube_music_subscribe_artist_channel_id"] = \
            response.json["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"][
                "channelId"]
            # origin_youtube_music_artist_subscriber_count
            origin_youtube_music_artist_subscriber_count = \
            response.json["header"]["musicImmersiveHeaderRenderer"]["subscriptionButton"]["subscribeButtonRenderer"][
                "subscriberCountWithSubscribeText"]["runs"][0]["text"]
            youtube_music_channel_id_batch_data_new_item["origin_youtube_music_artist_subscriber_count"] = origin_youtube_music_artist_subscriber_count
            # youtube_music_artist_subscriber_count
            youtube_music_channel_id_batch_data_new_item["youtube_music_artist_subscriber_count"] = int(float(
                origin_youtube_music_artist_subscriber_count.lower().replace("k",
                                                                             "")) * 1000) if "k" in origin_youtube_music_artist_subscriber_count.lower() else int(
                float(origin_youtube_music_artist_subscriber_count.lower().replace('m',
                                                                                   "")) * 1000000) if "m" in origin_youtube_music_artist_subscriber_count.lower() else int(
                float(origin_youtube_music_artist_subscriber_count.lower().replace("b",
                                                                                   "").strip()) * 1000000000) if "b" in origin_youtube_music_artist_subscriber_count.lower() else int(
                origin_youtube_music_artist_subscriber_count.strip())
            # youtube_music_artist_description
            if response.json["header"]["musicImmersiveHeaderRenderer"].get("description"):
                youtube_music_channel_id_batch_data_new_item["youtube_music_artist_description"] = \
            response.json["header"]["musicImmersiveHeaderRenderer"]["description"]["runs"][0]["text"]
                youtube_music_infomation_is_exist_remark = True
            else:
                youtube_music_channel_id_batch_data_new_item["youtube_music_artist_description"] = None

            # youtube_music_artist_background_image_url
            youtube_music_channel_id_batch_data_new_item["youtube_music_artist_background_image_url"] = \
            response.json["header"]["musicImmersiveHeaderRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"][
                "thumbnails"][-1]["url"]

            json_data_list = \
            response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]["contents"]

            for per_json_data in json_data_list:
                if per_json_data.get("musicShelfRenderer"):
                    if per_json_data["musicShelfRenderer"]["title"]["runs"][0]["text"] == "Songs":
                        if per_json_data["musicShelfRenderer"]["title"]["runs"][0].get("navigationEndpoint"):
                            # youtube_music_all_songs_id
                            youtube_music_all_songs_id = \
                            per_json_data["musicShelfRenderer"]["title"]["runs"][0]["navigationEndpoint"][
                                "browseEndpoint"]["browseId"][2:]
                            youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"] = youtube_music_all_songs_id
                            youtube_music_channel_id_batch_data_new_item[
                                "youtube_music_all_songs_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_all_songs_id
                            youtube_music_artist_plate_task_item = YoutubeMusicArtistPlateTaskItem()
                            youtube_music_artist_plate_task_item["gmg_artist_id"] = task_gmg_artist_id
                            youtube_music_artist_plate_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                            youtube_music_artist_plate_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"]
                            youtube_music_artist_plate_task_item["youtube_music_playlist_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_all_songs_id
                            youtube_music_artist_plate_task_item["youtube_music_plate_remark"] = "Songs"
                            yield youtube_music_artist_plate_task_item
                            youtube_music_songs_plate_is_exist_remark = True
                        else:
                            contents_list = \
                            per_json_data["musicShelfRenderer"]["contents"][0]["musicResponsiveListItemRenderer"][
                                "flexColumns"]
                            if len(contents_list):
                                if contents_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0].get(
                                        "navigationEndpoint"):
                                    playlist_id = \
                                    contents_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0][
                                        "navigationEndpoint"]["watchEndpoint"]["playlistId"]
                                    youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"] = playlist_id
                                    youtube_music_channel_id_batch_data_new_item[
                                        "youtube_music_all_songs_url"] = "https://music.youtube.com/playlist?list=" + playlist_id

                                    youtube_music_artist_plate_task_item = YoutubeMusicArtistPlateTaskItem()
                                    youtube_music_artist_plate_task_item["gmg_artist_id"] = task_gmg_artist_id
                                    youtube_music_artist_plate_task_item[
                                        "youtube_music_channel_id"] = task_youtube_music_channel_id
                                    youtube_music_artist_plate_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"]
                                    youtube_music_artist_plate_task_item["youtube_music_playlist_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"]
                                    youtube_music_artist_plate_task_item["youtube_music_plate_remark"] = "Songs"
                                    yield youtube_music_artist_plate_task_item

                                    youtube_music_songs_plate_is_exist_remark = True
                                else:
                                    youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"] = None
                                    youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_url"] = None
                            else:
                                youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"] = None
                                youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_url"] = None

                elif per_json_data.get("musicDescriptionShelfRenderer"):
                    if per_json_data["musicDescriptionShelfRenderer"]["header"]["runs"][0]["text"] == "About":
                        origin_views = per_json_data["musicDescriptionShelfRenderer"]["subheader"]["runs"][0]["text"]
                        # origin_views
                        youtube_music_channel_id_batch_data_new_item["origin_views"] = origin_views
                        # views
                        youtube_music_channel_id_batch_data_new_item["views"] = origin_views.replace("views", "").replace("view", "").replace(",",
                                                                                                            "").strip()
                        youtube_music_channel_id_batch_data_new_item["youtube_music_artist_about_description"] = \
                        per_json_data["musicDescriptionShelfRenderer"]["description"]["runs"][0]["text"]
                else:
                    if per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Albums":
                        if \
                        per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                            "title"]["runs"][0].get("navigationEndpoint"):
                            youtube_music_all_albums_singles_id = per_json_data["musicCarouselShelfRenderer"]["header"][
                                "musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"][
                                "browseEndpoint"]["browseId"]
                            youtube_music_channel_id_batch_data_new_item["youtube_music_all_albums_id"] = youtube_music_all_albums_singles_id
                            youtube_music_channel_id_batch_data_new_item[
                                "youtube_music_all_albums_url"] = "https://music.youtube.com/channel/" + youtube_music_all_albums_singles_id
                            # youtube_music_playlist_task_item = YoutubeMusicPlaylistTaskItem()
                            # youtube_music_playlist_task_item["gmg_artist_id"] = task_gmg_artist_id
                            # youtube_music_playlist_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                            # youtube_music_playlist_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_albums_id"]
                            # youtube_music_playlist_task_item["youtube_music_playlist_url"] =youtube_music_channel_id_batch_data_new_item[
                            #         "youtube_music_all_albums_url"]
                            # youtube_music_playlist_task_item["youtube_music_plate_remark"] = "Albums"
                            # yield youtube_music_playlist_task_item
                            youtube_music_album_plate_is_exist_remark = True

                            youtube_music_channel_id_other = youtube_music_all_albums_singles_id.replace("MPAD","")
                            if youtube_music_channel_id_other != task_youtube_music_channel_id:
                                youtube_music_artist_playlist_map_item = YoutubeMusicArtistPlaylistMapItem()
                                youtube_music_artist_playlist_map_item["gmg_artist_id"] = task_gmg_artist_id
                                youtube_music_artist_playlist_map_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                                youtube_music_artist_playlist_map_item["youtube_music_channel_id_other"] = youtube_music_channel_id_other
                                youtube_music_artist_playlist_map_item["youtube_music_playlist_id"] = "MPAD" + task_youtube_music_channel_id
                                youtube_music_artist_playlist_map_item["youtube_music_playlist_id_other"] = youtube_music_all_albums_singles_id
                                youtube_music_artist_playlist_map_item["youtube_music_playlist_url"] = "https://music.youtube.com/channel/MPAD" +  task_youtube_music_channel_id
                                youtube_music_artist_playlist_map_item["youtube_music_playlist_url_other"] = "https://music.youtube.com/channel/MPAD" + youtube_music_channel_id_other
                                youtube_music_artist_playlist_map_item["youtube_music_plate_remark"] = "Albums/Singles"
                                yield youtube_music_artist_playlist_map_item

                        # youtube_music_playlist_task_item = YoutubeMusicPlaylistTaskItem()
                        # youtube_music_playlist_task_item["gmg_artist_id"] = task_gmg_artist_id
                        # youtube_music_playlist_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                        # youtube_music_playlist_task_item["youtube_music_playlist_id"] = "MPAD"+task_youtube_music_channel_id
                        # youtube_music_playlist_task_item["youtube_music_playlist_url"] = "https://music.youtube.com/channel/MPAD"+task_youtube_music_channel_id
                        # youtube_music_playlist_task_item["youtube_music_plate_remark"] = "Albums"
                        # yield youtube_music_playlist_task_item



                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Singles":
                        if \
                        per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                            "title"]["runs"][0].get("navigationEndpoint"):
                            youtube_music_all_singles_id = per_json_data["musicCarouselShelfRenderer"]["header"][
                                "musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"][
                                "browseEndpoint"]["browseId"]
                            youtube_music_channel_id_batch_data_new_item["youtube_music_all_singles_id"] = youtube_music_all_singles_id
                            youtube_music_channel_id_batch_data_new_item[
                                "youtube_music_all_singles_url"] = "https://music.youtube.com/channel/" + youtube_music_all_singles_id
                            # youtube_music_playlist_task_item = YoutubeMusicPlaylistTaskItem()
                            # youtube_music_playlist_task_item["gmg_artist_id"] = task_gmg_artist_id
                            # youtube_music_playlist_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                            # youtube_music_playlist_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_singles_id"]
                            # youtube_music_playlist_task_item["youtube_music_playlist_url"] = youtube_music_channel_id_batch_data_new_item[
                            #         "youtube_music_all_singles_url"]
                            # youtube_music_playlist_task_item["youtube_music_plate_remark"] = "Singles"
                            # yield youtube_music_playlist_task_item

                            youtube_music_singles_plate_is_exist_remark = True

                            youtube_music_channel_id_other = youtube_music_all_singles_id.replace("MPAD", "")
                            if youtube_music_channel_id_other != youtube_music_all_singles_id:
                                youtube_music_artist_playlist_map_item = YoutubeMusicArtistPlaylistMapItem()
                                youtube_music_artist_playlist_map_item["gmg_artist_id"] = task_gmg_artist_id
                                youtube_music_artist_playlist_map_item[
                                    "youtube_music_channel_id"] = task_youtube_music_channel_id
                                youtube_music_artist_playlist_map_item[
                                    "youtube_music_channel_id_other"] = youtube_music_channel_id_other
                                youtube_music_artist_playlist_map_item[
                                    "youtube_music_playlist_id"] = "MPAD" + task_youtube_music_channel_id
                                youtube_music_artist_playlist_map_item[
                                    "youtube_music_playlist_id_other"] = youtube_music_all_singles_id
                                youtube_music_artist_playlist_map_item[
                                    "youtube_music_playlist_url"] = "https://music.youtube.com/channel/MPAD" + task_youtube_music_channel_id
                                youtube_music_artist_playlist_map_item[
                                    "youtube_music_playlist_url_other"] = "https://music.youtube.com/channel/MPAD" + youtube_music_channel_id_other
                                youtube_music_artist_playlist_map_item["youtube_music_plate_remark"] = "Albums/Singles"
                                yield youtube_music_artist_playlist_map_item

                        # youtube_music_playlist_task_item = YoutubeMusicPlaylistTaskItem()
                        # youtube_music_playlist_task_item["gmg_artist_id"] = task_gmg_artist_id
                        # youtube_music_playlist_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                        # youtube_music_playlist_task_item[
                        #     "youtube_music_playlist_id"] = "MPAD" + task_youtube_music_channel_id
                        # youtube_music_playlist_task_item[
                        #     "youtube_music_playlist_url"] = "https://music.youtube.com/channel/MPAD" + task_youtube_music_channel_id
                        # youtube_music_playlist_task_item["youtube_music_plate_remark"] = "Singles"
                        # yield youtube_music_playlist_task_item

                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Videos":
                        if \
                        per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                            "title"]["runs"][0].get("navigationEndpoint"):
                            youtube_music_all_videos_id = per_json_data["musicCarouselShelfRenderer"]["header"][
                                "musicCarouselShelfBasicHeaderRenderer"]["title"]["runs"][0]["navigationEndpoint"][
                                "browseEndpoint"]["browseId"][2:]
                            youtube_music_channel_id_batch_data_new_item["youtube_music_all_videos_id"] = youtube_music_all_videos_id

                            youtube_music_channel_id_batch_data_new_item[
                                "youtube_music_all_videos_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_all_videos_id

                            youtube_music_artist_plate_task_item = YoutubeMusicArtistPlateTaskItem()
                            youtube_music_artist_plate_task_item["gmg_artist_id"] = task_gmg_artist_id
                            youtube_music_artist_plate_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
                            youtube_music_artist_plate_task_item["youtube_music_playlist_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_videos_id"]
                            youtube_music_artist_plate_task_item["youtube_music_playlist_url"] = youtube_music_channel_id_batch_data_new_item[
                                "youtube_music_all_videos_url"]
                            youtube_music_artist_plate_task_item["youtube_music_plate_remark"] = "Videos"
                            yield youtube_music_artist_plate_task_item

                            youtube_music_videos_plate_is_exist_remark = True

                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Featured on":
                        inner_featured_on_json_data_list = per_json_data["musicCarouselShelfRenderer"]["contents"]
                        for per_inner_featured_on_json_data in inner_featured_on_json_data_list:
                            # youtube_music_artist_plate_task
                            youtube_music_artist_plate_task_item = YoutubeMusicArtistPlateTaskItem()
                            youtube_music_artist_plate_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_plate_task_item[
                                "youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_playlist_id = \
                            per_inner_featured_on_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0][
                                "navigationEndpoint"]["browseEndpoint"]["browseId"][2:]
                            youtube_music_artist_plate_task_item[
                                "youtube_music_playlist_id"] = youtube_music_playlist_id
                            youtube_music_artist_plate_task_item[
                                "youtube_music_playlist_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_playlist_id
                            youtube_music_artist_plate_task_item["youtube_music_plate_remark"] = "Featured on"

                            yield youtube_music_artist_plate_task_item

                            youtube_music_artist_page_featured_batch_data_item = YoutubeMusicArtistPageFeaturedBatchDataItem()
                            youtube_music_artist_page_featured_batch_data_item[
                                "gmg_artist_id"] = task_gmg_artist_id
                            youtube_music_artist_page_featured_batch_data_item[
                                "youtube_music_artist_channel_id"] = task_youtube_music_channel_id
                            youtube_music_artist_page_featured_batch_data_item[
                                "youtube_music_artist_channel_name"] = task_youtube_music_channel_name
                            youtube_music_artist_page_featured_batch_data_item["featured_title"] = \
                            per_inner_featured_on_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                            youtube_music_artist_page_featured_batch_data_item[
                                "featured_id"] = youtube_music_playlist_id
                            youtube_music_artist_page_featured_batch_data_item[
                                "featured_url"] = "https://music.youtube.com/playlist?list=" + youtube_music_playlist_id
                            youtube_music_artist_page_featured_batch_data_item["batch"] = self.batch_date
                            yield youtube_music_artist_page_featured_batch_data_item

                        youtube_music_featured_on_plate_is_exist_remark = True

                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Fans might also like":
                        inner_fans_might_also_like_json_data_list = per_json_data["musicCarouselShelfRenderer"][
                            "contents"]
                        for per_inner_fans_might_also_like_json_data in inner_fans_might_also_like_json_data_list:
                            youtube_music_artist_fans_also_like_batch_data_item = YoutubeMusicArtistFansAlsoLikeBatchDataItem()
                            youtube_music_artist_fans_also_like_batch_data_item[
                                "gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_artist_fans_also_like_batch_data_item[
                                "gmg_artist_name"] = request.task_gmg_artist_name
                            youtube_music_artist_fans_also_like_batch_data_item[
                                "youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_artist_fans_also_like_batch_data_item[
                                "youtube_music_channel_name"] = request.task_youtube_music_channel_name
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_name"] = \
                            per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0][
                                "text"]
                            if per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["title"]["runs"][
                                0].get("navigationEndpoint"):
                                fans_also_like_artist_channel_id = \
                                per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0][
                                    "navigationEndpoint"]["browseEndpoint"]["browseId"]
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_channel_id"] = fans_also_like_artist_channel_id
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_channel_url"] = "https://music.youtube.com/channel/" + fans_also_like_artist_channel_id
                            else:
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_channel_id"] = None
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_channel_url"] = None
                            youtube_music_artist_fans_also_like_batch_data_item["fans_also_like_artist_img_url"] = \
                            per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"][
                                "musicThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
                            if per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"].get("subtitle"):
                                origin_fans_also_like_artist_subscriber_count = \
                                per_inner_fans_might_also_like_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][
                                    0]["text"]
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "origin_fans_also_like_artist_subscriber_count"] = origin_fans_also_like_artist_subscriber_count
                                origin_fans_also_like_artist_subscriber_count_fixed = origin_fans_also_like_artist_subscriber_count.replace(
                                    " subscribers", "").replace(" subscriber", "").strip()
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_subscriber_count"] = int(float(
                                    origin_fans_also_like_artist_subscriber_count_fixed.lower().replace("k",
                                                                                                        "")) * 1000) if "k" in origin_fans_also_like_artist_subscriber_count_fixed.lower() else int(
                                    float(origin_fans_also_like_artist_subscriber_count_fixed.lower().replace('m',
                                                                                                              "")) * 1000000) if "m" in origin_fans_also_like_artist_subscriber_count_fixed.lower() else int(
                                    origin_fans_also_like_artist_subscriber_count_fixed.strip()) if "b" not in origin_fans_also_like_artist_subscriber_count_fixed.lower() else int(
                                    float(origin_fans_also_like_artist_subscriber_count_fixed.lower().replace("b",
                                                                                                              "").strip()) * 1000000000)
                            else:
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "origin_fans_also_like_artist_subscriber_count"] = None
                                youtube_music_artist_fans_also_like_batch_data_item[
                                    "fans_also_like_artist_subscriber_count"] = 0
                            # pprint(youtube_music_artist_fans_also_like_batch_data_item)
                            youtube_music_artist_fans_also_like_batch_data_item["batch"] = self.batch_date
                            yield youtube_music_artist_fans_also_like_batch_data_item
                        youtube_music_fans_might_also_like_plate_is_exist_remark = True
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Latest episodes":
                        youtube_music_latest_episodes_plate_is_exist_remark = True
                    elif per_json_data["musicCarouselShelfRenderer"]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["text"] == "Podcasts":
                        youtube_music_podcasts_plate_is_exist_remark = True

            # if "youtube_music_all_albums_id" in youtube_music_channel_id_batch_data_new_item:
            #     pass
            # else:
            #     youtube_music_channel_id_batch_data_new_item["youtube_music_all_albums_id"] = None
            #     youtube_music_channel_id_batch_data_new_item["youtube_music_all_albums_url"] = None
            # if "youtube_music_all_singles_id" in youtube_music_channel_id_batch_data_new_item:
            #     pass
            # else:
            #     youtube_music_channel_id_batch_data_new_item["youtube_music_all_singles_id"] = None
            #     youtube_music_channel_id_batch_data_new_item["youtube_music_all_singles_url"] = None

            youtube_music_channel_id_batch_data_new_item["batch"] = self.batch_date

            youtube_music_artist_page_plate_info_batch_data_item = YoutubeMusicArtistPagePlateInfoBatchDataItem()
            youtube_music_artist_page_plate_info_batch_data_item["gmg_artist_id"] = youtube_music_channel_id_batch_data_new_item["gmg_artist_id"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_channel_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_channel_id"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_id"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_songs_url"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_songs_url"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_albums_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_albums_id"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_albums_url"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_albums_url"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_singles_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_singles_id"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_singles_url"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_singles_url"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_videos_id"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_videos_id"]
            youtube_music_artist_page_plate_info_batch_data_item["youtube_music_all_videos_url"] = youtube_music_channel_id_batch_data_new_item["youtube_music_all_videos_url"]
            youtube_music_artist_page_plate_info_batch_data_item["batch"] = self.batch_date

            yield youtube_music_channel_id_batch_data_new_item
            yield youtube_music_artist_page_plate_info_batch_data_item

            youtube_music_channel_id_crawl_situation_batch_data_item = YoutubeMusicChannelIdCrawlSituationBatchDataItem()
            youtube_music_channel_id_crawl_situation_batch_data_item["gmg_artist_id"] = task_gmg_artist_id
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_channel_id"] = task_youtube_music_channel_id
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_channel_name"] = task_youtube_music_channel_name
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_artist_name"] = youtube_music_channel_id_batch_data_new_item["youtube_music_artist_name"]
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_infomation_is_exist_remark"] = "EI" if youtube_music_infomation_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_songs_plate_is_exist_remark"] = "EI" if youtube_music_songs_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_album_plate_is_exist_remark"] = "EI" if youtube_music_album_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_singles_plate_is_exist_remark"] = "EI" if youtube_music_singles_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_videos_plate_is_exist_remark"] = "EI" if youtube_music_videos_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_featured_on_plate_is_exist_remark"] = "EI" if youtube_music_featured_on_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_fans_might_also_like_plate_is_exist_remark"] = "EI" if youtube_music_fans_might_also_like_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_latest_episodes_plate_is_exist_remark"] = "EI" if youtube_music_latest_episodes_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["youtube_music_podcasts_plate_is_exist_remark"] = "EI" if youtube_music_podcasts_plate_is_exist_remark else "NI"
            youtube_music_channel_id_crawl_situation_batch_data_item["batch"] = self.batch_date

            yield youtube_music_channel_id_crawl_situation_batch_data_item


            # if youtube_music_album_plate_is_exist_remark or youtube_music_singles_plate_is_exist_remark:
            youtube_music_playlist_task_item = YoutubeMusicPlaylistTaskItem()
            youtube_music_playlist_task_item["gmg_artist_id"] = task_gmg_artist_id
            youtube_music_playlist_task_item["youtube_music_channel_id"] = task_youtube_music_channel_id
            youtube_music_playlist_task_item["youtube_music_playlist_id"] = "MPAD" + task_youtube_music_channel_id
            youtube_music_playlist_task_item[
                "youtube_music_playlist_url"] = "https://music.youtube.com/channel/MPAD" + task_youtube_music_channel_id
            youtube_music_playlist_task_item["youtube_music_plate_remark"] = "Singles/Albums"
            yield youtube_music_playlist_task_item

            yield self.update_task_batch(request.task_id, 1)

if __name__ == "__main__":
    spider = CrawlYoutubeArtistChannelPageInfoNewSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubeArtistChannelPageInfoNewSpider爬虫")

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
    # python crawl_youtube_artist_channel_page_info_new_spider.py --start_master  # 添加任务
    # python crawl_youtube_artist_channel_page_info_new_spider.py --start_worker  # 启动爬虫
