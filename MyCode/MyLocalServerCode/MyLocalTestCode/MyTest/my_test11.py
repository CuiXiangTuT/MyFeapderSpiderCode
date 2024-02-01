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
        url = "https://music.youtube.com/channel/UCKh0FImZMYvIZHzMSlbschg"
        headers = {
            "authority": "music.youtube.com",
            "method": "GET",
            "path": url.replace("https://music.youtube.com", ""),
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Accept-Encoding": "gzip, deflate, br",
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
        yield feapder.Request(url=url, headers=headers)

    def parse(self, request, response):
        visitorData = response.re('"visitorData":"(.*?)",')[0]
        print(visitorData)
        url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
        # url = "https://music.youtube.com/youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false"
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
            "browseId": "MPADUCKh0FImZMYvIZHzMSlbschg"
        }
        nextContinuationData = None
        yield feapder.Request(url=url, json=data, visitorData=visitorData, callback=self.parse1,
                              nextContinuationData=nextContinuationData)

    def parse1(self, request, response):
        if request.nextContinuationData == None:
            json_data_list = \
                response.json["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
                    "sectionListRenderer"]["contents"][0]["gridRenderer"]["items"]
            for per_json_data in json_data_list:
                d = dict()
                # img_url
                d["img_url"] = per_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"]["musicThumbnailRenderer"][
                    "thumbnail"]["thumbnails"][-1]["url"]
                # title
                d["title"] = per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                # url
                d["youtube_music_playlist_url"] = "https://music.youtube.com/browse/" + \
                                                  per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0][
                                                      "navigationEndpoint"][
                                                      "browseEndpoint"]["browseId"]
                # playlist_type
                d["playlist_type"] = per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
                # publish_date
                d["publish_date"] = per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][-1]["text"]
                pprint(d)

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
                                      nextContinuationData=nextContinuationData
                                      )
            else:
                print("歌手专辑单曲信息采集结束-1")
        else:
            # if response.json["continuationContents"].get("gridContinuation"):
            json_data_list = response.json["continuationContents"]["gridContinuation"]["items"]
            for per_json_data in json_data_list:
                d = dict()
                # img_url
                d["img_url"] = \
                    per_json_data["musicTwoRowItemRenderer"]["thumbnailRenderer"]["musicThumbnailRenderer"][
                        "thumbnail"][
                        "thumbnails"][-1]["url"]
                # title
                d["title"] = per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0]["text"]
                # url
                d["youtube_music_playlist_url"] = "https://music.youtube.com/browse/" + \
                                                  per_json_data["musicTwoRowItemRenderer"]["title"]["runs"][0][
                                                      "navigationEndpoint"]["browseEndpoint"]["browseId"]
                # playlist_type
                d["playlist_type"] = per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][0]["text"]
                # publish_date
                d["publish_date"] = per_json_data["musicTwoRowItemRenderer"]["subtitle"]["runs"][-1]["text"]
                pprint(d)
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
                                      nextContinuationData=nextContinuationData
                                      )
            else:
                print("歌手专辑单曲信息采集结束-2")
            # else:
            #     print("没有获取到gridContinuation，重新获取")
            #     url = "https://music.youtube.com/channel/MPADUCsINGsXjzHOpCkNBYIbp2kg"
            #     headers = {
            #         "scheme": "https",
            #         "path": url.replace("https://music.youtube.com/", ""),
            #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            #         "Cookie": "CONSENT=PENDING+405; VISITOR_INFO1_LIVE=IGZzaH1uGfQ; _ga=GA1.1.527396337.1699502544; _ga_2LYFVQK29H=GS1.1.1699525078.2.1.1699526072.0.0.0; VISITOR_PRIVACY_METADATA=CgJaQRIEGgAgIQ%3D%3D; _gcl_au=1.1.402953871.1702980312; PREF=tz=Asia.Shanghai&autoplay=true; YSC=2VkYWfoKilM",
            #         "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            #         "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            #     }
            #     response = requests.get(url=url,headers=headers).text
            #     visitorData = re.findall('"visitorData":"(.*?)",',response)[0]
            #     inner_url = "https://music.youtube.com/youtubei/v1/browse?continuation={}&type=next&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false".format(
            #         request.nextContinuationData)
            #     data = {
            #         "context": {
            #             "client": {
            #                 "visitorData": request.visitorData,
            #                 "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0,gzip(gfe)",
            #                 "clientName": "WEB_REMIX",
            #                 "clientVersion": "1.20231214.00.00",
            #                 "osName": "Windows",
            #                 "osVersion": "10.0"
            #             }
            #         }
            #     }
            #     yield feapder.Request(url=inner_url, json=data, visitorData=visitorData, callback=self.parse1,
            #                           nextContinuationData=request.nextContinuationData
            #                           )


if __name__ == "__main__":
    MyTestAirspider().start()
