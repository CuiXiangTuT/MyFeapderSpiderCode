# -*- coding: utf-8 -*-
"""
Created on 2023-12-21 15:06:53
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用于获取各个Playlist下的信息
"""

import feapder
from feapder import ArgumentParser
import json
import re
from datetime import datetime,timedelta
from pprint import pprint
from items.youtube_music_info_item import *
from copy import deepcopy

class CrawlYoutubePagePlaylistInfoSpider(feapder.BatchSpider):
    def init_task(self):
        pass

    def download_midware(self, request):
        request.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self,task):
        task_id = task.id
        task_gmg_artist_id = task.gmg_artist_id
        task_youtube_music_channel_id = task.youtube_music_channel_id
        task_youtube_music_playlist_id = task.youtube_music_playlist_id
        task_youtube_music_playlist_url = task.youtube_music_playlist_url
        task_youtube_music_plate_remark = task.youtube_music_plate_remark
        yield feapder.Request(url=task_youtube_music_playlist_url,
                              task_id=task_id,
                              task_gmg_artist_id=task_gmg_artist_id,
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
                item["gmg_artist_id"] = request.task_gmg_artist_id
                item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                # youtube_music_artist_plate_data_item["youtube_music_plate_remark"] =
                # 1-专辑名
                item["title"] = json_data["header"]["musicDetailHeaderRenderer"]["title"]["runs"][0]["text"]
                # 2-类型
                item["playlist_type"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][0]["text"]

                # 3-歌手名
                if "MUSIC_PAGE_TYPE_ARTIST" in str(
                        json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"]):
                    title_artist_list = [p for p in json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"]
                                         if "MUSIC_PAGE_TYPE_ARTIST" in str(p)]
                    if len(title_artist_list) == 1:
                        item["artist_name"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2][
                            "text"]
                    elif len(title_artist_list) > 1:
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
                    if len(json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"]) >= 3:
                        item["artist_name"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][2][
                            "text"]
                        item["artist_channel_id"] = None

                # 4-发行日期
                publish_date_str = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][-1]["text"]
                pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
                if bool(re.match(pattern, publish_date_str)):
                    item["publish_date"] = json_data["header"]["musicDetailHeaderRenderer"]["subtitle"]["runs"][-1][
                        "text"]
                else:
                    item["publish_date"] = None
                # 6-封面
                item["img_url"] = \
                json_data["header"]["musicDetailHeaderRenderer"]["thumbnail"]["croppedSquareThumbnailRenderer"][
                    "thumbnail"]["thumbnails"][-1]["url"]
                # 7-描述
                if "description" in str(json_data["header"]["musicDetailHeaderRenderer"]):
                    item["description"] = json_data["header"]["musicDetailHeaderRenderer"]["description"]["runs"][0][
                        "text"]
                else:
                    item["description"] = None
                # 8-歌曲数量
                item["origin_songs_count"] = \
                json_data["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][0]["text"]
                # 9-处理后的歌曲数量
                item["songs_count"] = item["origin_songs_count"].replace(" songs", "").replace(" song", "")
                # 10-时长
                item["origin_total_duration"] = \
                json_data["header"]["musicDetailHeaderRenderer"]["secondSubtitle"]["runs"][2]["text"]
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
                if "musicShelfRenderer" in str(
                        json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                            "sectionListRenderer"]["contents"][0]):
                    songs_list = \
                    json_data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                        "sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["contents"]
                    for per_song_json in songs_list:
                        youtube_music_artist_plate_data_item = YoutubeMusicArtistPlateDataItem()
                        youtube_music_artist_plate_data_item["gmg_artist_id"] = item["gmg_artist_id"]
                        youtube_music_artist_plate_data_item["youtube_music_channel_id"] = item["youtube_music_channel_id"]
                        youtube_music_artist_plate_data_item["youtube_music_playlist_id"] = item["youtube_music_playlist_id"]
                        youtube_music_artist_plate_data_item["youtube_music_playlist_url"] = item["youtube_music_playlist_url"]
                        youtube_music_artist_plate_data_item["title"] = item["title"]
                        youtube_music_artist_plate_data_item["playlist_type"] = item["playlist_type"]
                        youtube_music_artist_plate_data_item["artist_name"] = item["artist_name"]
                        youtube_music_artist_plate_data_item["publish_date"] = item["publish_date"]
                        youtube_music_artist_plate_data_item["artist_channel_id"] = item["artist_channel_id"]
                        youtube_music_artist_plate_data_item["img_url"] = item["img_url"]
                        youtube_music_artist_plate_data_item["origin_songs_count"] = item["origin_songs_count"]
                        youtube_music_artist_plate_data_item["songs_count"] = item["songs_count"]
                        youtube_music_artist_plate_data_item["description"] = item["description"]
                        youtube_music_artist_plate_data_item["origin_total_duration"] = item["origin_total_duration"]
                        youtube_music_artist_plate_data_item["total_duration"] = item["total_duration"]
                        youtube_music_artist_plate_data_item["url_canonical"] = item["url_canonical"]
                        youtube_music_artist_plate_data_item["origin_youtube_music_video_url"] = None
                        youtube_music_artist_plate_data_item["youtube_music_video_url_split_playlist_id"] = None
                        youtube_music_artist_plate_data_item["youtube_music_video_url_split_playlist_url"] = None

                        # 13-歌曲video id
                        if "playlistItemData" in str(per_song_json["musicResponsiveListItemRenderer"]):
                            youtube_music_artist_plate_data_item["youtube_music_video_id"] = \
                            per_song_json["musicResponsiveListItemRenderer"]["playlistItemData"]["videoId"]
                            youtube_music_artist_plate_data_item["youtube_music_video_url"] = "https://music.youtube.com/watch?v="+str(youtube_music_artist_plate_data_item["youtube_music_video_id"])
                            youtube_music_video_task_item = YoutubeMusicVideoTaskItem()
                            youtube_music_video_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                            youtube_music_video_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                            youtube_music_video_task_item["youtube_music_video_id"] = youtube_music_artist_plate_data_item["youtube_music_video_id"]
                            youtube_music_video_task_item["youtube_music_video_url"] ="https://music.youtube.com/watch?v=" + youtube_music_artist_plate_data_item["youtube_music_video_id"]
                            youtube_music_video_task_item["youtube_music_source_remark"] = youtube_music_artist_plate_data_item["playlist_type"]
                            youtube_music_video_task_item["youtube_music_source_playlist_url"] = request.task_youtube_music_playlist_url
                            # 14-暂不明确意思
                            youtube_music_artist_plate_data_item["youtube_music_playlist_set_video_id"] = \
                            per_song_json["musicResponsiveListItemRenderer"]["playlistItemData"]["playlistSetVideoId"]
                            flexColumns_list = per_song_json["musicResponsiveListItemRenderer"]["flexColumns"]
                            # 15-歌曲名
                            youtube_music_artist_plate_data_item["youtube_music_video_name"] = \
                            flexColumns_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            youtube_music_video_artist_name_list = \
                            flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]
                            if youtube_music_video_artist_name_list is None:
                                # 16-歌曲艺人名
                                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = None
                                # 17-歌曲艺人channel id
                                youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = None
                            elif "runs" in str(youtube_music_video_artist_name_list):
                                youtube_music_video_artist_name_inner_list = youtube_music_video_artist_name_list[
                                    "runs"]
                                if len(youtube_music_video_artist_name_inner_list)==1:
                                    # 16-歌曲艺人名
                                    youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = \
                                    youtube_music_video_artist_name_list["runs"][0]["text"]
                                    # 17-歌曲艺人channel id
                                    if "browseEndpoint" in str(youtube_music_video_artist_name_list["runs"][0]):
                                        youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = \
                                        youtube_music_video_artist_name_list["runs"][0]["navigationEndpoint"][
                                            "browseEndpoint"]["browseId"]
                                    else:
                                        youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = None
                                elif len(youtube_music_video_artist_name_inner_list) > 1:
                                    runs_list = flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"][
                                        "runs"]
                                    artist_name_list = [runs_list[k]["text"] for k in range(len(runs_list)) if k % 2 == 0]
                                    if len(artist_name_list) > 1:
                                        # 16-歌曲艺人名
                                        youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = ";".join(artist_name_list)
                                    elif len(artist_name_list) == 1:
                                        # 16-歌曲艺人id
                                        youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = artist_name_list[0]
                                    artist_channel_id_list = [k["navigationEndpoint"]["browseEndpoint"]["browseId"] for k in
                                                              flexColumns_list[1][
                                                                  "musicResponsiveListItemFlexColumnRenderer"]["text"][
                                                                  "runs"] if "browseId" in str(k)]
                                    if len(artist_channel_id_list) > 1:
                                        # 17-歌曲艺人channel id
                                        youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = ";".join(artist_channel_id_list)
                                    elif len(artist_channel_id_list) == 1:
                                        # 17-歌曲艺人channel id
                                        youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = artist_channel_id_list[0]
                            # 18-歌曲播放量
                            youtube_music_artist_plate_data_item["origin_youtube_music_video_play_count"] = \
                            flexColumns_list[2]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            flex_views = youtube_music_artist_plate_data_item["origin_youtube_music_video_play_count"].replace(" plays", "").replace(
                                " play", "")
                            youtube_music_artist_plate_data_item["youtube_music_video_play_count"] = int(float(flex_views.lower().replace("k", "")) * 1000) if "k" in flex_views.lower() else int(float(flex_views.lower().replace('m',"")) * 1000000) if "m" in flex_views.lower() else int(float(flex_views.lower().replace("b","")) * 1000000000) if "b" in flex_views.lower() else int(flex_views)
                            # 19-歌曲播放时长
                            youtube_music_artist_plate_data_item["origin_duration"] = \
                            per_song_json["musicResponsiveListItemRenderer"]["fixedColumns"][0][
                                "musicResponsiveListItemFixedColumnRenderer"]["text"]["runs"][0]["text"]
                            duration_list = youtube_music_artist_plate_data_item["origin_duration"].split(":")

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
                            youtube_music_artist_plate_data_item["duration"] = total_seconds
                            # 21-歌曲序号
                            youtube_music_artist_plate_data_item["serial_number"] = \
                            per_song_json["musicResponsiveListItemRenderer"]["index"]["runs"][0]["text"]
                            # 22-是否可播放
                            youtube_music_artist_plate_data_item["is_playable"] = 1
                            # 23-来自哪个模块
                            youtube_music_artist_plate_data_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                            youtube_music_artist_plate_data_item["batch"] = self.batch_date
                            youtube_music_artist_plate_data_item["youtube_music_video_image_url"] = None
                            youtube_music_artist_plate_data_item["other_info"] = None
                            yield youtube_music_artist_plate_data_item
                            yield youtube_music_video_task_item
                        else:
                            # 13-歌曲video id
                            youtube_music_artist_plate_data_item["youtube_music_video_id"] = None
                            # 14-暂不明确意思
                            youtube_music_artist_plate_data_item["youtube_music_playlist_set_video_id"] = None
                            # 15-歌曲名
                            flexColumns_list = per_song_json["musicResponsiveListItemRenderer"]["flexColumns"]
                            youtube_music_artist_plate_data_item["youtube_music_video_name"] = \
                            flexColumns_list[0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            # 16-歌曲艺人名
                            if "runs" in str(
                                    flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"][
                                        "text"]) and "text" in str(
                                flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][
                                    0]):
                                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = \
                            flexColumns_list[1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                            else:
                                youtube_music_artist_plate_data_item["youtube_music_video_artist_name"] = None
                            # 17-歌曲艺人channel id
                            youtube_music_artist_plate_data_item["youtube_music_video_artist_channel_id"] = None
                            # 18-歌曲播放量
                            youtube_music_artist_plate_data_item["origin_youtube_music_video_play_count"] = None
                            youtube_music_artist_plate_data_item["youtube_music_video_play_count"] = 0
                            # 19-歌曲播放时长
                            youtube_music_artist_plate_data_item["origin_duration"] = None
                            # 20-歌曲播放时长
                            youtube_music_artist_plate_data_item["duration"] = 0
                            # 21-歌曲序号
                            youtube_music_artist_plate_data_item["serial_number"] = -1
                            # 22-是否可播放
                            youtube_music_artist_plate_data_item["is_playable"] = 0
                            # 23-来自哪个模块
                            youtube_music_artist_plate_data_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                            youtube_music_artist_plate_data_item["batch"] = self.batch_date
                            youtube_music_artist_plate_data_item["youtube_music_video_image_url"] = None
                            youtube_music_artist_plate_data_item["other_info"] = None
                            yield youtube_music_artist_plate_data_item

                else:
                    pass
                youtube_music_artist_plate_crawl_situation_batch_record_item = YoutubeMusicArtistPlateCrawlSituationBatchRecordItem()
                youtube_music_artist_plate_crawl_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_artist_plate_crawl_situation_batch_record_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_artist_plate_crawl_situation_batch_record_item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_artist_plate_crawl_situation_batch_record_item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_artist_plate_crawl_situation_batch_record_item["youtube_music_playlist_infomation_remark"] = "EI"
                youtube_music_artist_plate_crawl_situation_batch_record_item["batch"] = self.batch_date
                yield youtube_music_artist_plate_crawl_situation_batch_record_item
            yield self.update_task_batch(request.task_id, 1)
        else:
            youtube_music_artist_plate_crawl_situation_batch_record_item = YoutubeMusicArtistPlateCrawlSituationBatchRecordItem()
            youtube_music_artist_plate_crawl_situation_batch_record_item["gmg_artist_id"] = request.task_gmg_artist_id
            youtube_music_artist_plate_crawl_situation_batch_record_item[
                "youtube_music_channel_id"] = request.task_youtube_music_channel_id
            youtube_music_artist_plate_crawl_situation_batch_record_item[
                "youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
            youtube_music_artist_plate_crawl_situation_batch_record_item[
                "youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
            youtube_music_artist_plate_crawl_situation_batch_record_item[
                "youtube_music_playlist_infomation_remark"] = "NI"
            youtube_music_artist_plate_crawl_situation_batch_record_item["batch"] = self.batch_date
            yield youtube_music_artist_plate_crawl_situation_batch_record_item
            yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = CrawlYoutubePagePlaylistInfoSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubePagePlaylistInfoSpider爬虫")

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
    # python crawl_youtube_page_playlist_info_spider.py --start_master  # 添加任务
    # python crawl_youtube_page_playlist_info_spider.py --start_worker  # 启动爬虫
