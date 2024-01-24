import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os
import isodate
from pprint import pprint
from datetime import datetime


class MyTestAirspider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        for i in ["WIHUcBY9lUw","8073Q0tQPDc"]:
            data = {
                "videoId": i,
                "context": {
                    "client": {
                        "hl": "en",
                        "gl": "US",
                        "clientName": "WEB_REMIX",
                        "clientVersion": "1.20210101.00.00"
                    }
                }
            }
            url = "https://music.youtube.com/youtubei/v1/player?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
            yield feapder.Request(url=url, method="POST", json=data)

    def parse(self, request, response):
        json_data = response.json
        youtube_music_video_views_data_item = dict()
        # youtube_music_video_views_data_item["gmg_artist_id"] = request.task_gmg_artist_id
        # youtube_music_video_views_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
        # youtube_music_video_views_data_item["youtube_music_video_id"] = request.task_youtube_music_video_id
        # youtube_music_video_views_data_item["youtube_music_video_url"] = request.task_youtube_music_video_url
        # youtube_music_video_views_data_item["youtube_music_source_remark"] = request.task_youtube_music_source_remark
        # youtube_music_video_views_data_item[
        #     "youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
        # 歌曲是否可看
        youtube_music_video_views_data_item["origin_is_playable"] = json_data["playabilityStatus"]["status"]
        if youtube_music_video_views_data_item["origin_is_playable"] in ["OK",'UNPLAYABLE']:
            # 1-youtube_video_id
            youtube_music_video_views_data_item["is_playable"] = 1
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
            tags_list = json_data["microformat"]["microformatDataRenderer"]["tags"]
            if len(tags_list) >= 1:
                youtube_music_video_views_data_item["youtube_music_video_tags"] = ','.join(tags_list) if len(
                    tags_list) > 1 else tags_list[0]
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
                    youtube_music_video_views_data_item["youtube_video_available_countries"] = None
            else:
                youtube_music_video_views_data_item["youtube_video_available_countries"] = None
            # youtube_music_video_views_data_item["batch"] = self.batch_date
            # yield youtube_music_video_views_data_item
            pprint(youtube_music_video_views_data_item)

            youtube_music_video_views_situation_batch_record_item = dict()
            # youtube_music_video_views_situation_batch_record_item["gmg_artist_id"] = request.gmg_artist_id
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_channel_id"] = request.youtube_music_channel_id
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_video_id"] = request.youtube_music_video_id
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_source_remark"] = request.youtube_music_source_remark
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_source_playlist_url"] = request.youtube_music_source_playlist_url
            youtube_music_video_views_situation_batch_record_item["youtube_music_video_views_infomation_remark"] = "EI"
            youtube_music_video_views_situation_batch_record_item["exception_info"] = None
            # youtube_music_video_views_situation_batch_record_item["batch"] = self.batch_date
            # yield youtube_music_video_views_situation_batch_record_item
            pprint(youtube_music_video_views_situation_batch_record_item)
        else:

            youtube_music_video_views_situation_batch_record_item = dict()
            youtube_music_video_views_situation_batch_record_item["origin_is_playable"] = youtube_music_video_views_data_item["origin_is_playable"]
            youtube_music_video_views_situation_batch_record_item["is_playable"] = 0
            # youtube_music_video_views_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_channel_id"] = request.task_youtube_music_channel_id
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_video_id"] = request.task_youtube_music_video_id
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_source_remark"] = request.task_youtube_music_source_remark
            # youtube_music_video_views_situation_batch_record_item[
            #     "youtube_music_source_playlist_url"] = request.task_youtube_music_source_playlist_url
            youtube_music_video_views_situation_batch_record_item["youtube_music_video_views_infomation_remark"] = "NI"
            youtube_music_video_views_situation_batch_record_item["exception_info"] = json_data["playabilityStatus"][
                "reason"]
            # youtube_music_video_views_situation_batch_record_item["batch"] = self.batch_date
            # yield youtube_music_video_views_situation_batch_record_item
            pprint(youtube_music_video_views_situation_batch_record_item)

if __name__ == "__main__":
    MyTestAirspider().start()