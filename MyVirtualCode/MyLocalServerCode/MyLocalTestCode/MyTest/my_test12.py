import feapder
from feapder import ArgumentParser
from feapder.db.redisdb import RedisDB
from queue import Queue
from feapder.utils.log import log
import os
import isodate
from pprint import pprint
from datetime import datetime, timedelta
from copy import deepcopy
import re
import requests


class MyTestAirspider(feapder.AirSpider):
    def init_task(self):
        pass

    def start_requests(self):
        task_id = 1
        task_gmg_artist_id = ""
        task_youtube_music_channel_id = "UCL2MDNdwEtV6aYUgNjFQGZA"
        task_youtube_music_playlist_id = "OLAK5uy_nSClHz9BcVUUkErpaaHUTjb4cM866SZ9U"
        task_youtube_music_playlist_url = ""
        task_youtube_music_plate_remark = ""
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
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20240103.01.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "browserName": "Chrome",
                    "browserVersion": "114.0.0.0"
                }
            },
            "browseId": "VL"+request.task_youtube_music_playlist_id
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
                        print("------->", last_text.isdigit())
                        if last_text.isdigit() and len(last_text) == 4:
                            d["publish_date"] = last_text
                            d["artist_name"] = None
                            d["artist_channel_id"] = None
                        else:
                            d["publish_date"] = None
                            d["artist_name"] = last_text
                            if inner_data[-1].get("navigationEndpoint"):
                                d["artist_channel_id"] = inner_data[-1]["navigationEndpoint"]["browseEndpoint"][
                                    "browseId"]
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
                            d["artist_name"] = ";".join([k["text"] for k in info if k["text"].strip() != "&"])
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

            json_data = \
                response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                    "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]
            for per_json_data in json_data:
                youtube_music_artist_plate_data_new_item = dict()
                # youtube_music_video_img_url
                youtube_music_artist_plate_data_new_item["youtube_music_video_img_url"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"][
                        "thumbnail"][
                        "thumbnails"][-1]["url"]
                # youtube_music_video_id
                youtube_music_video_id = per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"][
                    "videoId"]
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
                            [k["text"] for k in youtube_music_video_artist_name_list if
                             k["text"].strip() not in ["&", ","]])
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
                youtube_music_artist_plate_data_new_item["origin_youtube_music_video_play_count"] = None
                youtube_music_artist_plate_data_new_item["youtube_music_video_play_count"] = 0
                # youtube_music_playlist_set_video_id
                youtube_music_artist_plate_data_new_item["youtube_music_playlist_set_video_id"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
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
                pprint(youtube_music_artist_plate_data_new_item)
            if \
            response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]["contents"][0]["musicPlaylistShelfRenderer"].get("continuations"):
                nextContinuationData = \
                    response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"][
                        "content"][
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
                # yield self.update_task_state(request.task_id, 1)
                print("数据采集完毕-1")
        else:
            json_data_list = response.json["continuationContents"]["musicPlaylistShelfContinuation"]["contents"]
            for per_json_data in json_data_list:
                youtube_music_artist_plate_data_new_item = dict()
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
                            [k["text"] for k in youtube_music_video_artist_name_list if
                             k["text"].strip() not in ["&", ","]])
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
                youtube_music_artist_plate_data_new_item["origin_youtube_music_video_play_count"] = None
                youtube_music_artist_plate_data_new_item["youtube_music_video_play_count"] = 0
                # youtube_music_playlist_set_video_id
                youtube_music_artist_plate_data_new_item["youtube_music_playlist_set_video_id"] = \
                    per_json_data["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
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
                pprint(youtube_music_artist_plate_data_new_item)
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
                        "osVersion": "10.0",
                        "browserName": "Chrome",
                        "browserVersion": "114.0.0.0"
                    }
                },
                "browseId": "VL"+request.task_youtube_music_playlist_id
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


if __name__ == "__main__":
    MyTestAirspider().start()
