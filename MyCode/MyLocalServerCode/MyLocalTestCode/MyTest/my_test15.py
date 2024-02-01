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
from datetime import datetime
from pprint import pprint
import json


class MyTestAirspider(feapder.AirSpider):
    def download_midware(self, request):
        request.headers = {
            # 'Accept-Language': "en,zh-CN;q=0.9,zh;q=0.8",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        return request

    def start_requests(self):
        url = "https://www.youtube.com/channel/UCqECaJ8Gagnn7YCbPEzWH6g"
        yield feapder.Request(url=url)

    def parse(self, request, response):
        s = response.text
        start_marker = '"tagline":{'
        end_marker = '"moreIcon":{'

        start_index = s.find(start_marker)
        end_index = s.find(end_marker)

        if start_index != -1 and end_index != -1:
            content = "{" + s[start_index:end_index].strip()[:-1] + "}}}"
            start_token = '"token":'
            end_token = '"request":'
            start_token_index = content.find(start_token)
            end_token_index = content.find(end_token)
            token_str = "{" + content[start_token_index:end_token_index].strip()[:-1] + "}"

            token = eval(token_str)["token"]

            url = "https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"
            data = {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": "2.20240123.06.00",
                        "osName": "Windows",
                        "osVersion": "10.0"
                    }
                },
                "continuation": token
            }
            yield feapder.Request(url=url,json=data,callback=self.parse1)

        else:
            print("未找到指定的内容")

    def parse1(self,request,response):
        json_data = response.json["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"][0]["aboutChannelRenderer"]
        item = dict()
        # description
        item["description"] = json_data["metadata"]["aboutChannelViewModel"]["description"]
        # biography
        item["biography"] = json_data["metadata"]["aboutChannelViewModel"]["artistBio"]["content"]

        if json_data["metadata"]["aboutChannelViewModel"].get("country"):
            # country
            item["country"] = json_data["metadata"]["aboutChannelViewModel"]["country"]
        else:
            item["country"] = None
        # origin_subscriber_count
        origin_subscriber_count = json_data["metadata"]["aboutChannelViewModel"]["subscriberCountText"]
        item["origin_subscriber_count"] = origin_subscriber_count
        # subscriber_count
        subscriber_count = origin_subscriber_count.replace("subscribers","").replace("subscriber","").strip()
        item["subscriber_count"] = int(float(subscriber_count.lower().replace('m',''))*1000000) if 'm'  in subscriber_count.lower() else int(float(subscriber_count.lower().replace('k',''))*1000) if 'k' in subscriber_count.lower() else int(float(subscriber_count.lower().replace('b',''))*1000000000) if 'b' in subscriber_count.lower() else subscriber_count
        # origin_view_count
        origin_view_count = json_data["metadata"]["aboutChannelViewModel"]["viewCountText"]
        item["origin_view_count"] = origin_view_count
        # view_count
        item["view_count"] = origin_view_count.replace('views','').replace('view','').replace(',','').strip()
        # origin_joined_date
        origin_joined_date = json_data["metadata"]["aboutChannelViewModel"]["joinedDateText"]["content"]
        item["origin_joined_date"] = origin_joined_date
        # joined_date
        # 使用字符串处理方法提取日期部分
        date_string = origin_joined_date.replace("Joined ", "")
        # 使用datetime库解析日期字符串
        date = datetime.strptime(date_string, "%b %d, %Y")
        # 将日期转换为指定格式
        formatted_date = date.strftime("%Y-%m-%d")
        # joined_date
        item["joined_date"] = formatted_date
        # canonical_channel_url
        item["canonical_channel_url"] = json_data["metadata"]["aboutChannelViewModel"]["canonicalChannelUrl"]
        # youtube_artist_channel_id
        item['youtube_page_info_artist_channel_id'] = json_data["metadata"]["aboutChannelViewModel"]["channelId"]
        # origin_video_count
        origin_video_count = json_data["metadata"]["aboutChannelViewModel"]["videoCountText"]
        item["origin_video_count"] = origin_video_count
        # video_count
        item["video_count"] = origin_video_count.replace("videos","").replace("video","").strip()
        # links
        links_list = json_data["metadata"]["aboutChannelViewModel"]["links"]
        inner_item = dict()
        for per_link in links_list:
            plate_content = per_link["channelExternalLinkViewModel"]["title"]["content"].lower().replace(" ",'_').strip()
            inner_item[plate_content] = plate_content.replace("_(","(").replace(")_",")")
            inner_item[plate_content.replace(" ",'_')+"_url"] = "https://www."+per_link["channelExternalLinkViewModel"]["link"]["content"]
        # facebook
        item["facebook_url"] = inner_item["facebook_url"] if inner_item.get("facebook") else None
        # instagram
        item["instagram_url"] = inner_item["instagram_url"] if inner_item.get("instagram") else None
        # tiktok
        item["tiktok_url"] = inner_item["tiktok_url"] if inner_item.get("tiktok") else None
        # twitter
        item["twitter_url"] = inner_item["twitter_url"] if inner_item.get("twitter") else None
        # spotify
        item["spotify_url"] = inner_item["spotify_url"] if inner_item.get("spotify") else None
        # youtube_music
        item["youtube_music_url"] = inner_item["youtube_music_url"] if inner_item.get("youtube_music") else None
        # youtube
        item["youtube_url"] = inner_item["youtube_url"] if inner_item.get("youtube") else None
        # apple_music
        item["apple_music_url"] = inner_item["apple_music_url"] if inner_item.get("apple_music") else None
        # itunes
        item["itunes_url"] = inner_item["itunes_url"] if inner_item.get("itunes") else None
        pprint(item)
        print("----------------------------")
        pprint(inner_item)




if __name__ == "__main__":
    MyTestAirspider().start()
