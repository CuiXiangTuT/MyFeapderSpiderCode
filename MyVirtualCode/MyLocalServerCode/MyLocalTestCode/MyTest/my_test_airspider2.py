# -*- coding: utf-8 -*-
"""
Created on 2023-10-12 15:39:10
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
import json
import re
import warnings
import httpx
from datetime import datetime,timedelta
from pprint import pprint


class MyTestAirspider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        task_id = 1
        task_gmg_artist_id = ""
        task_gmg_artist_name = ""
        # for channel_id in ["UCL2MDNdwEtV6aYUgNjFQGZA"]:
        task_youtube_music_channel_id = ""
        # 对task_youtube_music_plate_remark做个判定，可能需要做不同的处理
        task_youtube_music_plate_remark = "Albums/Singles"
        task_youtube_music_playlist_id = ""
        task_youtube_music_playlist_url = "https://music.youtube.com/playlist?list=RDCLAK5uy_lBiyOUBnKuu8qcfu6fDqp3cmW-5Z56dSk"
        yield feapder.Request(url=task_youtube_music_playlist_url,
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_gmg_artist_name=task_gmg_artist_name,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_plate_remark=task_youtube_music_plate_remark,
                              task_youtube_music_playlist_id=task_youtube_music_playlist_id,
                              task_youtube_music_playlist_url=task_youtube_music_playlist_url,
                              )


    def parse(self, request, response):
        pattern = r"initialData\.push\({([\s\S]*?)}\);"
        response.encoding = response.apparent_encoding
        matches = re.findall(pattern, response.text)
        if len(matches) >= 2:
            second_data = matches[1]
            match = re.search(r"data: '(.*)'", second_data)
            if match:
                data_value = match.group(1)
                data = bytes(data_value, 'UTF-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
                json_data = json.loads(data)
                item = dict()
                # 1-专辑名
                item["title"] = json_data["header"]["musicDetailHeaderRenderer"]["title"]["runs"][0]["text"]
                # 2-类型
                item["playlist_type"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][0]["text"]
                # 3-歌手名
                if "MUSIC_PAGE_TYPE_ARTIST" in str(json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"]):
                    title_artist_list = [p for p in json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"] if "MUSIC_PAGE_TYPE_ARTIST" in str(p)]
                    if len(title_artist_list)==1:
                        item["artist_name"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2]["text"]
                    elif len(title_artist_list)>1:
                        item["artist_name"] = ";".join([k["text"] for k in title_artist_list])

                    # 5-歌手channel id
                    if len(title_artist_list) == 1:
                        if "navigationEndpoint" in str(
                                json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2]):
                            item["artist_channel_id"] = \
                            json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2][
                                "navigationEndpoint"]["browseEndpoint"]["browseId"]
                        else:
                            item["artist_channel_id"] = None
                    elif len(title_artist_list) > 1:
                        title_artist_channel_list = [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in
                                                     title_artist_list if "browseId" in str(k)]
                        if len(title_artist_channel_list) == 1:
                            item["artist_channel_id"] = title_artist_channel_list[0]
                        elif len(title_artist_channel_list) > 1:
                            item["artist_channel_id"] = ";".join(title_artist_channel_list)

                else:
                    if len(json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"])>=3:
                        item["artist_name"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2]["text"]
                        item["artist_channel_id"] = None
                # 4-发行日期
                publish_date_str = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][-1]["text"]
                pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
                if bool(re.match(pattern, publish_date_str)):
                    item["publish_date"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][-1]["text"]
                else:
                    item["publish_date"] = None


                # 6-封面
                item["img_url"] = json_data["header"]["musicDetailHeaderRenderer"]["thumbnail"]["croppedSquareThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
                # 7-描述
                if "description" in str(json_data["header"]["musicDetailHeaderRenderer"]):
                    item["description"] = json_data["header"]["musicDetailHeaderRenderer"]["description"]["runs"][0]["text"]
                else:
                    item["description"] = None
                # 8-歌曲数量
                item["origin_songs_count"] = json_data["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][0]["text"]
                # 9-处理后的歌曲数量
                item["songs_count"] = item["origin_songs_count"].replace(" songs","").replace(" song","")
                # 10-时长
                item["origin_total_duration"] = json_data["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][2]["text"]
                # 11-处理后的时长
                total_seconds = 0
                # 将时间字符串转换为时间间隔对象
                time_delta = timedelta()
                time_parts = item["origin_total_duration"].split(',')
                for part in time_parts:
                    time_value, time_unit = part.strip().split()
                    if "hour" in time_unit:
                        time_delta += timedelta(hours=int(time_value))
                    elif "minute" in time_unit:
                        time_delta += timedelta(minutes=int(time_value))
                    elif "second" in time_unit:
                        time_delta += timedelta(seconds=int(time_value))

                # 将时间间隔对象转换为秒数并累加
                total_seconds += time_delta.total_seconds()
                item["total_duration"] = int(total_seconds)
                # 12-URL规范化
                item["url_canonical"] = json_data["microformat"]["microformatDataRenderer"]["urlCanonical"]
                # 获取包含的歌曲
                if "musicShelfRenderer" in str(json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]):
                    songs_list = json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["contents"]
                    for per_song_json in songs_list:
                        # 13-歌曲video id
                        if "playlistItemData" in str(per_song_json["musicResponsiveListItemRenderer"]):
                            item["youtube_music_video_id"] = per_song_json["musicResponsiveListItemRenderer"]["playlistItemData"]["videoId"]
                            # 14-暂不明确意思
                            item["youtube_music_playlist_set_video_id"] = per_song_json["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
                            flexColumns_list = per_song_json["musicResponsiveListItemRenderer"]["flexColumns"]
                            # 15-歌曲名
                            item["youtube_music_video_name"] = flexColumns_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            youtube_music_video_artist_name_list = flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]

                            if youtube_music_video_artist_name_list is None:
                                # 16-歌曲艺人名
                                item["youtube_music_video_artist_name"] = None
                                # 17-歌曲艺人channel id
                                item["youtube_music_video_artist_channel_id"] = None
                            elif "runs" in str(youtube_music_video_artist_name_list):
                                youtube_music_video_artist_name_inner_list = youtube_music_video_artist_name_list["runs"]
                                if len(youtube_music_video_artist_name_inner_list) == 1:
                                    # 16-歌曲艺人名
                                    item["youtube_music_video_artist_name"] = youtube_music_video_artist_name_list["runs"][0]["text"]
                                    # 17-歌曲艺人channel id
                                    if "browseEndpoint" in str(youtube_music_video_artist_name_list["runs"][0]):
                                        item["youtube_music_video_artist_channel_id"] = youtube_music_video_artist_name_list["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                                    else:
                                        item["youtube_music_video_artist_channel_id"] = None
                                elif len(youtube_music_video_artist_name_inner_list)>1:
                                    runs_list = flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"]
                                    artist_name_list = [runs_list[k]["text"] for k in range(len(runs_list)) if k%2==0]
                                    if len(artist_name_list)>1:
                                        # 16-歌曲艺人名
                                        item["youtube_music_video_artist_name"] = ";".join(artist_name_list)
                                    elif len(artist_name_list)==1:
                                        # 16-歌曲艺人名
                                        item["youtube_music_video_artist_name"] = artist_name_list[0]
                                    artist_channel_id_list = [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"] if "browseId" in str(k)]
                                    if len(artist_channel_id_list)>1:
                                        # 17-歌曲艺人channel id
                                        item["youtube_music_video_artist_channel_id"] = ";".join(artist_channel_id_list)
                                    elif len(artist_channel_id_list)==1:
                                        # 17-歌曲艺人channel id
                                        item["youtube_music_video_artist_name"] = artist_channel_id_list[0]


                            # 18-歌曲播放量
                            item["origin_youtube_music_video_play_count"] = flexColumns_list[2]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            flex_views = item[
                                "origin_youtube_music_video_play_count"].replace(" plays", "").replace(
                                " play", "")
                            item["youtube_music_video_play_count"] = int(float(flex_views.lower().replace("k", "")) * 1000) if "k" in flex_views.lower() else int(float(flex_views.lower().replace('m',"")) * 1000000) if "m" in flex_views.lower() else int(float(flex_views.lower().replace("b","")) * 1000000000) if "b" in flex_views.lower() else int(flex_views)
                            item["youtube_music_video_play_count"] = int(float(flex_views.lower().replace("k",""))*1000) if "k" in flex_views.lower() else int(float(flex_views.lower().replace('m',""))*1000000) if "m" in flex_views.lower() else int(flex_views)
                            # 19-歌曲播放时长
                            item["origin_duration"] = per_song_json["musicResponsiveListItemRenderer"]["fixedColumns"][0]["musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
                            duration_list = item["origin_duration"].split(":")

                            if len(duration_list) == 2:
                                minutes, seconts = duration_list
                                hours = 0
                                minutes = int(minutes)
                                seconts = int(seconts)
                            elif len(duration_list) == 3:
                                hours, minutes, seconts = duration_list
                                hours = int(hours)
                                minutes = int(minutes)
                                seconts = int(seconts)
                            else:
                                seconts = duration_list[0]
                                hours = 0
                                minutes = 0
                                seconts = int(seconts)
                            total_seconds = hours * 3600 + minutes * 60 + seconts
                            # 20-歌曲时长
                            item["duration"] = total_seconds
                            # 21-歌曲序号
                            item["serial_number"] = per_song_json["musicResponsiveListItemRenderer"]["index"]["runs"][0]["text"]
                            # 22-是否可播放
                            item["is_playable"] = 1

                        else:
                            # 13-歌曲video id
                            item["youtube_music_video_id"] = None
                            # 14-暂不明确意思
                            item["youtube_music_playlist_set_video_id"] = None
                            # 15-歌曲名
                            flexColumns_list = per_song_json["musicResponsiveListItemRenderer"]["flexColumns"]
                            item["youtube_music_video_name"] = flexColumns_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            # 16-歌曲艺人名
                            if "runs" in str(
                                    flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]) and "text" in str(
                                    flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][
                                        0]):
                                item["youtube_music_video_artist_name"] = \
                                    flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0][
                                        "text"]
                            else:
                                item["youtube_music_video_artist_name"] = None
                            # 17-歌曲艺人channel id
                            item["youtube_music_video_artist_channel_id"] = None
                            # 18-歌曲播放量
                            item["origin_youtube_music_video_play_count"] = None
                            item["youtube_music_video_play_count"] = 0
                            # 19-歌曲播放时长
                            item["origin_duration"] = None
                            # 20-歌曲播放时长
                            item["duration"] = 0
                            # 21-歌曲序号
                            item["serial_number"] = -1
                            # 22-是否可播放
                            item["is_playable"] = 0

                        pprint(item)
                        print("---------------------------------------------------")
                else:
                    pass

        else:
            print("无法找到第二个initialData.push的值")


if __name__ == "__main__":
    MyTestAirspider().start()
