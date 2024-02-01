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
            "videoId": "rjdFlFyhroU",
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "US",
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20210101.00.00"
                }
            }
        }
        url = "https://music.youtube.com/youtubei/v1/next?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        yield feapder.Request(url=url, method="POST", json=data)

    def parse(self, request, response):
        json_data = response.json["contents"]["singleColumnMusicWatchNextResultsRenderer"]["tabbedRenderer"]["watchNextTabbedResultsRenderer"]["tabs"][0]

        if json_data['tabRenderer']["content"]['musicQueueRenderer'].get("content"):
            d = dict()
            # 1-title
            d["youtube_music_video_title"] = json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"]["contents"][0]["playlistPanelVideoRenderer"]["title"]["runs"][0]["text"]
            # 2-artist
            youtube_music_video_artist_name_list =  json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"]["contents"][0]["playlistPanelVideoRenderer"]["longBylineText"]["runs"]
            index = next((i for i, d in enumerate(youtube_music_video_artist_name_list) if d.get("text") == " • "), None)
            if index==1:
                d["youtube_music_video_artist_name"] = youtube_music_video_artist_name_list[0]["text"]
                d["youtube_music_video_artist_channel_id"] = youtube_music_video_artist_name_list[0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
            elif index>1:
                d["youtube_music_video_artist_name"]= ";".join([youtube_music_video_artist_name_list[i]["text"] for i in range(0,index) if i%2==0])
                d["youtube_music_video_artist_channel_id"] = ";".join([youtube_music_video_artist_name_list[i]["navigationEndpoint"]["browseEndpoint"]["browseId"] for i in range(0,index) if i%2==0])
            else:
                d["youtube_music_video_artist_name"] = None
                d["youtube_music_video_artist_channel_id"] = None
            if "view" in youtube_music_video_artist_name_list[index+1]["text"]:
                # 3-views
                origin_youtube_music_video_views = youtube_music_video_artist_name_list[index+1]["text"]
                d["origin_youtube_music_video_views"] = origin_youtube_music_video_views
                origin_youtube_music_video_views_split = origin_youtube_music_video_views.replace(" views","").replace(" view","")
                d["youtube_music_video_views"] = int(float(origin_youtube_music_video_views_split.lower().replace("k",""))*1000) if "k" in origin_youtube_music_video_views_split.lower() else int(float(origin_youtube_music_video_views_split.lower().replace('m',""))*1000000) if "m" in origin_youtube_music_video_views_split.lower() else int(origin_youtube_music_video_views_split.strip())
            else:
                d["origin_youtube_music_video_views"] = None
                d["youtube_music_video_views"] = 0
                # 4-likes
            # origin_youtube_music_video_likes = youtube_music_video_artist_name_list[index+3]["text"]
            # d["origin_youtube_music_video_likes"] = origin_youtube_music_video_likes
            # origin_youtube_music_video_likes_split = origin_youtube_music_video_likes.replace(" likes", "").replace(
            #     " like", "")
            # d["youtube_music_video_likes"] = int(float(origin_youtube_music_video_likes_split.lower().replace("k",
            #                                                                                                   "")) * 1000) if "k" in origin_youtube_music_video_likes_split.lower() else int(
            #     float(origin_youtube_music_video_likes_split.lower().replace('m',
            #                                                                  "")) * 1000000) if "m" in origin_youtube_music_video_likes_split.lower() else int(
            #     origin_youtube_music_video_likes_split.strip())
            # 5-image_url
            d["image_url"] = json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"]["contents"][0]["playlistPanelVideoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]

            if json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"]["contents"][0]["playlistPanelVideoRenderer"].get("lengthText"):
                # 6-duration
                origin_duration = json_data["tabRenderer"]["content"]["musicQueueRenderer"]["content"]["playlistPanelRenderer"]["contents"][0]["playlistPanelVideoRenderer"]["lengthText"]["runs"][0]["text"]
                d["origin_duration"] = origin_duration
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
                d["duration"] = total_seconds
            else:
                d["origin_duration"] = None
                d["duration"] = 0
            pprint(d)
        else:
            print("不存在信息")


if __name__ == "__main__":
    MyTestAirspider().start()