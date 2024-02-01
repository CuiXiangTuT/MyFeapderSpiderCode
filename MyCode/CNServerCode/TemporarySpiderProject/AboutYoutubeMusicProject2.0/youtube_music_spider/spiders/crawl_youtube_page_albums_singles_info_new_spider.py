# -*- coding: utf-8 -*-
"""
Created on 2024-01-08 18:38:25
---------
@summary:
---------
@author: QiuQiuRen
@description：
    用于获取歌手页面下的所有专辑及单曲信息

"""

import feapder
from feapder import ArgumentParser
from items.youtube_music_info_item import *


class CrawlYoutubePageAlbumsSinglesInfoNewSpider(feapder.BatchSpider):
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
        yield feapder.Request(url=url, headers=headers,
                              task_id=task_id,
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
                    "browserName": "Edge Chromium",
                    "browserVersion": "120.0.0.0"
                }
            },
            "browseId": request.task_youtube_music_playlist_id
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
            json_data_list = \
                response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                    "sectionListRenderer"]["contents"][0]["gridRenderer"]["items"]
            for per_json_data in json_data_list:
                youtube_music_playlist_data_item = YoutubeMusicPlaylistDataItem()
                youtube_music_playlist_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_playlist_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_playlist_data_item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_playlist_data_item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_playlist_data_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                # img_url
                youtube_music_playlist_data_item["img_url"] = \
                per_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"]["musicThumbnailRenderer"][
                    "thumbnail"]["thumbnails"][-1]["url"]
                # title
                youtube_music_playlist_data_item["title"] = \
                per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                # url
                youtube_music_playlist_data_item[
                    "youtube_music_albums_singles_playlist_url"] = "https://music.youtube.com/browse/" + \
                                                                   per_json_data["musicTwoRowItemRenderer"]["title"][
                                                                       "runs"][0][
                                                                       "navigationEndpoint"][
                                                                       "browseEndpoint"]["browseId"]
                # playlist_type
                youtube_music_playlist_data_item["playlist_type"] = \
                per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
                # publish_date
                youtube_music_playlist_data_item["publish_date"] = \
                per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][-1]["text"]

                youtube_music_playlist_data_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_playlist_data_item["youtube_music_albums_singles_playlist_url"]
                youtube_music_playlist_data_item["batch"] = self.batch_date
                yield youtube_music_playlist_data_item

                youtube_music_plate_url_task_item = YoutubeMusicPlateUrlTaskItem()
                youtube_music_plate_url_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_plate_url_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_plate_url_task_item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_plate_url_task_item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_plate_url_task_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_playlist_data_item["youtube_music_playlist_url_pre_redirect"]
                youtube_music_plate_url_task_item["title"] = youtube_music_playlist_data_item["title"]
                youtube_music_plate_url_task_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                yield youtube_music_plate_url_task_item


            if response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                "sectionListRenderer"]["contents"][0]["gridRenderer"].get("continuations"):
                nextContinuationData = \
                    response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                        "sectionListRenderer"]["contents"][0]["gridRenderer"]["continuations"][0][
                        "nextContinuationData"][
                        "continuation"]

                url = "https://music.youtube.com/youtubei/v1/browse?continuation={}&type=next&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false".format(
                    nextContinuationData)
                data = {
                    "context": {
                        "client": {
                            "visitorData": request.visitorData,
                            "clientName": "WEB_REMIX",
                            "clientVersion": "1.20231214.00.00",
                            "osName": "Windows",
                            "osVersion": "10.0"
                        }
                    }
                }
                print(request.visitorData)
                yield feapder.Request(url=url, json=data, visitorData=request.visitorData, callback=self.parse1,
                                      nextContinuationData=nextContinuationData,
                                      task_id=request.task_id,
                                      task_gmg_artist_id=request.task_gmg_artist_id,
                                      task_youtube_music_channel_id=request.task_youtube_music_channel_id,
                                      task_youtube_music_playlist_id=request.task_youtube_music_playlist_id,
                                      task_youtube_music_playlist_url=request.task_youtube_music_playlist_url,
                                      task_youtube_music_plate_remark = request.task_youtube_music_plate_remark,
                                      )
            else:
                yield self.update_task_state(request.task_id, 1)
        else:
            json_data_list = response.json["continuationContents"]["gridContinuation"]["items"]
            for per_json_data in json_data_list:
                youtube_music_playlist_data_item = YoutubeMusicPlaylistDataItem()
                youtube_music_playlist_data_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_playlist_data_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_playlist_data_item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_playlist_data_item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_playlist_data_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                # img_url
                youtube_music_playlist_data_item["img_url"] = \
                    per_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"]["musicThumbnailRenderer"][
                        "thumbnail"][
                        "thumbnails"][-1]["url"]
                # title
                youtube_music_playlist_data_item["title"] = \
                per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                # url
                youtube_music_playlist_data_item[
                    "youtube_music_albums_singles_playlist_url"] = "https://music.youtube.com/browse/" + \
                                                                   per_json_data["musicTwoRowItemRenderer"]["title"][
                                                                       "runs"][0][
                                                                       "navigationEndpoint"]["browseEndpoint"][
                                                                       "browseId"]
                # playlist_type
                youtube_music_playlist_data_item["playlist_type"] = \
                per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
                # publish_date
                youtube_music_playlist_data_item["publish_date"] = \
                per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][-1]["text"]
                youtube_music_playlist_data_item["youtube_music_playlist_url_pre_redirect"] = youtube_music_playlist_data_item["youtube_music_albums_singles_playlist_url"]
                youtube_music_playlist_data_item["batch"] = self.batch_date
                youtube_music_playlist_data_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                yield youtube_music_playlist_data_item

                youtube_music_plate_url_task_item = YoutubeMusicPlateUrlTaskItem()
                youtube_music_plate_url_task_item["gmg_artist_id"] = request.task_gmg_artist_id
                youtube_music_plate_url_task_item["youtube_music_channel_id"] = request.task_youtube_music_channel_id
                youtube_music_plate_url_task_item["youtube_music_playlist_id"] = request.task_youtube_music_playlist_id
                youtube_music_plate_url_task_item["youtube_music_playlist_url"] = request.task_youtube_music_playlist_url
                youtube_music_plate_url_task_item["youtube_music_playlist_url_pre_redirect"] = \
                youtube_music_playlist_data_item["youtube_music_playlist_url_pre_redirect"]
                youtube_music_plate_url_task_item["title"] = youtube_music_playlist_data_item["title"]
                youtube_music_plate_url_task_item["youtube_music_plate_remark"] = request.task_youtube_music_plate_remark
                yield youtube_music_plate_url_task_item

            if response.json["continuationContents"]["gridContinuation"].get("continuations"):
                nextContinuationData = \
                    response.json["continuationContents"]["gridContinuation"]["continuations"][0][
                        "nextContinuationData"][
                        "continuation"]
                url = "https://music.youtube.com/youtubei/v1/browse?continuation={}&type=next&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false".format(
                    nextContinuationData)
                data = {
                    "context": {
                        "client": {
                            "visitorData": request.visitorData,
                            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0,gzip(gfe)",
                            "clientName": "WEB_REMIX",
                            "clientVersion": "1.20231214.00.00",
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
                                      )
            else:
                yield self.update_task_state(request.task_id, 1)


if __name__ == "__main__":
    spider = CrawlYoutubePageAlbumsSinglesInfoNewSpider(
        redis_key="xxx:xxxx",  # 分布式爬虫调度信息存储位置
        task_table="",  # mysql中的任务表
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="xxx_batch_record",  # mysql中的批次记录表
        batch_name="xxx(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    parser = ArgumentParser(description="CrawlYoutubePageAlbumsSinglsInfoNewSpider爬虫")

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
    # python crawl_youtube_page_albums_singles_info_new_spider.py --start_master  # 添加任务
    # python crawl_youtube_page_albums_singles_info_new_spider.py --start_worker  # 启动爬虫
