# -*- coding: utf-8 -*-
"""
Created on 2024-01-10 15:46:15
---------
@summary:
---------
@author: QiuQiuRen
"""

import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *


class CrawlYoutubePageSongsInfoNewSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def start_requests(self, task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_playlist_id = task.youtube_music_playlist_id
        task_youtube_music_playlist_url = task.youtube_music_playlist_url
        task_youtube_music_plate_remark = task.youtube_music_plate_remark
        url = "https://music.youtube.com/channel/{}".format(task_youtube_music_channel_id)
        headers = {
            "authority": "music.youtube.com",
            "method": "GET",
            "path": url.replace("https://music.youtube.com", ""),
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "max-age=0",
            "Cache-Control": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Cookie": "CONSENT=PENDING+405; VISITOR_INFO1_LIVE=IGZzaH1uGfQ; _ga=GA1.1.527396337.1699502544; _ga_2LYFVQK29H=GS1.1.1699525078.2.1.1699526072.0.0.0; VISITOR_PRIVACY_METADATA=CgJaQRIEGgAgIQ%3D%3D; _gcl_au=1.1.402953871.1702980312; PREF=tz=Asia.Shanghai&autoplay=true; YSC=2VkYWfoKilM",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Sec-Ch-Ua-Bitness": '"64"',
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "Sec-Ch-Ua-Arch": '"x86"',
            "Sec-Ch-Ua-Full-Version-List": '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.130", "Microsoft Edge";v="120.0.2210.91"',
            "Sec-Ch-Ua-Mobile": '?0',
            "Sec-Ch-Ua-Model": "",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
            "Sec-Ch-Ua-Wow64": '?0',
            "Sec-Fetch-Dest": 'document',
            "Sec-Fetch-Mode": 'navigate',
            "Sec-Fetch-Site": 'same-origin',
            "Sec-Fetch-User": '?1',
            "Service-Worker-Navigation-Preload": 'true',
            "Upgrade-Insecure-Requests": '1'
        }

        yield feapder.Request(url=url, headers=headers, task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_playlist_id=task_youtube_music_playlist_id,
                              task_youtube_music_playlist_url=task_youtube_music_playlist_url,
                              task_youtube_music_plate_remark=task_youtube_music_plate_remark,
                              )

    def parse(self, request, response):
        task_id = request.task_id
        task_gmg_artist_id = request.task_gmg_artist_id
        task_youtube_music_channel_id = request.task_youtube_music_channel_id
        task_youtube_music_playlist_id = request.task_youtube_music_playlist_id
        task_youtube_music_playlist_url = request.task_youtube_music_playlist_url
        task_youtube_music_plate_remark = request.task_youtube_music_plate_remark
        visitorData = response.re('"visitorData":"(.*?)",')[0]
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        data = {
            "context": {
                "client": {
                    "visitorData": visitorData,
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "platform": "DESKTOP",
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20240103.01.00"
                }
            },
            "browseId": "VLOL" + task_youtube_music_playlist_id
        }
        nextContinuationData = None
        yield feapder.Request(url=url, json=data, visitorData=visitorData, callback=self.parse1,
                              nextContinuationData=nextContinuationData,
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
                              task_youtube_music_channel_id=task_youtube_music_channel_id,
                              task_youtube_music_playlist_id=task_youtube_music_playlist_id,
                              task_youtube_music_playlist_url=task_youtube_music_playlist_url,
                              task_youtube_music_plate_remark=task_youtube_music_plate_remark,
                              )

    def parse1(self, request, response):
        if request.nextContinuationData == None:
            d = dict()
            # serial_number
            d["serial_number"] = 0
            d["description"] = None
            d["url_canonical"] = None
            if response.json.get("header"):
                # title
                d["title"] = response.json["header"]["musicDetailHeaderRenderer"]["title"]["runs"][0]["text"]
                if response.json["header"]["musicDetailHeaderRenderer"].get("subtitle"):
                    # playlist_type
                    d["playlist_type"] = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][0][
                        "text"]
                    # artist_name
                    inner_data = response.json["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"]
                    count = sum(1 for item in inner_data if isinstance(item, dict) and item.get("text") == " • ")
                    print(count)
                    if count == 1:

                        last_text = inner_data[-1]["text"]
                        if last_text.isdigit() and len(last_text) == 4:
                            d["publish_date"] = last_text
                            d["artist_name"] = None
                            d["artist_channel_id"] = None
                        else:
                            d["publish_date"] = None
                            d["artist_name"] = last_text
                            if inner_data[-1].get("navigationEndpoint"):
                                d["artist_channel_id"] = inner_data[-1]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            else:
                                d["artist_channel_id"] = None
                    elif count == 2:
                        info = list()
                        found_first_marker = False
                        for per_inner_data in inner_data:
                            if isinstance(per_inner_data, dict) and "text" in per_inner_data:
                                text = per_inner_data["text"]
                                if text == " • ":
                                    if found_first_marker:
                                        break
                                    found_first_marker = True
                                elif found_first_marker and text != "&":
                                    info.append(per_inner_data)

                        if len(info) == 1:
                            # artist_name
                            d["artist_name"] = info[0]["text"]
                            # artist_channel_id
                            if info[0].get("navigationEndpoint"):
                                d["artist_channel_id"] = info[0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
                            else:
                                d["artist_channel_id"] = None
                        elif len(info) > 1:
                            d["artist_name"] = ";".join([k["text"] for k in info if k["text"].strip()!="&"])
                            artist_channel_id = ";".join(
                                [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in info if
                                 k.get("navigationEndpoint")])
                            if artist_channel_id.startswith(";"):
                                d["artist_channel_id"] = artist_channel_id[1:]
                            if artist_channel_id.endswith(";"):
                                d["artist_channel_id"] = artist_channel_id[:-1]

                        # publish_date
                        if inner_data[-1].get("text") and inner_data[-1]["text"].isdigit() and len(
                                inner_data[-1]["text"]) == 4:
                            d["publish_date"] = inner_data[-1]["text"]
                        else:
                            d["publish_date"] = None

                else:
                    d["playlist_type"] = None
                    d["artist_name"] = None
                    d["artist_channel_id"] = None
                    d["publish_date"] = None

                if response.json["header"]["musicDetailHeaderRenderer"].get("thumbnail"):
                    # img_url
                    d["img_url"] = \
                        response.json["header"]["musicDetailHeaderRenderer"]["thumbnail"][
                            "croppedSquareThumbnailRenderer"][
                            "thumbnail"]["thumbnails"][-1]["url"]
                else:
                    d["img_url"] = None
                if response.json["header"]["musicDetailHeaderRenderer"].get("secondSubtitle"):
                    secondSubtitle_list = response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"]
                    if len(secondSubtitle_list) == 3:
                        # origin_songs_count
                        origin_songs_count = \
                            response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][0]["text"]

                        # songs_count
                        d["origin_songs_count"] = origin_songs_count
                        d["songs_count"] = origin_songs_count.replace(" songs", "").replace(" song", "").strip()
                        # origin_total_duration
                        origin_total_duration = \
                            response.json["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][-1]["text"]
                        d["origin_total_duration"] = origin_total_duration
                        parts = origin_total_duration.split(",")
                        hours = 0
                        minutes = 0
                        seconds = 0

                        for part in parts:
                            if "hours" in part or "+" in part:
                                hours = int(part.replace("+", "").strip().split()[0])
                            elif "minutes" in part:
                                minutes = int(part.replace("+", "").strip().split()[0])
                            elif "seconds" in part:
                                seconds = int(part.replace("+", "").strip().split()[0])

                        total_seconds = hours * 3600 + minutes * 60 + seconds
                        d["total_duration"] = total_seconds
                    else:
                        d["origin_songs_count"] = None
                        d["songs_count"] = 0
                        d["origin_total_duration"] = None
                        d["total_duration"] = 0
            else:
                d["title"] = None
                d["playlist_type"] = None
                d["artist_name"] = None
                d["artist_channel_id"] = None
                d["publish_date"] = None
                d["img_url"] = None
                d["origin_songs_count"] = None
                d["songs_count"] = 0
                d["origin_total_duration"] = None
                d["total_duration"] = 0

            json_data_list = \
                response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                    "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]
            for per_json_data in json_data_list:
                youtube_music_artist_plate_data_new_item = YoutubeMusicArtistPlateDataNewItem()
                youtube_music_artist_plate_data_new_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                youtube_music_artist_plate_data_new_item["serial_number"] = d["serial_number"]
                youtube_music_artist_plate_data_new_item["description"] = d["description"]
                youtube_music_artist_plate_data_new_item["url_canonical"] = d["url_canonical"]
                youtube_music_artist_plate_data_new_item["title"] = d["title"]
                youtube_music_artist_plate_data_new_item["playlist_type"] = d["playlist_type"]
                youtube_music_artist_plate_data_new_item["artist_name"] = d["artist_name"]
                youtube_music_artist_plate_data_new_item["artist_channel_id"] = d["artist_channel_id"]
                youtube_music_artist_plate_data_new_item["publish_date"] = d["publish_date"]
                youtube_music_artist_plate_data_new_item["img_url"] = d["img_url"]
                youtube_music_artist_plate_data_new_item["origin_songs_count"] = d["origin_songs_count"]
                youtube_music_artist_plate_data_new_item["songs_count"] = d["songs_count"]
                youtube_music_artist_plate_data_new_item["origin_total_duration"] = d["origin_total_duration"]
                youtube_music_artist_plate_data_new_item["total_duration"] = d["total_duration"]

                # youtube_music_video_img_url
                youtube_music_artist_plate_data_new_item["youtube_music_video_img_url"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"][
                        "thumbnail"][
                        "thumbnails"][-1]["url"]
                # youtube_music_video_id
                youtube_music_video_id = per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"]["videoId"]
                youtube_music_artist_plate_data_new_item["youtube_music_video_id"] = youtube_music_video_id
                # youtube_music_video_url
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url"] = "https://music.youtube.com/watch?v=" + youtube_music_video_id
                # origin_youtube_music_video_url
                youtube_music_artist_plate_data_new_item["origin_youtube_music_video_url"] = None
                # youtube_music_video_url_split_playlist_id
                youtube_music_video_url_split_playlist_id = \
                    per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"][
                        "watchEndpoint"]["playlistId"]
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url_split_playlist_id"] = youtube_music_video_url_split_playlist_id
                # origin_youtube_music_video_url_split_playlist_url
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url_split_playlist_url"] = "https://music.youtube.com/browse/" + youtube_music_video_url_split_playlist_id
                # youtube_music_video_name
                youtube_music_artist_plate_data_new_item["youtube_music_video_name"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                # youtube_music_video_artist_name
                # youtube_music_video_artist_channel_id
                inner_text = per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][1]
                if inner_text["musicResponsiveListItemFlexColumnRenderer"]["text"].get("runs"):
                    youtube_music_video_artist_name_list = \
                        per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"]
                    if len(youtube_music_video_artist_name_list) == 1:
                        youtube_music_artist_plate_data_new_item["youtube_music_video_artist_name"] = \
                            youtube_music_video_artist_name_list[0]["text"]
                        if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0].get(
                                "navigationEndpoint"):
                            youtube_music_artist_plate_data_new_item["youtube_music_video_artist_channel_id"] = \
                                youtube_music_video_artist_name_list[0]["navigationEndpoint"]["browseEndpoint"][
                                    "browseId"]
                        else:
                            youtube_music_artist_plate_data_new_item["youtube_music_video_artist_channel_id"] = None
                    elif len(youtube_music_video_artist_name_list) > 1:
                        youtube_music_artist_plate_data_new_item["youtube_music_video_artist_name"] = ";".join(
                            [k["text"] for k in youtube_music_video_artist_name_list if k["text"].strip() not in ["&",","]])
                        youtube_music_video_artist_channel_id = ";".join(
                            [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in
                             youtube_music_video_artist_name_list if k.get("navigationEndpoint")])
                        if youtube_music_video_artist_channel_id.startswith(";"):
                            youtube_music_video_artist_channel_id = youtube_music_video_artist_channel_id[1:]
                        if youtube_music_video_artist_channel_id.endswith(";"):
                            youtube_music_video_artist_channel_id = youtube_music_video_artist_channel_id[:-1]
                        youtube_music_artist_plate_data_new_item[
                            "youtube_music_video_artist_channel_id"] = youtube_music_video_artist_channel_id
                else:
                    youtube_music_artist_plate_data_new_item["youtube_music_video_artist_name"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_video_artist_channel_id"] = None

                # origin_youtube_music_video_play_count
                if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][2][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"].get("runs"):
                    origin_youtube_music_video_play_count = \
                        per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][2][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_new_item[
                        "origin_youtube_music_video_play_count"] = origin_youtube_music_video_play_count
                    flex_play_count = origin_youtube_music_video_play_count.replace(" plays", "").replace(
                        " play", "")
                    youtube_music_artist_plate_data_new_item["youtube_music_video_play_count"] = int(float(
                        flex_play_count.lower().replace("k", "")) * 1000) if "k" in flex_play_count.lower() else int(
                        float(flex_play_count.lower().replace('m',
                                                              "")) * 1000000) if "m" in flex_play_count.lower() else int(
                        float(flex_play_count.lower().replace("b",
                                                              "").strip()) * 1000000000) if "b" in flex_play_count.lower() else int(
                        flex_play_count.strip())
                else:
                    youtube_music_artist_plate_data_new_item["origin_youtube_music_video_play_count"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_video_play_count"] = 0

                # youtube_music_playlist_set_video_id
                youtube_music_artist_plate_data_new_item["youtube_music_playlist_set_video_id"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
                # youtube_music_video_playlist_name
                if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"].get("runs"):
                    youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_name"] = \
                        per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                    if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0].get("navigationEndpoint"):
                        youtube_music_video_playlist_id = \
                            per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                                "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"][
                                "browseEndpoint"]["browseId"]
                        youtube_music_artist_plate_data_new_item[
                            "youtube_music_video_playlist_id"] = youtube_music_video_playlist_id
                        youtube_music_artist_plate_data_new_item[
                            "origin_youtube_music_playlist_url"] = "https://music.youtube.com/browse/" +youtube_music_video_playlist_id
                        youtube_music_artist_plate_data_new_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_artist_plate_data_new_item[
                                "origin_youtube_music_playlist_url"]
                    else:
                        youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_id"] = None
                        youtube_music_artist_plate_data_new_item["origin_youtube_music_playlist_url"] = None
                        youtube_music_artist_plate_data_new_item["youtube_music_playlist_url_pre_redirect"] = None
                else:
                    youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_name"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_id"] = None
                    youtube_music_artist_plate_data_new_item["origin_youtube_music_playlist_url"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_playlist_url_pre_redirect"] = None
                if per_json_data["musicResponsiveListItemRenderer"].get("fixedColumns"):
                    if per_json_data["musicResponsiveListItemRenderer"]["fixedColumns"][0].get(
                            "musicResponsiveListItemFixedColumnRenderer"):
                        origin_duration = per_json_data["musicResponsiveListItemRenderer"]["fixedColumns"][0][
                            "musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
                        youtube_music_artist_plate_data_new_item["origin_duration"] = origin_duration
                        duration_list = origin_duration.split(":")

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
                        youtube_music_artist_plate_data_new_item["duration"] = total_seconds
                else:
                    youtube_music_artist_plate_data_new_item["origin_duration"] = None
                    youtube_music_artist_plate_data_new_item["duration"] = 0
                youtube_music_artist_plate_data_new_item["is_playable"] = 1
                youtube_music_artist_plate_data_new_item["other_info"] = None
                youtube_music_artist_plate_data_new_item["batch"] = self.batch_date
                yield youtube_music_artist_plate_data_new_item

                youtube_music_video_task_item = YoutubeMusicVideoTaskItem()
                youtube_music_video_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_video_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_video_task_item["youtube_music_video_id"] = youtube_music_artist_plate_data_new_item["youtube_music_video_id"]
                youtube_music_video_task_item["youtube_music_video_url"] = youtube_music_artist_plate_data_new_item["youtube_music_video_url"]
                youtube_music_video_task_item["youtube_music_source_remark"] = youtube_music_artist_plate_data_new_item["youtube_music_plate_remark"]
                youtube_music_video_task_item["youtube_music_source_playlist_url"] = youtube_music_artist_plate_data_new_item["youtube_music_playlist_url"]
                yield youtube_music_video_task_item

            if response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"].get("continuations"):
                nextContinuationData = \
                    response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                        "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"]["continuations"][0][
                        "nextContinuationData"]["continuation"]
                url = "https://music.youtube.com/youtubei/v1/browse?continuation={}&type=next&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false".format(
                    nextContinuationData)
                data = {
                    "context": {
                        "client": {
                            "visitorData": request.visitorData,
                            "clientName": "WEB_REMIX",
                            "clientVersion": "1.20240103.01.00",
                            "osName": "Windows",
                            "osVersion": "10.0"
                        }
                    }
                }
                yield feapder.Request(url=url, json=data, visitorData=request.visitorData, callback=self.parse1,
                                      nextContinuationData=nextContinuationData,
                                      task_id=request.task_id,
                                      task_gmg_artist_id=request.task_gmg_artist_id,
                                      task_youtube_music_channel_id=request.task_youtube_music_channel_id,
                                      task_youtube_music_playlist_id=request.task_youtube_music_playlist_id,
                                      task_youtube_music_playlist_url=request.task_youtube_music_playlist_url,
                                      task_youtube_music_plate_remark=request.task_youtube_music_plate_remark,
                                      d=d,
                                      )
            else:
                yield self.update_task_state(request.task_id, 1)
                # print("数据采集完毕-1")
        else:
            json_data_list = response.json["continuationContents"]["musicPlaylistShelfContinuation"]["contents"]
            for per_json_data in json_data_list:
                youtube_music_artist_plate_data_new_item = YoutubeMusicArtistPlateDataNewItem()
                youtube_music_artist_plate_data_new_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                youtube_music_artist_plate_data_new_item["serial_number"] = request.d["serial_number"]
                youtube_music_artist_plate_data_new_item["description"] = request.d["description"]
                youtube_music_artist_plate_data_new_item["url_canonical"] = request.d["url_canonical"]
                youtube_music_artist_plate_data_new_item["title"] = request.d["title"]
                youtube_music_artist_plate_data_new_item["playlist_type"] = request.d["playlist_type"]
                youtube_music_artist_plate_data_new_item["artist_name"] = request.d["artist_name"]
                youtube_music_artist_plate_data_new_item["artist_channel_id"] = request.d["artist_channel_id"]
                youtube_music_artist_plate_data_new_item["publish_date"] = request.d["publish_date"]
                youtube_music_artist_plate_data_new_item["img_url"] = request.d["img_url"]
                youtube_music_artist_plate_data_new_item["origin_songs_count"] = request.d["origin_songs_count"]
                youtube_music_artist_plate_data_new_item["songs_count"] = request.d["songs_count"]
                youtube_music_artist_plate_data_new_item["origin_total_duration"] = request.d["origin_total_duration"]
                youtube_music_artist_plate_data_new_item["total_duration"] = request.d["total_duration"]
                # youtube_music_video_img_url
                youtube_music_artist_plate_data_new_item["youtube_music_video_img_url"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"][
                        "thumbnail"][
                        "thumbnails"][-1]["url"]
                # youtube_music_video_id
                youtube_music_video_id = per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"]["videoId"]
                youtube_music_artist_plate_data_new_item["youtube_music_video_id"] = youtube_music_video_id
                # youtube_music_video_url
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url"] = "https://music.youtube.com/watch?v=" + youtube_music_video_id
                # origin_youtube_music_video_url
                youtube_music_artist_plate_data_new_item["origin_youtube_music_video_url"] = None
                # youtube_music_video_url_split_playlist_id
                youtube_music_video_url_split_playlist_id = \
                    per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"][
                        "watchEndpoint"]["playlistId"]
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url_split_playlist_id"] = youtube_music_video_url_split_playlist_id
                # youtube_music_video_url_split_playlist_url
                youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url_split_playlist_url"] = "https://music.youtube.com/browse/" + youtube_music_video_url_split_playlist_id
                # youtube_music_video_name
                youtube_music_artist_plate_data_new_item["youtube_music_video_name"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                # youtube_music_video_artist_name
                # youtube_music_video_artist_channel_id
                inner_text = per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][1]
                if inner_text["musicResponsiveListItemFlexColumnRenderer"]["text"].get("runs"):
                    youtube_music_video_artist_name_list = \
                        per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"]
                    if len(youtube_music_video_artist_name_list) == 1:
                        youtube_music_artist_plate_data_new_item["youtube_music_video_artist_name"] = \
                            youtube_music_video_artist_name_list[0]["text"]
                        if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0].get(
                                "navigationEndpoint"):
                            youtube_music_artist_plate_data_new_item["youtube_music_video_artist_channel_id"] = \
                                youtube_music_video_artist_name_list[0]["navigationEndpoint"]["browseEndpoint"][
                                    "browseId"]
                        else:
                            youtube_music_artist_plate_data_new_item["youtube_music_video_artist_channel_id"] = None
                    elif len(youtube_music_video_artist_name_list) > 1:
                        youtube_music_artist_plate_data_new_item["youtube_music_video_artist_name"] = ";".join(
                            [k["text"] for k in youtube_music_video_artist_name_list if k["text"].strip() not in ["&",","]])
                        youtube_music_video_artist_channel_id = ";".join(
                            [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in
                             youtube_music_video_artist_name_list if k.get("navigationEndpoint")])
                        if youtube_music_video_artist_channel_id.startswith(";"):
                            youtube_music_video_artist_channel_id = youtube_music_video_artist_channel_id[1:]
                        if youtube_music_video_artist_channel_id.endswith(";"):
                            youtube_music_video_artist_channel_id = youtube_music_video_artist_channel_id[:-1]
                        youtube_music_artist_plate_data_new_item[
                            "youtube_music_video_artist_channel_id"] = youtube_music_video_artist_channel_id
                else:
                    youtube_music_artist_plate_data_new_item["youtube_music_video_artist_name"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_video_artist_channel_id"] = None

                # origin_youtube_music_video_play_count
                if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][2][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"].get("runs"):
                    origin_youtube_music_video_play_count = \
                        per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][2][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                    youtube_music_artist_plate_data_new_item[
                        "origin_youtube_music_video_play_count"] = origin_youtube_music_video_play_count
                    flex_play_count = youtube_music_artist_plate_data_new_item[
                        "origin_youtube_music_video_play_count"].replace(" plays", "").replace(
                        " play", "")
                    youtube_music_artist_plate_data_new_item["youtube_music_video_play_count"] = int(float(
                        flex_play_count.lower().replace("k", "")) * 1000) if "k" in flex_play_count.lower() else int(
                        float(flex_play_count.lower().replace('m',
                                                              "")) * 1000000) if "m" in flex_play_count.lower() else int(
                        float(flex_play_count.lower().replace("b",
                                                              "").strip()) * 1000000000) if "b" in flex_play_count.lower() else int(
                        flex_play_count.strip())
                else:
                    youtube_music_artist_plate_data_new_item["origin_youtube_music_video_play_count"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_video_play_count"] = 0

                # youtube_music_playlist_set_video_id
                youtube_music_artist_plate_data_new_item["youtube_music_playlist_set_video_id"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
                # youtube_music_video_playlist_name
                if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"].get("runs"):
                    youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_name"] = \
                        per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                    if per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0].get("navigationEndpoint"):
                        youtube_music_video_playlist_id = \
                            per_json_data["musicResponsiveListItemRenderer"]["flexColumns"][3][
                                "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["navigationEndpoint"][
                                "browseEndpoint"]["browseId"]
                        youtube_music_artist_plate_data_new_item[
                            "youtube_music_video_playlist_id"] = youtube_music_video_playlist_id
                        youtube_music_artist_plate_data_new_item[
                            "origin_youtube_music_playlist_url"] = "https://music.youtube.com/browse/" + youtube_music_video_playlist_id
                        youtube_music_artist_plate_data_new_item["youtube_music_playlist_url_pre_redirect"] = \
                            youtube_music_artist_plate_data_new_item[
                                "origin_youtube_music_playlist_url"]
                    else:
                        youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_id"] = None
                        youtube_music_artist_plate_data_new_item["origin_youtube_music_playlist_url"] = None
                        youtube_music_artist_plate_data_new_item["youtube_music_playlist_url_pre_redirect"] = None
                else:
                    youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_name"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_video_playlist_id"] = None
                    youtube_music_artist_plate_data_new_item["origin_youtube_music_playlist_url"] = None
                    youtube_music_artist_plate_data_new_item["youtube_music_playlist_url_pre_redirect"] = None
                if per_json_data["musicResponsiveListItemRenderer"].get("fixedColumns"):
                    if per_json_data["musicResponsiveListItemRenderer"]["fixedColumns"][0].get(
                            "musicResponsiveListItemFixedColumnRenderer"):
                        origin_duration = per_json_data["musicResponsiveListItemRenderer"]["fixedColumns"][0][
                            "musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
                        youtube_music_artist_plate_data_new_item["origin_duration"] = origin_duration
                        duration_list = origin_duration.split(":")

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
                        youtube_music_artist_plate_data_new_item["duration"] = total_seconds
                else:
                    youtube_music_artist_plate_data_new_item["origin_duration"] = None
                    youtube_music_artist_plate_data_new_item["duration"] = 0
                youtube_music_artist_plate_data_new_item["is_playable"] = 1
                youtube_music_artist_plate_data_new_item["other_info"] = None
                youtube_music_artist_plate_data_new_item["batch"] = self.batch_date
                yield youtube_music_artist_plate_data_new_item

                youtube_music_video_task_item = YoutubeMusicVideoTaskItem()
                youtube_music_video_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_video_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_video_task_item["youtube_music_video_id"] = youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_id"]
                youtube_music_video_task_item["youtube_music_video_url"] = youtube_music_artist_plate_data_new_item[
                    "youtube_music_video_url"]
                youtube_music_video_task_item["youtube_music_source_remark"] = youtube_music_artist_plate_data_new_item[
                    "youtube_music_plate_remark"]
                youtube_music_video_task_item["youtube_music_source_playlist_url"] = \
                youtube_music_artist_plate_data_new_item["youtube_music_playlist_url"]
                yield youtube_music_video_task_item

            if response.json["continuationContents"]["musicPlaylistShelfContinuation"].get("continuations"):
                nextContinuationData = \
                    response.json["continuationContents"]["musicPlaylistShelfContinuation"]["continuations"][0][
                        "nextContinuationData"]["continuation"]
                url = "https://music.youtube.com/youtubei/v1/browse?continuation={}&type=next&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false".format(
                    nextContinuationData)
                data = {
                    "context": {
                        "client": {
                            "visitorData": request.visitorData,
                            "clientName": "WEB_REMIX",
                            "clientVersion": "1.20240103.01.00",
                            "osName": "Windows",
                            "osVersion": "10.0"
                        }
                    }
                }
                yield feapder.Request(url=url, json=data, visitorData=request.visitorData, callback=self.parse1,
                                      nextContinuationData=nextContinuationData,
                                      task_id=request.task_id,
                                      task_gmg_artist_id=request.task_gmg_artist_id,
                                      task_youtube_music_channel_id=request.task_youtube_music_channel_id,
                                      task_youtube_music_playlist_id=request.task_youtube_music_playlist_id,
                                      task_youtube_music_playlist_url=request.task_youtube_music_playlist_url,
                                      task_youtube_music_plate_remark=request.task_youtube_music_plate_remark,
                                      d=request.d
                                      )
            else:
                yield self.update_task_state(request.task_id, 1)



if __name__ == "__main__":
    spider = CrawlYoutubePageSongsInfoNewSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubePageSogsInfoNewSpider爬虫")

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
    # python crawl_youtube_page_songs_info_new_spider.py --start_master  # 添加任务
    # python crawl_youtube_page_songs_info_new_spider.py --start_worker  # 启动爬虫
