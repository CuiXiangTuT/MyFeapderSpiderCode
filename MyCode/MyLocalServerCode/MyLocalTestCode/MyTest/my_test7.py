import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os
import isodate
from pprint import pprint
from datetime import datetime
from copy import deepcopy

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
            "browseId": "VLRDCLAK5uy_mijutvVbzp7bbNlWt-B5U90qb5KplCkSQ"
        }
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        yield feapder.Request(url=url, json=data)

    def parse(self, request, response):
        d = dict()
        # title
        d["title"] = response.json["header"]["musicDetailHeaderRenderer"]["title"]["runs"][0]["text"]
        # playlist_type
        d["playlist_type"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][0]["text"]
        # playlist_owner
        d["playlist_owner"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2]["text"]
        # publish_date
        d["playlist_publish_date"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][4]["text"]
        # origin_songs_count
        origin_songs_count = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][0]["text"]
        d["origin_songs_count"] = origin_songs_count
        # songs_count
        d["songs_count"] = origin_songs_count.replace(" songs","").replace(" song","").strip()
        # origin_duration
        d["origin_duration"] = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][2]["text"]
        # duration
        parts = d["origin_duration"].split(",")
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
        d["duration"] = total_seconds
        # description
        d["description"] = response.json["header"]["musicDetailHeaderRenderer"]["description"]["runs"][0]["text"]
        # image_url
        d["image_url"] = response.json["header"]["musicDetailHeaderRenderer"]["thumbnail"]["croppedSquareThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]

        # pprint(d)
        songs_info_list = response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]
        for per_song_info in songs_info_list:
            song_dict = deepcopy(d)
            # songs_url
            song_dict["songs_image_url"] = per_song_info["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][0]["url"]
            # song_id
            song_dict["youtube_music_video_id"] = per_song_info["musicResponsiveListItemRenderer"]["playlistItemData"]["videoId"]
            # song_name
            song_dict["youtube_music_video_name"] = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
            # youtube_music_video_artist_name
            youtube_music_video_artist_name_list = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"]
            if len(youtube_music_video_artist_name_list)==1:
                song_dict["youtube_music_video_artist_name"] = youtube_music_video_artist_name_list[0]["text"]
                if youtube_music_video_artist_name_list[0].get("navigationEndpoint"):
                    song_dict["youtube_music_video_artist_id"] = youtube_music_video_artist_name_list[0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                else:
                    song_dict["youtube_music_video_artist_id"] = None
            elif len(youtube_music_video_artist_name_list)>1:
                artist_names = ";".join([k["text"] for k in youtube_music_video_artist_name_list if k["text"]!=" & "])
                song_dict["youtube_music_video_artist_name"] = artist_names

                artist_channel_ids = ";".join([k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in youtube_music_video_artist_name_list if k.get("navigationEndpoint")])
                song_dict["youtube_music_video_artist_id"] = artist_channel_ids
            else:
                song_dict["youtube_music_video_artist_name"] = None
            # addition_infomation
            other_info = per_song_info["musicResponsiveListItemRenderer"]["flexColumns"][2]["musicResponsiveListItemFlexColumnRenderer"]
            if other_info["text"].get("runs"):
                if other_info["text"]["runs"][0].get("navigationEndpoint"):
                    song_dict["other_info"] = other_info["text"]["runs"][0]["text"]
                    song_dict["youtube_music_playlist_name"] = other_info["text"]["runs"][0]["text"]
                    song_dict["youtube_music_playlist_id"] = other_info["text"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                    song_dict["youtube_music_playlist_url"] = "https://music.youtube.com/browse/"+str(song_dict["youtube_music_playlist_id"])
                else:
                    song_dict["other_info"] = other_info["text"]["runs"][0]["text"]
                    song_dict["youtube_music_playlist_name"] = None
                    song_dict["youtube_music_playlist_id"] = None
                    song_dict["youtube_music_playlist_url"] = None
            else:
                song_dict["other_info"] = None
                song_dict["youtube_music_playlist_name"] = None
                song_dict["youtube_music_playlist_id"] = None
                song_dict["youtube_music_playlist_url"] = None
            # origin_duration
            origin_duration = per_song_info["musicResponsiveListItemRenderer"]["fixedColumns"][0]["musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
            song_dict["origin_duration"] = origin_duration
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
            song_dict["duration"] = total_seconds
            # playlist_set_video_id
            song_dict["youtube_music_playlist_set_video_id"] = per_song_info["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
            pprint(song_dict)
            print("--------------------------------------------------------------------------------------")


if __name__ == "__main__":
    MyTestAirspider().start()